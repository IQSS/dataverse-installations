from collections import OrderedDict
import json

class MetadataBlockInfo(object):
    """
    First attempt at this -- need add handling of multiple values
    """

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

    def as_json(self, as_string=False):

        d = OrderedDict()

        for ds_field in self.dataset_fields:
            key, val = self.get_dataset_field_as_json(ds_field)
            if val and len(val) > 0:
                d[key] = val

        if as_string:
            return json.dumps(d)

        return d

    def get_dataset_field_as_json(self, ds_field):
        """
        Return a (key, value) where the value may be a string or list
        """
        #print 'ds_field', ds_field, ds_field.datasetfieldtype.name
        #import ipdb; ipdb.set_trace()

        if ds_field.flat_val:
            if ds_field.allow_multiples():
                return (ds_field.datasetfieldtype.name, [ds_field.flat_val.value])
            else:
                return (ds_field.datasetfieldtype.name, ds_field.flat_val.value)
        elif ds_field.vocab_list:
            fmt_vocal_list = [ ds_value.value for ds_value in ds_field.vocab_list]
            if ds_field.allow_multiples():
                return (ds_field.datasetfieldtype.name, fmt_vocal_list)
            else:
                if len(fmt_vocal_list) > 0:
                    return (ds_field.datasetfieldtype.name, fmt_vocal_list[0])
                else:
                    return (ds_field.datasetfieldtype.name, None)


        elif getattr(ds_field, 'secondary_fields', None) is not None:
            #print 'ds_field.secondary_fields', ds_field.secondary_fields
            if ds_field.allow_multiples():
                val_list = []
                last_parent_id = None
                mini_dict = OrderedDict()
                for ds_sec_field in ds_field.secondary_fields:
                    if last_parent_id != None and\
                        last_parent_id != ds_sec_field.parentdatasetfieldcompoundvalue_id:
                        val_list.append(mini_dict)
                        mini_dict = OrderedDict()

                    key, val = self.get_dataset_field_as_json(ds_sec_field)
                    if key != None and val!= None:
                        mini_dict[key] = val


                    last_parent_id = ds_sec_field.parentdatasetfieldcompoundvalue_id

                if len(mini_dict) > 0:
                    val_list.append(mini_dict)
                    #if key != None and val!= None:
                    #    key_name = key
                    #    val_list.append(val)
                return (ds_field.datasetfieldtype.name, val_list)

            else:
                d2 = OrderedDict()
                for ds_sec_field in ds_field.secondary_fields:
                    key, val = self.get_dataset_field_as_json(ds_sec_field)
                    if key != None and val!= None:
                        d2[key] = val
            return (ds_field.datasetfieldtype.name, d2)
        else:
            return None, None
