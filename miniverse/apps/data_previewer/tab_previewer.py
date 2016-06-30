from os.path import join, isfile
import pandas as pd
import json




def run_test():
    dir_name = 'test_files'

    dta_file = join(dir_name, 'raw_census_data.dta')
    assert isfile(dta_file), '%s cannot be None' % dta_file

    df = pd.read_stata(dta_file)
    print df[:10]
    print df.columns
    print df[:5].to_json()
    #print '%s' % df_dict
    print '-' * 40
    return
    xlsx_file = join(dir_name, 'ReligionData.Punjab.1901_1931.v1.xlsx')
    assert isfile(xlsx_file), '%s cannot be None' % xlsx_file

    df2 = pd.read_excel(xlsx_file)
    print df2[:10]
    print df2.columns

if __name__=='__main__':
    run_test()