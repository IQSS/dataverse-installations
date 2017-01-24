


def get_is_published_filter_param(dvobject_var_name='dvobject'):
    """
    Filter parameters to check if a dvobject has a publication date--
    which indicates that it has been published.

    Usage may be:
     filter_params = get_is_published_filter_param()
     # filter_params = {dvobject__publicationdate__isnull : False }

     list_of_PUBLISHED_datasets = Dataset.objects.filter(**filter_params)
    """
    date_var = '%s__publicationdate__isnull' % dvobject_var_name
    return {date_var : False}


def get_is_NOT_published_filter_param(dvobject_var_name='dvobject'):
    """
    Check if the dvobject has a null publication date--which indicates
    that it has NOT been published

    Usage may be:
     filter_params = get_is_NOT_published_filter_param()
     # exclude_params = {dvobject__publicationdate__isnull : True }

     list_of_UNPUBLISHED_datasets = Dataset.objects.filter(**filter_params)

    """
    date_var = '%s__publicationdate__isnull' % dvobject_var_name
    return {date_var : True}
