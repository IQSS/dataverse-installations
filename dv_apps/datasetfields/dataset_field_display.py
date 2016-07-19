
class DatasetFieldDisplayHelper(object):
    """
    Container for the displaying a Dataset Field

    Fields may have 3 types of display values:
    """
    def __init__(self, dataset_field):
        self.dataset_field = dataset_field

        if self.dataset_field.has_multiples():
            self.value_list = []
        else:
            self.value_list = None

        self.flat_val = None
        self.vocab_list = None

    def has_multiples(self):
        if self.value_list:
            return True
        return False

    def add_flat_value(self, val):
        if val is None:
            return

        if self.has_multiples():
            self.value_list.append(val)
        else:
            self.flat_val = val

    def add_value_to_dataset_field(self, value_lookup, controlled_vocab_lookup):
        """
        Add either a "flat_val" or of "vocab_list" to the object
        """
        val = value_lookup.get(self.dataset_field.id, None)
        if val is not None:
            self.add_flat_value(val)
            return True

        self.vocab_list = controlled_vocab_lookup.get(self.dataset_field.id, None)
        if self.vocab_list is not None:
            return True

        return False

'''

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


'''
