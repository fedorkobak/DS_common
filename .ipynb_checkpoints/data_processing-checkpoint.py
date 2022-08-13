# funciton for data processing
import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder


def insert_next(df, col_name, transform_col, new_name = None):
    '''
        Insertion to data frame after given colum
            Inputs:
                df - pandas.DataFrame in which the insertion is required;
                col_name - str the name of the column after which insertion is required;
                transform_col - pandas.Series to be inserted;
                new_name - str name of new column, by default col_name + "_transf" will used.
            Output
                pd.DataFrame with inserted column.
    '''
    if new_name is None:
        new_name = col_name + "_transf"
    
    if new_name in df.columns:
        df[new_name] = transform_col
    else:
        df.insert(
            df.columns.get_loc(col_name) + 1,
            new_name,
            transform_col
        )
    
    return df


def get_num_cond(df):
    '''
        Get condition for selection from pandas.DataFrame numeric data types
            Inputs:
                df - pandas.DataFrame which numeric columns you have to choose;
            Output
                pd.Series contains boolen dtype condition.
    '''
    return df.apply(lambda x: pd.api.types.is_numeric_dtype(x.dtype))



def pd_OHE(df, sk_OHE_kwarg = {}):
    '''
        One hot encoding for pandas.DataFrame. Result type steel
        pandas.DataFrame and columns have readable names, in fomat colname_catname.
            Inputs:
                df - pandas.DataFrame for one hot encoding;
                sk_OHE_kwag - dict which contains sklearn.preprocessing.OneHotEncoding arguments.
            Output pandas.DataFrame with incoed features.
    '''
    
    def name_cat(cats, name, drop_idx = None):
        '''
            For givent categoryes and name
            returns list of strings "category_name" with
            len of cats array
        '''
        # if some columns droped we need to delete related
        # category from columns names
        if not drop_idx is None:
            cats = np.delete(cats, drop_idx)
            
        return list(map(lambda x: name + "_" + str(x), cats))
    
    sk_OHE_kwarg["sparse"] = False
    my_ohe = OneHotEncoder(**sk_OHE_kwarg).fit(df)
    
    columns = []
    for i in range(len(my_ohe.categories_)):
        if not my_ohe.drop_idx_ is None:
            columns += name_cat(my_ohe.categories_[i], df.columns[i], drop_idx = my_ohe.drop_idx_[i])
        else:
            columns += name_cat(my_ohe.categories_[i], df.columns[i])
    
    return pd.DataFrame(my_ohe.transform(df), columns = columns, index = df.index)

def np_replace(arr, rule):
    '''
        Replacing funciton for numpy array.
        Inputs:
            arr - numpy array to be transformed;
            rule - rule as dict.
        Output trancfromed numpy array.
    '''
    rule_values = np.array(list(rule.values()))
    rule_keys = np.array(list(rule.keys()))
        
    replacer = lambda key: rule_values[key == rule_keys][0] if np.any(key == rule_keys) else key
        
    return np.array(list(map(replacer, arr.ravel()))).reshape(arr.shape)

def get_merge_repl_rule(joiners):
    '''
        Get an merging rule for the levels of some variable 
        for further use in pandas.Series.replace
        Inputs:
            joiners - where each nested list is a list 
                      of levels to form a new, merged level;
        Output dictionary with format {<old_level>:<new_level>}
    '''
    
    rule = {}
    
    for join_lev in joiners:
        res_level = join_lev[0]
        for lev in join_lev[1:]:
            res_level += "_" + lev
        for lev in join_lev:
            rule[lev] = res_level
            
    return rule