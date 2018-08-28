# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 08:46:31 2018

@author: nxtehr
"""
import pandas as pd
import matplotlib.pyplot as plt
import plotting_functions
import basic_functions
import instant_n
import weld_hardness_contour
import os

#you can change the path to wherever the main excel file is
#make sure that when you are changing the path, you are usign '/', not '\'
path = 'J:/nxtehr/My study/complete_data.xlsx'

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''PLOTTING EACH TWO VARIABLES VS EACH OTHER FOR ALL THICKNESSES TOGETHER'''
#get the possible variables
variables = list(basic_functions.front_or_back('front',path).columns[2:])
variables = pd.Series(variables)
print (variables)
#look at the printed variables and choose the index of any variable you want to plot
#the variable you choose will be as x axis and all the other variabels will be its y axis in different plots
#for example number 3 corresponds to P(L.M)
#you can choose more than one variable at the same time
desired_variables = [variables[17]]

#you can change the arguments in the function based on you needs. read below for detailed explanations of arguments
'''desired_corr_names = the varibale you chose as the xaxis
   thickness = 'all' for all the plots to be plotted in the same plot. you can choose between 6,10,12.7,16,19 to have the other thicknesses
   fit = if you want to have the fitted line on the plot
   r2 = if you chose to have the fitted line, you can choose the min R2 value that is accepted to you (default is 0.7 now)
   plot = this plot is generating data for other functions so there are some cases that we just want to have the 
          data and not the plots. if you want to plot the results, the plot argument should be "y"'''
          
'''!!!!!!!!!!!PLOT!!!!!!!!!!!!'''        
#if you do not want this part to be plotted, simply comment the line below (and uncomment it when you want to have the plots)         
plotting_functions.corr_f_and_b_thickness(var = desired_variables,path = path, thickness = 'all' ,fit = 'n',r2 = 0.7, plot = 'y')
          
          
#if you want to have a dataframe showing all the correlations between each two variable, run the line below
#then open the all_correlations varibale from the varibales tab on top right window
all_columns = basic_functions.front_or_back('back',path).columns[2:].tolist()      
all_correlations, values_Df_both = plotting_functions.corr_f_and_b_thickness(var = all_columns,path = path)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''PLOTTING TWO VARIBALES VS EACH OTHER FOR EACH THICKNESS IN SUBPLOTS'''
variables = list(basic_functions.front_or_back('front',path).columns[2:])
variables = pd.Series(variables)
print(variables)
'''xaxis = the varibale you chose as the xaxis from the variabels list printed in the line above
   yaxis = make sure that the yaxis you choose is a varibale that comes after the xaxis variable in the variables list printed
           otherwise you get the message saying exchange x and y
   fit = if you want to have the fitted line on the plot
   r2 = if you chose to have the fitted line, you can choose the min R2 value that is accepted to you (default is 0.7)
   temper = whether you want to add 2 data points for the tempered reference sample to the plot or not'''
xaxis =  'retained austenite %'
yaxis = 'yield stress (MPa)'

'''!!!!!!!!!!!PLOT!!!!!!!!!!!!'''    
#if you do not want this part to be plotted, simply comment the line below (and uncomment it when you want to have the plots)         
plotting_functions.two_var_fb_subplot(xaxis,yaxis,path, fit = 'n', r2 = 0.7, temper = 'n')        
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''PLOTTING THE VARIBALES VS QT WHILE HAVING THE PT AS THE COLOR ON EACH POINT'''
variables = list(basic_functions.front_or_back('front',path).columns[2:])
variables = pd.Series(variables)
print(variables)
'''!!!!!!!!!!!PLOT!!!!!!!!!!!!'''    
plotting_functions.plot_QT_PT(variables = ['retained austenite %'], path = path)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''PLOTTING THE VARIBALES VS PT FOR 12.7 MM SAMPLE WITH Pt WRITTEN ON THE PLOT'''
variables = list(basic_functions.front_or_back('front',path).columns[2:])
variables = pd.Series(variables)
print(variables)
'''!!!!!!!!!!!PLOT!!!!!!!!!!!!'''    
plotting_functions.plot_PT_12mm('retained austenite %',path = path,legend_loc = 2)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''PLOTTING THE 3D PLOTS'''
variables = list(basic_functions.front_or_back('front',path).columns[5:])
variables = pd.Series(variables)
print(variables)
'''!!!!!!!!!!!PLOT!!!!!!!!!!!!'''    
plotting_functions.plot_3D(['yield stress (MPa)'],path)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''PLOTTING THE INSTANTANOUS n'''
"""MAKE SURE THAT YOU CHANGE THE PATH IN THE instant_n.clean_data fundtion if the tenisle files are somewhere else"""
files = os.listdir('J:/nxtehr/Lab Results/Tensile test/Q&P tensile test files/')
files = [f for f in files if "xlsx" in f]
print(files)
#from the files printed you can just enter the name of the sample or samples you want to plot the instantanous n for them,
#with the same format as below
samples = ['5181-1.xlsx','5189-1.xlsx']    
instant_n.instant_n_plot(samples,path)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''PLOTTING THE WELD HARDNESS CONTOUR MAP'''
#depending on whether you want to plot the preheat or no preheat weld, comment one of the df's that you do not want
#df = weld_hardness_contour.read_raw_data('preheat', sheetname = 'Report')
df = weld_hardness_contour.read_raw_data('no preheat', sheetname = 'Report')
weld_hardness_contour.weld_hardness_map(df)