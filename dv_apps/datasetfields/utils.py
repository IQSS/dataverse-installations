from dv_apps.datasets.models import Dataset, DatasetVersion
from dv_apps.datasetfields.models import DatasetField, DatasetFieldValue, DatasetFieldType



def get_dataset_title(dataset_version):
    """
    Traverse the dataset metadata to retrieve a dataset title

    success: (True, title)

    fail: (False, error message)
    """
    if not isinstance(dataset_version, DatasetVersion):
        return False, "dataset_version must be a DatasetVersion model"

    search_attrs = dict(name='title',\
                        required=True,\
                        metadatablock__name='citation')
    # -----------------------------
    # Get the DatasetFieldType
    # -----------------------------
    try:
        ds_field_type = DatasetFieldType.objects.get(**search_attrs)
    except DatasetFieldType.DoesNotExist:
        return False, 'DatasetFieldType for Citation title not found.  (kwargs: %s)' % search_attrs

    # -----------------------------
    # Get the DatasetField
    # -----------------------------
    search_attrs2 = dict(datasetversion__id=dataset_version.id,\
                    datasetfieldtype__id=ds_field_type.id)
    #search_attrs2 = dict(datasetversion=dataset_version,\
    #                datasetfieldtype=ds_field_type)
    ds_field = DatasetField.objects.select_related('datasetfieldtype').filter(**search_attrs2).first()

    if ds_field is None:
        return False, 'No value found for Dataset Field. (kwargs: %s)' % (search_attrs2)


    # -----------------------------
    # Get the DatasetFieldValue
    # -----------------------------
    ds_value = DatasetFieldValue.objects.filter(datasetfield=ds_field).first()
    if ds_value is not None:
        return True, ds_value.value

    return False, 'No value found for DatasetFieldValue: %s (id:%s)' % (ds_field, ds_field.id)
