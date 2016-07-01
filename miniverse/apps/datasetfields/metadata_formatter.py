from apps.datasetfields.models import DatasetField, DatasetFieldType,\
    DatasetFieldValue, DatasetFieldCompoundValue,\
    DatasetFieldControlledVocabularyValue
from collections import OrderedDict
from apps.utils.msg_util import *

class DatasetValue(object):

    def __init__(self, val_list):
        assert len(val_list) == 4, 'There must be 4 values in %s' % val_list
        self.id, self.displayorder, self.value, self.ds_field_id = val_list

    def __str__(self):
        return '%s' % (self.value)

class MetadataBlockInfo(object):

    def __init__(self, name, metadata_block):
        self.name = name
        self.metadata_block = metadata_block # metadata_block object
        self.dataset_fields = []

    def __str__(self):
        if self.metadata_block:
            return self.metadata_block.displayname

        return self.name

    def add_dataset_field(self, ds_field):
        if ds_field is None:
            return
        self.dataset_fields.append(ds_field)


class MetadataFormatter(object):
    """
    Look for a rational way to query metadata in order to switch
    to document structure.  (schema.org, JSON schema, etc)

    (1) Get datasetfield based on DatasetVersion
        (1a) Get related datasetfieldtype
    (2)
    """
    def __init__(self, dataset_version):
        self.dataset_version = dataset_version

        self.metadata_blocks = OrderedDict()
        self.metadata_fields = []  #

        self.gatherMetadata()

    def gatherMetadata(self):
        """
        Traverse the convolution!!
        """
        # (1) Gather the DatasetField objects
        #
        primary_ds_fields = DatasetField.objects.select_related('datasetfieldtype'\
            ,'datasetfieldtype__metadatablock').filter(datasetversion=self.dataset_version)

        ds_field_ids = []  # For looking up compound vals
        for ds_field in primary_ds_fields:
            ds_field_ids.append(ds_field.id)

        # -------------------------------------------
        # (2) Query the dataset compound value table to get the PKs
        #   for sub DatasetField objects
        #
        #   Map:  { id of DatasetFieldCompoundValue : parent dataset field id }
        # -------------------------------------------
        kwargs = dict(parentdatasetfield__id__in=ds_field_ids)
        compound_id_pairs = DatasetFieldCompoundValue.objects.values_list(\
            'id', 'parentdatasetfield').filter(**kwargs\
            ).order_by('displayorder')


        # -------------------------------------------
        # (3) Get the "Secondary" DatasetFields objects
        #
        #   "Crazy walk"
        #   Primary DatasetField id -> DatasetFieldCompoundValue.parentdatasetfield.id
        #       -> DatasetFieldCompoundValue.id -> Secondary DatasetField parentdatasetfieldcompoundvalue.id
        # -------------------------------------------

        # -------------------------------------------
        # (3a) Get the Compound value keys from (2)
        # -------------------------------------------
        ds_compound_ids = [compound_key for compound_key, primary_ds_id in compound_id_pairs]

        # -------------------------------------------
        # (3b) Pull the Secondary DatasetField objects
        # -------------------------------------------
        kwargs2 = dict(parentdatasetfieldcompoundvalue__id__in=ds_compound_ids)
        secondary_ds_fields = DatasetField.objects.select_related(\
            'datasetfieldtype', 'parentdatasetfieldcompoundvalue'
            ).filter(**kwargs2\
            ).order_by('parentdatasetfieldcompoundvalue_id',\
                'datasetfieldtype__displayorder')

        # -------------------------------------------
        # (3c) Map the Primary DatasetField objects to
        #    the Secondary DatasetField objects
        # -------------------------------------------

        # {primary DatasetField id  : [Secondary DatasetField, ...] }
        primary_secondary_lookup = {}

        # Iterate through the secondary fields, creating a lookup
        #
        for secondary_ds in secondary_ds_fields:
            # Check the DatasetFieldCompoundValue crosswalk to match
            #   with a primary DatasetField
            for compound_key, primary_ds_id in compound_id_pairs:
                if compound_key == secondary_ds.parentdatasetfieldcompoundvalue.id:
                    # A match!  Add it to the lookup
                    primary_secondary_lookup.setdefault(primary_ds_id, []).append(secondary_ds)

        # -------------------------------------------
        # (4) Gather the values for all of the fields
        # -------------------------------------------
        ds_field_ids += [ds.id for ds in secondary_ds_fields]

        value_lookup = self.get_value_lookup(ds_field_ids)

        controlled_vocab_lookup = self.get_controlled_vocab_lookup(ds_field_ids)


        # -------------------------------------------
        # (5) Put this mess together
        # -------------------------------------------

        # -------------------------------------------
        # (5a) Go through primary field list, adding values as needed
        # -------------------------------------------
        self.metadata_fields = []
        cnt = 0
        for ds_field in primary_ds_fields:

            ds_field.metadata_block = ds_field.datasetfieldtype.metadatablock

            cnt+=1
            #print '\n(%s) check ds_field: %s' % (cnt, ds_field)

            secondary_fields = primary_secondary_lookup.get(ds_field.id, None)

            # (A) Add primary field flat value, if it exists
            if self.add_value_to_dataset_field(ds_field, value_lookup, controlled_vocab_lookup):
                pass    # Great, flat value added
                #print '(1st) %s -> [%s]' % (ds_field.datasetfieldtype.title, ds_field.flat_val)
            elif secondary_fields:
                # (B) Add flat values to secondary fields, if they exist

                #print 'secondary fields detected!'
                # Iterate through secondary fields, adding values to each
                ds_field.secondary_fields = []
                for sec_field in secondary_fields:
                    self.add_value_to_dataset_field(sec_field, value_lookup, controlled_vocab_lookup)
                    ds_field.secondary_fields.append(sec_field)
                #for sf in ds_field.secondary_fields:
                #    print '(2nd) %s -> [%s]' % (sf.datasetfieldtype.title, sf.flat_val)
            else:
                msgt('AINT got nuthin: %s: %s' % (ds_field, ds_field.datasetfieldtype.title))

            self.metadata_fields.append(ds_field)
            self.add_to_metadata_blocks(ds_field)

    def add_to_metadata_blocks(self, dataset_field):

        if len(self.metadata_blocks) == 0:  # Initialize
            self.metadata_blocks = OrderedDict()

        metadata_block_name = dataset_field.metadata_block.name
        #msgx(dataset_field.metadata_block.__class__)
        block_info = self.metadata_blocks.get(metadata_block_name, None)
        if block_info is None:
            block_info = MetadataBlockInfo(metadata_block_name, dataset_field.metadata_block)
            self.metadata_blocks[metadata_block_name] = block_info

        block_info.add_dataset_field(dataset_field)



    def add_value_to_dataset_field(self, ds_field, value_lookup, controlled_vocab_lookup):
        """
        Add either a "flat_val" or of "vocab_list" to the object
        """
        ds_field.flat_val = value_lookup.get(ds_field.id, None)
        if ds_field.flat_val is not None:
            return True

        ds_field.vocab_list = controlled_vocab_lookup.get(ds_field.id, None)
        if ds_field.vocab_list is not None:
            return True

        return False

    def get_value_lookup(self, dataset_field_ids):

        value_lookup = {}

        # ----------------------
        # Flat values
        # ----------------------
        ds_values = DatasetFieldValue.objects.values_list(\
            'id', 'displayorder', 'value', 'datasetfield__id'\
            ).filter(datasetfield__id__in=dataset_field_ids)

        for ds_val in ds_values:
            datasetValue = DatasetValue(ds_val)
            value_lookup[datasetValue.ds_field_id] = datasetValue

        #for key, val in value_lookup.items():
        #    msg('%s -> [%s]' % (key, val.value))
        return value_lookup


    def get_controlled_vocab_lookup(self, dataset_field_ids):
        """
        Given a list of DatasetField Ids:
            - Retrieve any controlled vocabulary
            - Return a dict of { dataset id : [DatasetValue, DatasetValue, etc]}
        """
        vocab_lookup = {}

        # ----------------------
        # Controlled Vocab values
        # ----------------------
        ds_vocab_values = DatasetFieldControlledVocabularyValue.objects.select_related(\
                'controlledvocabularyvalues', 'datasetfield').filter(\
                datasetfield__id__in=dataset_field_ids)

        for vocab_value in ds_vocab_values:
            vocab_val_list = (vocab_value.controlledvocabularyvalues.id,\
                    vocab_value.controlledvocabularyvalues.displayorder,\
                    vocab_value.controlledvocabularyvalues.strvalue,\
                    vocab_value.datasetfield.id)
            datasetValue = DatasetValue(vocab_val_list)

            vocab_lookup.setdefault(vocab_value.datasetfield.id, []\
                ).append(datasetValue)

        #for key, val in vocab_lookup.items():
        #    msg('%s -> [%s]' % (key, val))
        return vocab_lookup
