###################################### all user defined functions #################################################

######### Function required imports ##########
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mutual_info_score
labelencoder_x = LabelEncoder()
import pandas as pd


########################################### PREPROCESSING FUNCTIONS ###############################################

def check_missing_col(df, obj=1):
    '''
        inputs => dataframe and optional parameter for object dtype
        method to check and find the columns with missing values
        returns a tuple(Column Name, missing Value Counts)
        if obj = 1 => we are checking for Object datatype columns
        else => only for int64 or float64
    '''
    if df is None:
        return None
    if obj:
        return [(x, df.shape[0]-df[x].count()) for x in df.columns if df[x].dtype=='O' and df[x].count()!=df.shape[0]]
    else:
        return [(x, df.shape[0]-df[x].count()) for x in df.columns if df[x].dtype!='O' and df[x].count()!=df.shape[0]]


def find_missing_row(col, df, obj=1):
    '''
        if col is passed, this method returns the missing value row
        like always obj=1 for object datatype
    '''
    if col is None or df is None:
        return None
    if obj:
        return [x for x in range(df.shape[0]) if type(df[col][x])!=str]
    else:
        return [x for x in range(df.shape[0]) if not x>=0]
    
    

### if there is any comman row among all, let's remove it
def common_row_missing(col, df, obj=1):
    '''
        calculates frequency of row numbers having missing values
    '''
    if col is None or df is None:
        return None
    scoring_rows = {}
    for x in col:
        for y in find_missing_row(x[0],df, obj):
            if y in scoring_rows:
                scoring_rows[y]+= 1
            else:
                scoring_rows[y] = 1
    return sorted(scoring_rows.items(), key=lambda kv: kv[1], reverse=True)[:10]




def fill_funding(col, df):
    '''
        #### intution ###
        filling missing funding values before tagging growth rate
    '''
    if col is None or df is None:
        return None
    
    funding_rec = pd.DataFrame(df.groupby('Agency')[col].mean())
    print(funding_rec.head())
    company_details =[(x,df['Agency'][x]) for x in range(df.shape[0]) if not df[col][x]>=0]
    ## print(comany_details)
    ## tuple index, agency
    for x in company_details:
        print(x[0], x[1])
        df[col][x[0]] = funding_rec[col][x[1]]



def loop_check(obj=1):
    '''
        preprocessing handy check to find missing cols
    '''
    dataset_missing_col = check_missing_col(dataset,obj)
    for x in dataset_missing_col:
        print(dataset[x[0]].head())



def fill_sub_agency(df):
    '''
        subagency values are missing filling it based on groupby agency most frequent Subagency
    '''
    ## let's fill it based on agency
    if df is None or 'Agency' not in df.columns or 'Subagency' not in df.columns:
        return None
    agency_rec = pd.DataFrame(df.groupby('Agency')['Subagency'].agg(lambda x:x.value_counts().index[0]))
    company_details =[(x,df['Agency'][x]) for x in range(df.shape[0]) if type(df['Subagency'][x])!=str]
    for x in company_details:
        df['Subagency'][x[0]] = agency_rec['Subagency'][x[1]]
    return agency_rec


def fill_single_val_col(col,df):
    '''
        fill single valued columns like single unique and nan
    '''
    if col is None or df is None:
        return None
    for x in col:
        df[col]= df[col].fillna("NOT")
        print('Handled missing values of -------------------- ',x)
        
        
def fill_missing_year(col,df):
    '''
        filling missing values of year
    '''
    if col is None or df is None or 'Agency' not in df.columns or 'Investment Name' not in df.columns:
        return None
    year_rec = pd.DataFrame(df.groupby('Agency')[col].mean())
    investment_names = [(x, df['Investment Name'][x], df['Agency'][x]) for x in range(df.shape[0]) if not df[col][x]>=0]
    for x in investment_names:
        # print(x[0],x[2])
        df[col][x[0]] = int(year_rec.ix[x[2]])


############################################# STAGE 1 FUNCTIONS ####################################################
        
## let's tag for each investment
def growth_rate(past, cur):
    '''
        ### STAGE 1 FUNCTION ###
        for tagging investment names based on growth rate percentage
    '''
    if past:
        # check for past is zero
        if cur:
            return 1 if round(((cur-past)*100/past),2) >0 else 0
        else:
            return 0
    elif cur == 0 or cur is None:
        return 0
    else:
        # logically previously no funding but now we have, so positive
        return 1
    
### checking if adding a feature growth percentage can impact 
def add_growth_per(df):
    '''
        ### STAGE 1 FUNCTION ###
        Also to add extra column as growth_percentage
    '''
    if 'C2) Funding FY2009' in df.columns and 'C1) Funding FY2008' in df.columns:
        df['growth_percentage'] = ((df['C2) Funding FY2009']-df['C1) Funding FY2008'])*100/df['C1) Funding FY2008'])
        return df
    else:
        return None


############################################# STAGE 2 FUNCTIONS ###################################################    
    
def just_label_encode(col):
    '''
        label encode data before plotting 
    '''
    if len(col)>0:
        return labelencoder_x.fit_transform(col)
    else:
        return None


def show_uni_plots(funding_var, gen_dataset):
    '''
        ### STAGE 2 FUNCTION ###
        function to plot the dataset of non-funding variables
    '''
    if funding_var is None or gen_dataset is None or len(funding_var)==0:
        return None
    for x in gen_dataset.columns:
        if x not in funding_var:
            plt.figure(x)
            gen_dataset[x] = gen_dataset[x].astype('str')
            sns.distplot(just_label_encode(gen_dataset[x]),axlabel = x, kde_kws={'color':'r'})


## target vs all non-funding var
def get_mutual_info_score(target,col):
    '''
        ### STAGE 2 FUNCTION ###
        function to calculate target vs specified column [non-funding in this context]
    '''
    
    if col is None or target is None or len(target)!=len(col):
        return None
    return mutual_info_score(target,col)
