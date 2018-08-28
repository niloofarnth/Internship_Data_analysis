# -*- coding: utf-8 -*-
'''
@author: nxtehr
'''

#import the required libraries
import pandas as pd
from scipy import stats


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
function for cleaning the data for all the samples
    inputs:
        1. sheetname :"front" or "back" which corresponds to the location of testing
        2. path : the location of the file    
    construnction of the input file: 
        the file can have the following columns:
        sample,Thickness (mm),	quenching temperature °C,	partitioning temperature °C,
        partitioning time (min),P(L.M.),retained austenite %,	max strain,stress at UTS (MPa),
        yield stress (MPa),strain at UTS,	K,	n_R^2	,n_SD,LCVN RT(J),	LCVN -20C(J),LCVN -40C(J),
        Average Hardness (HBW),n,c% in austenite
    output: it gives the dataframe of the cleaned data from the excel sheet for 
            the back and front samples separately with added columns
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def front_or_back(sheetname,path):
    
    #read the excel file
    xls = pd.ExcelFile(path)
    #get the sheet for the front data 
    if sheetname == 'front':
        raw_data = pd.read_excel(xls, 'front plastic')
        #choose the range of the data needed in the excel sheet
        raw_data = raw_data.iloc[:35,10:]   
        raw_data['sample'] = raw_data['sample'].astype('object')
        
    # the sheet for the back data 
    elif sheetname == 'back':
        raw_data = pd.read_excel(xls, 'back plastic')
        #choose the range of the data needed in the excel sheet
        raw_data = raw_data.iloc[:35,10:]   
        
    #creating the new required columns and renaming the other columns    
    raw_data['yield ratio'] = raw_data['yield stress (MPa)']/raw_data['stress at UTS (MPa)']
    raw_data.rename(columns = {'yield ratio':'$S_y$/$S_{UTS}$'}, inplace = True)
    raw_data.rename(columns = {'strain at UTS':'$e_{UTS}$'}, inplace = True)
    raw_data.rename(columns = {'max strain':'%El'}, inplace = True)
    raw_data.rename(columns = {'stress at UTS (MPa)':'$S_{UTS}$'}, inplace = True)
    raw_data.rename(columns = {'R^2':'$R^2$'}, inplace = True)
    raw_data['%El'] = pd.to_numeric(raw_data['%El']*100,errors = 'coerce')
    
    #rearrange the column order. 
    cols = list(raw_data)
    cols.insert(11, cols.pop(cols.index('$S_y$/$S_{UTS}$')))
    #here we can choose which columns to show in the final data frame
    raw_data = raw_data.loc[:, cols]
    
    return raw_data 

#uncomment the next 3 lines to check the resuls of the upper function
#path = 'C:/Users/nxtehr/Documents/Q&P/Q&P tensile test files/Q&P Files/plasic strain_new.xlsx'
#front = front_or_back('front',path)
#back = front_or_back('back',path)



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
function for calculating the correlation between each two variables for in the dataframe
obtained in the front_or_back function
    inputs: 
        1. sheetname :"front" or "back" which corresponds to the location of testing
        2. path : the location of the file   
    output:
        it gives a dataframe showing the linear regression results for each two columns
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def corr_front_or_back(sheetname,path, save_fig_yn = 'n', plot = 'n'):
    #get the data from front_or_back function and remove the sample name and thickness
    data = front_or_back(sheetname,path)
    data = data[data.columns[2:]].astype(float)
    all_values = []
    
    #getting the correlation one by one between each two columns(var1,var2)...
    for col in data.columns:
        idx = data.columns.get_loc(col)+1
        while idx <len(data.columns):
            var1 = data[col]
            var2 = data[data.columns[idx]]
            
            #exclude the correlations with SD, R2 values and K
            if (var1.name in ['n_SD' ,'n_R^2','K']) or (var2.name in ['n_SD' ,'n_R^2','K']) :
                idx += 1
                continue
            
            #create the new DF from the two columns
            new_df = pd.concat([var1, var2], axis=1)
            
            #drop any row with NaN value
            new_df = new_df.dropna(how = 'any')
            
            #get the linear regression data, such as r value, p value and standard deviation
            slope, intercept, r_value, p_value, std_err = stats.linregress(new_df.iloc[:,0],new_df.iloc[:,1])
            #add the data above to the values list
            values = [sheetname,col,data.columns[idx],slope, intercept, r_value,r_value**2, p_value, std_err]
            #add the regression data for each two column to one main list
            all_values.append(values)
            idx += 1
    #make a dataframe from all_values list, showing the correlation of each two varibale in a row       
    corr_f_or_b_DF = pd.DataFrame(all_values, columns = ['location','var1','var2','slope','intercept','r_value',\
                                                         'r^2 value','p_value','std-err'])
    return corr_f_or_b_DF
            
#uncomment the next 3 lines to check the resuls of the upper function
#path = 'C:/Users/nxtehr/Documents/Q&P/Q&P tensile test files/Q&P Files/plasic strain_new.xlsx'
#a = corr_front_or_back('front',path, save_fig_yn = 'n', plot = 'n')


