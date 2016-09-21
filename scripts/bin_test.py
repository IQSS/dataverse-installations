if __name__ == '__main__':
    import os, sys
    import django
    from os.path import realpath, dirname
    proj_path = dirname(dirname(realpath(__file__)))

    sys.path.append(proj_path)
    #sys.path.append(dirname(proj_path))
    django.setup()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miniverse.settings.local")

import random
import numpy as np
import pandas as pd
from django.db.models import F

from dv_apps.datasets.models import *
from dv_apps.datafiles.models import FileMetadata

def run_test1():

    raw_data = {'regiment': ['Nighthawks', 'Nighthawks', 'Nighthawks', 'Nighthawks', 'Dragoons', 'Dragoons', 'Dragoons', 'Dragoons', 'Scouts', 'Scouts', 'Scouts', 'Scouts'],
            'company': ['1st', '1st', '2nd', '2nd', '1st', '1st', '2nd', '2nd','1st', '1st', '2nd', '2nd'],
            'name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze', 'Jacon', 'Ryaner', 'Sone', 'Sloan', 'Piger', 'Riani', 'Ali'],
            'preTestScore': [4, 24, 31, 2, 3, 4, 24, 31, 2, 3, 2, 3],
            'postTestScore': [25, 94, 57, 62, 70, 25, 94, 57, 62, 70, 62, 70]}
    df = pd.DataFrame(raw_data, columns = ['regiment', 'company', 'name', 'preTestScore', 'postTestScore'])
    print df

    bins = [0, 25, 50, 75, 100]
    group_names = ['Low', 'Okay', 'Good', 'Great']

    categories = pd.cut(df['postTestScore'], bins, labels=group_names)
    df['categories'] = pd.cut(df['postTestScore'], bins, labels=group_names)
    print categories

    pd.value_counts(df['categories'])

    print df

def get_rand_num_array(cnt, low_num=1, high_num=100):

    l = []
    for x in range(0, cnt):
        l.append(random.randint(low_num, high_num))
    return l

def get_bin_list(step=10, low_num=0, high_num=100):
    assert high_num > low_num, "high_num must be greater than low_num"
    assert low_num >= 0, "low_num must be at least 0.  Cannot be negative"
    assert step > 0, "step must greater than 0"
    assert high_num > step, "step must lower than high_num"

    l = []
    next_num = low_num
    while next_num <= high_num:
        l.append(next_num)
        next_num += step
    return l

def run_test3():

    # Make query
    ds_version_counts = FileMetadata.objects.all(\
                        ).annotate(dsv_id=F('datasetversion__id'),\
                        ).values('dsv_id',\
                        ).annotate(cnt=models.Count('datafile__id')\
                        ).values('dsv_id', 'cnt'\
                        ).order_by('-cnt')

    # Convert to Dataframe
    df = pd.DataFrame(list(ds_version_counts), columns = ['dsv_id', 'cnt'])

    #print df
    print df['cnt'].max()
    print '-' * 10

    step_num = 20
    bins = get_bin_list(step=10, low_num=0, high_num=199)
    bins += get_bin_list(step=100, low_num=200, high_num=999)
    bins += get_bin_list(step=1000, low_num=1000, high_num=df['cnt'].max()+1000)

    #bins + = get_bin_list(step=step_num, low_num=0, high_num=df['cnt'].max()+step_num)

    print 'bins', bins
    print '-' * 10

    df['bin_label'] = pd.cut(df['cnt'], bins)

    print '-' * 10
    print df
    print '-' * 10
    vcounts = pd.value_counts(df['bin_label'])
    print 'vcounts\n', vcounts
    print '-' * 10

    d = vcounts.to_dict()
    print '=' * 40

    new_dict = {}
    for k, v in d.items():
        #if v > 0:
        sort_key = int(k[1:-1].split(',')[0])
        new_dict[sort_key] = (k, v)


    keys = new_dict.keys()
    keys.sort()
    for k in keys:
        info = new_dict[k]
        #print '(%d) %s    %s' % (k, info[0], info[1])
        print '%s    %s' % (info[0], info[1])

    #for info in ds_version_counts:
    #    print info



    '''
    ds_counts_by_month = ds_counts_by_month.annotate(\
        yyyy_mm=TruncYearMonth('%s' % date_param)\
        ).values('yyyy_mm'\
        ).annotate(cnt=models.Count('dvobject_id')\
        ).values('yyyy_mm', 'cnt'\
        ).order_by('%syyyy_mm' % self.time_sort)
    '''
def run_test2():

    orig_animals = ['cat', 'dog', 'mouse']
    animals = orig_animals * 3

    raw_data = { 'animal' : animals,
                'score' : get_rand_num_array(len(animals))
    }

    # make DataFrame
    #
    df = pd.DataFrame(raw_data, columns = ['animal', 'score'])

    print '-' * 10
    print df
    print '-' * 10
    #return

    # Create array for bins
    #
    bins = get_bin_list(step=20, low_num=0, high_num=100)

    # For each score assign it to a bin
    #
    labels = pd.cut(df['score'], bins)

    # Same as above but adding the bin value as a column to the DataFrame
    #
    df['bin_label'] = pd.cut(df['score'], bins)
    print type(df)
    print df.describe
    print '-' * 10

    from collections import Counter
    c = Counter(df['bin_label'])
    print '-' * 10
    print c

    vcounts = pd.value_counts(df['bin_label'])
    print vcounts
    #print 'by_bin', by_bin
    print '-' * 10
    vcounts = df['bin_label'].value_counts()
    d = vcounts.to_dict()
    keys = d.keys()
    keys.sort()
    for k in keys:
        print k, d[k], type(k)

    return
    # Show the count in each bin
    #
    vc_series = pd.value_counts(df['bin_label'])
    print '\n', 'vc_series', vc_series
    print '-' * 10

    print vc_series.axes
    import ipdb; ipdb.set_trace()
    #vc_series.sort_values(inplace=True, axis=0)
    #print '\n', 'vc_series', vc_series

    #print pd.value_counts(df['bin_label'])

    #print '\n', grouped

    #print Dataset.objects.all().count()

if __name__ == '__main__':
    run_test3()
