# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 09:50:23 2018

@author: nxtehr
"""
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.ticker as ticker
import basic_functions




''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''function for plotting the results of the correlation between each two column
   for both back and front at the same time either for all thicknesses in one plot
   or for each thickness separately'''
   
def corr_f_and_b_thickness(var,path, thickness = 'all' ,fit = 'n',r2 = 0.7, plot = 'n'):
    
    #get the initial data from basic_functions
    back_results = basic_functions.front_or_back('back',path) 
    front_results = basic_functions.front_or_back('front',path)
    #if we chose a thickness other than all the thicknesses together
    if thickness != 'all':
        back_results = back_results[back_results['Thickness (mm)']== thickness].reset_index(drop = True)
        front_results = front_results[front_results['Thickness (mm)']== thickness].reset_index(drop = True)
    back_results = back_results[back_results.columns[2:]].astype(float)
    front_results = front_results[front_results.columns[2:]].astype(float)
    all_values = []
    # values_Df_both is to be used in another function
    values_Df_both = pd.DataFrame()
    #this part gets one variable as the x axis and plots all the other varibales as y axis vs the chosen x axis
    for col in var:
        idx = back_results.columns.get_loc(col)+1
        while idx <len(back_results.columns):
            var1_b = back_results[col]
            var2_b = back_results[back_results.columns[idx]]
            var1_f = front_results[col]
            var2_f = front_results[front_results.columns[idx]]
            new_df_f = pd.concat([var1_f, var2_f], axis=1).dropna(how = 'any')
            new_df_b =  pd.concat([var1_b, var2_b], axis=1).dropna(how = 'any')
            b_f_DF = pd.concat([new_df_f,new_df_b],axis=1)
            
            
            #first 2columns for front, second 2 columns for back for each two variables
            values_Df_both = pd.concat([values_Df_both,b_f_DF],axis=1)
            if (new_df_f.empty == True) | (new_df_b.empty == True):
                idx += 1
                continue
            #get the statistical data for each two correlations
            slope_f, intercept_f, r_value_f, p_value_f, std_err_f = stats.linregress(new_df_f.iloc[:-1,0],new_df_f.iloc[:-1,1])
            slope_b, intercept_b, r_value_b, p_value_b, std_err_b = stats.linregress(new_df_b.iloc[:-1,0],new_df_b.iloc[:-1,1])
            values_b = ['back',col,back_results.columns[idx],slope_b, intercept_b, r_value_b,r_value_b**2, p_value_b, std_err_b]
            values_f = ['front',col,front_results.columns[idx],slope_f, intercept_f, r_value_f,r_value_f**2, p_value_f, std_err_f]
            all_values.append(values_b)
            all_values.append(values_f)
            idx += 1
            #if the plotting was chosen as 'y' then it plots the results in one plot
            if plot == 'y':
                x_f = new_df_f.iloc[:-1,0]
                y_f = new_df_f.iloc[:-1,1]
                x_b = new_df_b.iloc[:-1,0]
                y_b = new_df_b.iloc[:-1,1]
                f, ax = plt.subplots(figsize=(7,7), dpi=200)
                ax.plot(x_f,y_f, 'o', label='front')
                ax.plot(x_b,y_b, 'o', color ='#ff7f0e', label='back')
                ax.plot(new_df_b.iloc[-1,0],new_df_b.iloc[-1,1], 'o', c = '#89460C' , label = 'temper_b')   
                ax.plot(new_df_f.iloc[-1,0],new_df_f.iloc[-1,1], 'o', c = '#124365' , label = 'temper_f')
                #if it was chosen to have the fitted line plotted as well        
                if fit == 'y' :
                    if (r_value_f**2) >r2:
                        ax.plot(x_f, intercept_f + slope_f*x_f, '#1f77b4',linewidth=1,alpha = 0.6,label='fitted line: y={:.2f}x+{:.2f}'.format(slope_f,intercept_f))
                        ax.plot([], [], ' ', label='$R^2$ = {:.2f}'.format(r_value_f**2))
                    if (r_value_b**2) >r2:
                        ax.plot(x_b, intercept_b + slope_b*x_b, '#ff7f0e',linewidth=1,alpha = 0.6,label='fitted line: y={:.2f}x+{:.2f}'.format(slope_b,intercept_b))
                        ax.plot([], [], ' ', label='$R^2$ = {:.2f}'.format(r_value_b**2))
                #add legend and labels and title
                ax.legend()
                ax.set_xlabel(new_df_b.columns[0])
                ax.set_ylabel(new_df_b.columns[1])
                ax.set_title('{} vs. {}'.format(new_df_b.columns[1],new_df_b.columns[0]))
                
    #this DF will be passed to the other functions            
    values_Df = pd.DataFrame(all_values, columns = ['location','var1','var2','slope','intercept','r_value',\
                                                    'r^2 value','p_value','std-err'])
     
    return (values_Df,values_Df_both)



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''plot each two variables for both f and b and all thicknesses in subplots'''

def two_var_fb_subplot(xaxis,yaxis,path, fit = 'n', r2 = 0.7,temper = 'n'):
    fig, ax = plt.subplots(1,5, figsize=(15, 6), sharex=True, sharey = True)
    for t,j in zip([6,10,12.7,16,19],range(0,5)):
        column_names = list(basic_functions.front_or_back('back',path).columns[2:])
        values_Df,values_Df_both = corr_f_and_b_thickness(var= column_names,path = path,thickness = t)
        all_indexes = pd.DataFrame(values_Df_both.columns, columns = ['var'])
        idx = []
        for i in range (0,len(all_indexes),4):
            idx.append(i)
            idx.append(i+1)
        indexes = all_indexes.iloc[idx]  
        possible_x = indexes.index[indexes['var'] == xaxis].tolist()
        all_y = []
        for x in possible_x: 
            if x+1 in indexes.index.values.tolist() and indexes['var'].loc[x+1] == yaxis:
                all_y.append(x)
                i = x
        if len(all_y) == 0:
            print('The y variable you chose is designed to be on the xaxis.\ntry to exchange  x and y')
            plt.close(fig)
            break

        if t != 10:
            x_f = values_Df_both.iloc[:,i]
            y_f = values_Df_both.iloc[:,i+1]
            x_b = values_Df_both.iloc[:,i+2]           
            y_b = values_Df_both.iloc[:,i+3]
            slope_f, intercept_f, r_value_f, p_value_f, std_err_f = stats.linregress(x_f,y_f)
            slope_b, intercept_b, r_value_b, p_value_b, std_err_b = stats.linregress(x_b,y_b)
            ax = ax.ravel()
            ax[j].plot(x_f,y_f, 'o', label='front')
            ax[j].plot(x_b,y_b, 'o', color ='#ff7f0e', label='back')
        if t == 10 and temper == 'y':
            x_f = values_Df_both.iloc[:-1,i]
            y_f = values_Df_both.iloc[:-1,i+1]
            x_b = values_Df_both.iloc[:-1,i+2]           
            y_b = values_Df_both.iloc[:-1,i+3]
            slope_f, intercept_f, r_value_f, p_value_f, std_err_f = stats.linregress(x_f,y_f)
            slope_b, intercept_b, r_value_b, p_value_b, std_err_b = stats.linregress(x_b,y_b)
            ax = ax.ravel()
            ax[j].plot(x_f,y_f, 'o', label='front')
            ax[j].plot(x_b,y_b, 'o', color ='#ff7f0e', label='back')
            ax[j].plot(values_Df_both.iloc[-1,i],values_Df_both.iloc[-1,i+1], 'o', c = '#124365' , label = 'temper_f')
            ax[j].plot(values_Df_both.iloc[-1,i+2],values_Df_both.iloc[-1,i+3], 'o', c = '#89460C' , label = 'temper_b')
              
        elif t == 10 and temper =='n':
            x_f = values_Df_both.iloc[:-1,i]
            y_f = values_Df_both.iloc[:-1,i+1]
            x_b = values_Df_both.iloc[:-1,i+2]           
            y_b = values_Df_both.iloc[:-1,i+3]
            slope_f, intercept_f, r_value_f, p_value_f, std_err_f = stats.linregress(x_f,y_f)
            slope_b, intercept_b, r_value_b, p_value_b, std_err_b = stats.linregress(x_b,y_b)
            ax = ax.ravel()
            ax[j].plot(x_f,y_f, 'o', label='front')
            ax[j].plot(x_b,y_b, 'o', color ='#ff7f0e', label='back')
            
              
        if (r_value_f**2) > r2 and fit =='y':
            ax[j].plot(x_f, intercept_f + slope_f*x_f, '#1f77b4',linewidth=1,alpha = 0.6, label = '')
        if (r_value_b**2) > r2 and fit =='y':
            ax[j].plot(x_b, intercept_b + slope_b*x_b, '#ff7f0e',linewidth=1,alpha = 0.6, label = '')
        ax[j].set_title('{} mm'.format(t))
        plt.suptitle('{} vs. {}'.format(y_f.name,x_f.name),  fontsize=20,x = 0.5, y = 0.65)
        
        for axis in ax.flat:
            axis.tick_params(labelsize=11)
            axis.label_outer()
        
        #setting only one xlabel for the subplots 1,5
        ax[2].set_xlabel(xlabel=x_f.name, fontsize = 12)
        ax[0].set_ylabel(ylabel=y_f.name, fontsize = 12)
                
    plt.subplots_adjust(left=0.070, right=0.96, top=0.555, bottom=0.105,wspace = 0.080,hspace =0.245 )   
    

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def plot_QT_PT(variables, path):

    front = basic_functions.front_or_back('front',path)
    back = basic_functions.front_or_back('back',path)
    
    m = front[front['Thickness (mm)']== 6]['partitioning temperature °C'].tolist()
    m = [round(x,2) for x in m if pd.notnull(x)]
    m = list(sorted(set(m)))
    mapping = {m[0]:"s",m[1]:"v",m[2]:"o",m[3]:"^",m[4]:"P",m[5]:"*",m[6]:"D"}
    
    mapping_cf = {m[0]:"#FFB2B2",m[1]:"#D18681",m[2]:"#CC4C4C",m[3]:"#CC0000",m[4]:"#990000",m[5]:"#4D0808",\
                  m[6]:"#330000"}
    mapping_cb = {m[0]:"#B2B2FF",m[1]:"#7F7FFF",m[2]:"#6666FF",m[3]:"#3333FF",m[4]:"#0000E5",m[5]:"#00007F",\
                  m[6]:"#000033"}
    
    for cl in variables:
        fig, ax = plt.subplots(1,5, figsize=(15, 6),sharex=True, sharey = True)
        for t,j in zip([6,10,12.7,16,19],range(0,5)):
            PT = front[front['Thickness (mm)']== t]['partitioning temperature °C'].tolist()
            PT = [x for x in PT if pd.notnull(x)]
            PT_unique = set(PT)
            ax = ax.ravel()
            for temp in sorted(PT_unique):
                x_f = front[front['Thickness (mm)']== t][front['partitioning temperature °C']== temp][front['quenching temperature °C']> 50]['quenching temperature °C']
                y_f = front[front['Thickness (mm)']== t][front['partitioning temperature °C']== temp][front['quenching temperature °C']> 50][cl]
                x_b = back[back['Thickness (mm)']== t][back['partitioning temperature °C']== temp][front['quenching temperature °C']> 50]['quenching temperature °C']
                y_b = back[back['Thickness (mm)']== t][back['partitioning temperature °C']== temp][front['quenching temperature °C']> 50][cl]
                ax[j].plot(x_f,y_f,'o',label=round(temp,2),color =  mapping_cf[round(temp,2)],alpha = 0.8, marker = mapping[round(temp,2)])
                ax[j].plot(x_b,y_b,'o',label=round(temp,2),color = mapping_cb[round(temp,2)],alpha = 0.5, marker = mapping[round(temp,2)])
                ax[j].set_title('{} mm'.format(t), fontsize = 15)
                plt.suptitle('{} vs. {}'.format(cl,'quenching temperature °C'),fontsize=20,x = 0.5, y = 0.68)
#            if cl == 'retained austenite %' and t == 6:
#                xf = front[front['Thickness (mm)']== t]['quenching temperature °C']
#                yf = front[front['Thickness (mm)']== t][cl]
#                xb = back[back['Thickness (mm)']== t]['quenching temperature °C']
#                yb = back[back['Thickness (mm)']== t][cl]
#                pf = np.poly1d(np.polyfit(xf, yf, 3)) 
#                pb = np.poly1d(np.polyfit(xb, yb, 3)) 
#                xf_new = np.linspace(120,240, 100)
#                xb_new = np.linspace(xb.min(), xb.max(), 100)
#                yf_new = pf(xf_new)
#                yb_new = pb(xb_new)
#                ax[j].plot(xf_new,yf_new,'r--',alpha = 0.4)
#                ax[j].plot(xb_new,yb_new,'b--',alpha = 0.4)
        for axis in ax.flat:
                axis.tick_params(labelsize=11)  
                axis.set_xlim(115,240)
                axis.label_outer()
        
        #setting only one xlabel for the subplots 1,5
        ax[2].set_xlabel(xlabel='quenching temperature °C', fontsize = 12)
        ax[0].set_ylabel(ylabel=cl, fontsize = 12)
    
        def is_inlist(handle, handles):
            for h in handles:
                if h.get_color() == handle.get_color():
                    return True
            return False
        scatters_f=[]
        scatters_b = []
        labels_f =[]
        labels_b = ['','','','','','','']
        for i in range(0,5):
            h, l = ax[i].get_legend_handles_labels()
            for hi, li, n in zip(h,l,range(1,15)):
                if not is_inlist(hi, scatters_f) and (n%2 != 0):
                    scatters_f.append(hi)
                    labels_f.append(int(float((li))))
                elif not is_inlist(hi, scatters_b) and  (n%2 == 0):
                    scatters_b.append(hi)
        
                    
        first_legend = fig.legend(handles=scatters_f,labels=labels_f,loc =(0.8,0.62), fontsize = 12, \
                                  title = 'partitioning Temperature °C \n\n             front')
        fig.legend(handles=scatters_b, labels=labels_b, loc=(0.8,0.62), fontsize = 12,frameon=False,title = 'back') 
        
        plt.subplots_adjust(left=0.070, right=0.96, top=0.555, bottom=0.105,wspace = 0.080,hspace =0.245 )   

        

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def plot_PT_12mm(variable,path,legend_loc = 2):
    front = basic_functions.front_or_back('front',path)
    back = basic_functions.front_or_back('back',path)
    x_f = front[front['Thickness (mm)'] == 12.7][front['quenching temperature °C']< 210]['partitioning temperature °C']
    y_f = front[front['Thickness (mm)'] == 12.7][front['quenching temperature °C']< 210][variable]
    x_b = back[back['Thickness (mm)'] == 12.7][front['quenching temperature °C']< 210]['partitioning temperature °C']
    y_b = back[back['Thickness (mm)'] == 12.7][front['quenching temperature °C']< 210][variable]
    text_f = front[front['Thickness (mm)'] == 12.7][front['quenching temperature °C']< 210]['partitioning time (min)']
    text_b = back[back['Thickness (mm)'] == 12.7][back['quenching temperature °C']< 210]['partitioning time (min)']
    f, ax = plt.subplots(figsize=(7,7), dpi=200)
    ax.plot(x_f,y_f, 'o', label='front',alpha = 0.7)
    
    ax.plot(x_b,y_b, 'o', color ='#ff7f0e', label='back',alpha = 0.7)
    ax.set_xlim(260,340)
    ax.legend(loc =legend_loc)
    ax.set_xlabel('partitioning temperature °C')
    ax.set_ylabel(variable)
    
    for i,j,text in zip(list(x_f),list(y_f),list(text_f)):
        ax.text(i + 1,j-0.001,s = str(int(text))+ 'min',  fontsize = 8)
        
    for i,j,text in zip(list(x_b),list(y_b),list(text_b)):
        ax.text(i + 1,j-0.001,s = str(int(text))+ 'min',  fontsize = 8)
    plt.show()



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#list of all the variables that we want to have the plot for

def plot_3D(variables,path):
    cmap = colors.ListedColormap(['#58FF33', '#336EFF','#FF3333'])
    bounds=[15,25,35,45]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    for cl in variables: 
    #finding the min and max of each variable for using in z-axis
        var_min = basic_functions.front_or_back('back',path)[cl].min()
        if basic_functions.front_or_back('front',path)[cl].min() <var_min:
            var_min = basic_functions.front_or_back('front',path)[cl].min()
        var_max = basic_functions.front_or_back('back',path)[cl].max()
        if basic_functions.front_or_back('front',path)[cl].max() >var_max:
            var_max = basic_functions.front_or_back('front',path)[cl].max()
    #plotting the figure for each varible or column        
        fig = plt.figure(figsize=(16,10))
        
        for t,j in zip([19,16,12.7,10,6],reversed(range(1,6))):  #the subplots are being plotted in a reverse order because\
            #the 20min partitioning time is not applicable for the thicker samples.
            back_results = basic_functions.front_or_back('back',path)[basic_functions.front_or_back('back',path)['Thickness (mm)'] == t] 
            front_results = basic_functions.front_or_back('front',path)[basic_functions.front_or_back('front',path)['Thickness (mm)'] == t] 
            x_axis_f = front_results[front_results['quenching temperature °C']>50]['quenching temperature °C']
            y_axis_f = front_results[front_results['quenching temperature °C']>50]['partitioning temperature °C']
            color_axis_f = front_results[front_results['quenching temperature °C']>50]['partitioning time (min)']
            z_axis_f = front_results[front_results['quenching temperature °C']>50][cl]
            x_axis_b = back_results[front_results['quenching temperature °C']>50]['quenching temperature °C']
            y_axis_b = back_results[front_results['quenching temperature °C']>50]['partitioning temperature °C']
            color_axis_b = back_results[front_results['quenching temperature °C']>50]['partitioning time (min)']
            z_axis_b = back_results[front_results['quenching temperature °C']>50][cl]
        
            #print(z_axis_f)
            
            ax = fig.add_subplot(2,3,j, projection='3d')
            ax.set_xlabel('quenching temperature °C',fontsize = 12)
            ax.set_ylabel('partitioning temperature °C',fontsize = 12)
            ax.set_zlabel(cl, fontsize = 12)
            ax.set_xlim(100,240)
            ax.set_ylim(200,400)
            ax.yaxis.set_major_locator(ticker.MultipleLocator(50))
            plt.gca().invert_yaxis()
            
            scatter_plot_f = ax.scatter(x_axis_f, y_axis_f, z_axis_f, s=100,c=color_axis_f, cmap=cmap, norm=norm, \
                                       alpha = 0.8)
            scatter_plot_b = ax.scatter(x_axis_b, y_axis_b, z_axis_b, s=100,c=color_axis_b, cmap=cmap, norm=norm, \
                                    edgecolor='black', hatch = '////', alpha = 0.8)
            
            ax.set_title('{} mm'.format(t),x = 0.7, y=0.95, fontsize = 15)
            ax.set_zlim(var_min-0.1*(var_min),var_max+0.1*(var_max))
            
            
            # position of colorbar, where arg is [left, bottom, width, height]
        cax_f = fig.add_axes([0.8,0.15, 0.01,0.2])
        cbar_f = plt.colorbar(scatter_plot_f ,cmap=cmap, norm=norm, boundaries=bounds, ticks=[20, 30, 40],
                              shrink=0.5, aspect=15, cax = cax_f)
        cbar_f.ax.set_yticklabels([]) 
        cbar_f.set_label('            partitioning time (min)\n\n  front', labelpad=-25, y=1.3, rotation=0,fontsize = 12)
        cax_b = fig.add_axes([0.82,0.15, 0.01,0.2])
        cbar_b = plt.colorbar(scatter_plot_b ,cmap=cmap, norm=norm, boundaries=bounds, ticks=[20, 30, 40],
                              shrink=0.5, aspect=15, cax = cax_b)
        cbar_b.ax.set_yticklabels(['20', '30', '45']) 
        cbar_b.set_label('\n\n   back', labelpad=-25, y=1.3, rotation=0, fontsize = 12)
        fig.patches.extend([plt.Rectangle((0.82,0.15),0.01,0.2,fill=False, hatch = '////', alpha=0.5, zorder=1000,
                                          transform=fig.transFigure, figure=fig)])
        plt.suptitle('{}'.format(cl),fontsize=20)
        plt.tight_layout()
        plt.tight_layout(pad=4, w_pad=0.5, h_pad=1.0)
    
        
        plt.show()
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    

    


        
        
