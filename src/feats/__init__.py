import pandas as pd
import numpy as np

def sum_document_flags(df):
    cnt = np.zeros(df.shape[0])
    for i in range(2, 22):
        col = f'FLAG_DOCUMENT_{i}'
        cnt = df[col] + cnt
    return cnt

def age_category(df):
    age = (df.DAYS_BIRTH * -1)/365
    ageC = pd.cut(age, list(range(0, 101, 5)), right=False)
    return ageC

def organization_type_categ(df):
    types = ['Business Entity Type 3' 'XNA' 'Self-employed' 'Other' 'Medicine'
    'Business Entity Type 2' 'Government' 'School' 'Trade: type 7'
    'Kindergarten' 'Construction']
    return df.ORGANIZATION_TYPE.apply(lambda x: x if x in types else 'other').astype('category')


def target_encoding(df, test_df, column):
    df.groupby('TARGET')


def app_features(df):
    df['X_AMT_LOAN_PERIOD'] = df['AMT_CREDIT'] / df['AMT_ANNUITY']
    df['X_AMT_GOODS_RATIO'] = df['AMT_GOODS_PRICE'] / df['AMT_CREDIT']
    # df['AMT_GOODS_DIFF'] = df['AMT_CREDIT'] - df['AMT_GOODS_PRICE']
    # df['AMT_CREDIT_INCOME_RATIO'] = df['AMT_CREDIT'] / df['AMT_INCOME_TOTAL']
    # df['AMT_ANNUITY_INCOME_RATIO'] = df['AMT_ANNUITY'] / df['AMT_INCOME_TOTAL']

    # NaN values for DAYS_EMPLOYED: 365.243 -> nan
    df['DAYS_EMPLOYED'].replace(365243, np.nan, inplace= True)

    # Social features
    df['X_WORKING_LIFE_RATIO'] = df['DAYS_EMPLOYED'] / df['DAYS_BIRTH']
    df['X_INCOME_PER_FAM'] = df['AMT_INCOME_TOTAL'] / df['CNT_FAM_MEMBERS']

    df['X_HOUR_APPR_PROCESS_START'] = df.HOUR_APPR_PROCESS_START.astype('category')
    del df['HOUR_APPR_PROCESS_START']

    df['X_OCCUPATION_TYPE'] = df.OCCUPATION_TYPE.astype('category')
    del df['OCCUPATION_TYPE']

    for i in range(2, 22):
        c = f'FLAG_DOCUMENT_{i}'
        del df[c]

    columns = ['APARTMENTS_AVG', 'BASEMENTAREA_AVG', 'YEARS_BEGINEXPLUATATION_AVG', 'YEARS_BUILD_AVG', 'COMMONAREA_AVG', 'ELEVATORS_AVG', 'ENTRANCES_AVG',
      'FLOORSMAX_AVG', 'FLOORSMIN_AVG', 'LANDAREA_AVG', 'LIVINGAPARTMENTS_AVG', 'LIVINGAREA_AVG', 'NONLIVINGAPARTMENTS_AVG', 'NONLIVINGAREA_AVG', 'APARTMENTS_MODE',
      'BASEMENTAREA_MODE', 'YEARS_BEGINEXPLUATATION_MODE', 'YEARS_BUILD_MODE', 'COMMONAREA_MODE', 'ELEVATORS_MODE', 'ENTRANCES_MODE', 'FLOORSMAX_MODE', 'FLOORSMIN_MODE',
      'LANDAREA_MODE', 'LIVINGAPARTMENTS_MODE', 'LIVINGAREA_MODE', 'NONLIVINGAPARTMENTS_MODE', 'NONLIVINGAREA_MODE', 'APARTMENTS_MEDI', 'BASEMENTAREA_MEDI',
      'YEARS_BEGINEXPLUATATION_MEDI', 'YEARS_BUILD_MEDI', 'COMMONAREA_MEDI', 'ELEVATORS_MEDI', 'ENTRANCES_MEDI', 'FLOORSMAX_MEDI', 'FLOORSMIN_MEDI', 'LANDAREA_MEDI',
      'LIVINGAPARTMENTS_MEDI', 'LIVINGAREA_MEDI', 'NONLIVINGAPARTMENTS_MEDI', 'NONLIVINGAREA_MEDI', 'FONDKAPREMONT_MODE', 'HOUSETYPE_MODE', 'TOTALAREA_MODE',
      'WALLSMATERIAL_MODE', 'EMERGENCYSTATE_MODE'
      ]

    for c in columns:
      del df[c]

def app_stat_features(df, test_df):
    columns = ['OCCUPATION_TYPE', 'AMT_INCOME_TOTAL']
    df2 = pd.concat([df[columns], test_df[columns]])
    occ_median = df2.groupby('OCCUPATION_TYPE').median().reset_index()
    occ_median.rename(columns={ 'AMT_INCOME_TOTAL': 'X_MEDIAN_OCCUPATION_INCOME' }, inplace=True)

    df = df.merge(right=occ_median, how='left', on='OCCUPATION_TYPE')
    test_df = test_df.merge(right=occ_median, how='left', on='OCCUPATION_TYPE')
    return (df, test_df)

def prev_features(df):
    # AMT APPLICATION
    diff = (df['AMT_APPLICATION'] - df['AMT_CREDIT']) / df['AMT_CREDIT']
    df['X_AMT_APPLICATION_DIFF_RATIO'] = diff
    del df['AMT_APPLICATION']

def combined_features(df):
    df['X_APPROVTED_AMT_CREDIT_RATIO'] = df['AMT_CREDIT'] / df['prev_X_MAX_AMT_CREDIT']
    return True