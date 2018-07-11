from mainfunctions import *
import pandas as pd
import pytest
import random

dataset = pd.read_excel('./Dataset/2010 Federal STEM Education Inventory Data Set.xls', skiprows=1)
df = dataset.copy()
dummy_false_df, dummy_true_df = pd.DataFrame(dataset['C1) Funding FY2008']), pd.DataFrame(dataset[['C1) Funding FY2008','C2) Funding FY2009']])

######################################## PREPROCESSING TEST CASES #################################################

def test_check_missing_col():
    '''
        check_missing_col(df, obj=1 or 0)
    '''
    with pytest.raises(expected_exception=TypeError,  message="Expecting TypeError with no required args passed"):
        check_missing_col()
    assert check_missing_col(None) == None, "Failed at df is None"
    assert check_missing_col(pd.DataFrame()) == [], "Failed at empty dataframe"
    

def test_find_missing_row():
    '''
        find_missing_row(col,df,obj)
    '''
    with pytest.raises(expected_exception=TypeError,  message="Expecting TypeError with no required args passed"):
        find_missing_row()
    assert find_missing_row(None,None) == None, "Failed at either of col or df as None"
    assert find_missing_row(None,dummy_true_df) == None, "Failed at Column can't be None"
    assert find_missing_row(['some funny variable'], None) == None, "Failed at df as None"
    with pytest.raises(expected_exception=KeyError, message="Failed at no keyerror message"):
        find_missing_row('abc',df)
        
def test_common_row_missing():
    '''
        common_row_missing(col,df,obj=1 or 0)
    '''
    with pytest.raises(expected_exception=TypeError,  message="Expecting TypeError with no required args passed"):
        common_row_missing()
    assert common_row_missing(None,None) == None, "Failed at either of col or df as None"
    assert common_row_missing(None,dummy_true_df) == None, "Failed at Column can't be None"
    assert common_row_missing(['some funny variable'], None) == None, "Failed at df as None"
    with pytest.raises(expected_exception=KeyError, message="Failed at no keyerror message"):
        common_row_missing('abc',df)


def test_fill_funding():
    '''
        fill_funding(col,df)
    '''
    with pytest.raises(expected_exception=TypeError,  message="Expecting TypeError with no required args passed"):
        fill_funding()
    assert fill_funding(None,None) == None, "Failed at either of col or df as None"
    assert fill_funding(None,dummy_true_df) == None, "Failed at Column can't be None"
    assert fill_funding(['some funny variable'], None) == None, "Failed at df as None"
    with pytest.raises(expected_exception=KeyError, message="Failed at no keyerror message"):
        fill_funding('abc',df)
     
        
def test_fill_sub_agency():
    '''
        fill_sub_agency(df)
    '''
    with pytest.raises(expected_exception=TypeError,  message="Expecting TypeError with no required args passed"):
        fill_sub_agency()
    assert fill_sub_agency(pd.DataFrame()) == None, "Failed at empty dataframe"
    assert fill_sub_agency(None) == None, "Failed at None"
    
    
def test_fill_single_val_col():
    '''
        fill_single_val_col(col,df)
    '''
    with pytest.raises(expected_exception=TypeError,  message="Expecting TypeError with no required args passed"):
        fill_single_val_col()
    assert fill_single_val_col(None,None) == None, "Failed at either of col or df as None"
    assert fill_single_val_col(None,dummy_true_df) == None, "Failed at Column can't be None"
    assert fill_single_val_col([1,2,3], None) == None, "Failed at df as None"
    with pytest.raises(expected_exception=KeyError, message="Failed at no keyerror message"):
        fill_single_val_col('abc',df)
        
        
def test_fill_missing_year():
    '''
        fill_missing_year(col=,df=)
    '''
    with pytest.raises(expected_exception=TypeError,  message="Expecting TypeError with no required args passed"):
        fill_missing_year()
    assert fill_missing_year(None,None) == None, "Failed at either of col or df as None"
    assert fill_missing_year(None,dummy_true_df) == None, "Failed at Column can't be None"
    assert fill_missing_year([1,2,3], None) == None, "Failed at df as None"
    with pytest.raises(expected_exception=KeyError, message="Failed at no keyerror message"):
        fill_missing_year('abc',df)
        

############################################# STAGE 1 TESTCASES ####################################################     
        
def test_growth_rate():
    '''
        growth rate(pastValue, CurValue)
    '''
    with pytest.raises(expected_exception=TypeError,  message="Expecting TypeError with no required args passed"):
        growth_rate()
    assert growth_rate(12,0) == 0, "Failed at no funding at present"
    assert growth_rate(0,random.random()) == 1, "Failed at no funds in past"
    assert growth_rate(0,0) == 0, "Failed at no funds at anytime"
    assert growth_rate(None,None) == 0, "Failed at funds are None"
    assert growth_rate(None,0) == 0, "Failed at if past funds is None"
    assert growth_rate(0,None) == 0, "Failed at if current funds is None"
    assert growth_rate(10,None) == 0, "Failed at if current funds None and past has funds"
    
    
def test_add_growth_per():
    '''
        growth rate per(df)
    '''
    with pytest.raises(expected_exception=TypeError,  message="Expecting TypeError with no required args passed"):
        add_growth_per()
    dummy_false_df, dummy_true_df = pd.DataFrame(dataset['C1) Funding FY2008']), pd.DataFrame(dataset[['C1) Funding FY2008','C2) Funding FY2009']])
    assert add_growth_per(dummy_false_df) == None
    assert add_growth_per(dummy_true_df) is not None, "Cannot add growth percentage"
    assert add_growth_per(dummy_false_df) is None, "Dataframe has no required columns"
    

############################################## STAGE 2 TESTCASES ##################################################     

def test_just_label_encode():
    '''
        just_label_encode(col)
    '''
    with pytest.raises(expected_exception=TypeError,  message="Expecting TypeError with no required args passed"):
        just_label_encode()
    col = ['Hello','Python','World']
    assert list(just_label_encode(col)) == [0,1,2], "Encoding error"
    assert len(list(just_label_encode(col))) == len(col), "Different in length output"
    assert just_label_encode([]) == None
    
    
def test_show_uni_plots():
    '''
        show_uni_plots(funding_var, df)
        In this context we always provide funding_var as a list not as NoneType
    '''
    with pytest.raises(expected_exception=TypeError,  message="Expecting TypeError with no required args passed"):
        show_uni_plots()
    
    false_var, true_var = [], [1,2,3]
    assert show_uni_plots(true_var,pd.DataFrame()) == None, "Failed at empty dataframe"
    assert show_uni_plots(true_var, None) == None, "Failed at dataframe as None"
    assert show_uni_plots(None,None) == None, "Failed at either funding_var or dataframe as None"
    assert show_uni_plots(None,dummy_false_df) == None, "Failed at funding_var as none"
    assert show_uni_plots(false_var, dummy_false_df) == None, "Failed at funding_var as empty list"
    
    
def test_get_mutual_info_score():
    '''
        get_mutual_info_score(target,col)
    '''
    with pytest.raises(expected_exception=TypeError,  message="Expecting TypeError with no required args passed"):
        get_mutual_info_score()
    col = ['Hello','Python','World']
    assert get_mutual_info_score([1,2],['my-dummy-col']) == None, "Failed at different length case"
    assert get_mutual_info_score([1,2],['hel','wor']) is not None, "Failed at getting mutual info score"
    assert get_mutual_info_score(['1',2],None) == None, "Failed at col is None"
    assert get_mutual_info_score(None,['1',2]) == None, "Failed at target as None"
    