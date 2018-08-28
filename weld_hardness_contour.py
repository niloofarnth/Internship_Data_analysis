# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 10:42:31 2018

@author: nxtehr
"""

#plotting the contour map for hardness of welds
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap




def read_raw_data(condition, sheetname = 'Report'):
    if condition =='no preheat':
        path = 'J:/nxtehr/Lab Results/Microhardness/Q&P weld/No preheat sample/No preheat weld hardness map.xlsx'
    if condition == 'preheat':
        path = 'J:/nxtehr/Lab Results/Microhardness/Q&P weld/Preheat sample/preheat(345)_weld hardness map.xlsx'
    xls = pd.ExcelFile(path)
    raw_data = pd.read_excel(xls, sheetname)
    
    raw_data.columns = raw_data.iloc[15]
    raw_data = raw_data.iloc[16:916,:6]
    raw_data.reset_index(drop = True, inplace = True)
    x_list = []
    y_list = []
    hardness_list = []
    number_list = []
    x = -300
    number = 0
    i = 1
    while i <31 and number <900:
        number += 1
        if i == 1:
            x += 300
            y = 9000
        if i == 30:
            i = 0
        y -= 300 
        hardness = raw_data['Hardness'][number-1]
        x_list.append(x)
        y_list.append(y)
        hardness_list.append(hardness)
        number_list.append(number)
        df = pd.DataFrame({'number':number_list,'x':x_list,'y':y_list,'hardness':hardness_list})
        i += 1
              
    return df



def weld_hardness_map(df):
    f, ax = plt.subplots(figsize=(7,7), dpi=200)
    # Make data
    x = np.linspace(0,8700/1000,30)
    y = np.linspace(8700/1000,0,30)
    #make a meshgrid of X and Y
    X,Y= np.meshgrid(x,y)
    #get the initial z
    z = df['hardness']
    #make a list of Z every 30 data points to make a g2D grid like Z
    n = 30
    z_new = [z[i:i+n] for i in range(0, len(z), n)]
    #make a 2D array 
    Z = np.array(z_new).transpose()
    #replacing all the values higher than 650(possibly outliers) with 650 
    Z[Z > 650] = 649
    # Plot the surface.
    cmap = cm.magma_r#pink_r ##
    bounds=np.linspace(190,710,100)
    norm = colors.BoundaryNorm(bounds, cmap.N)
    levels = np.linspace(200,650,10).astype(int)
    surf = ax.contourf(X, Y, Z, antialiased=False, cmap = cmap, norm= norm,levels = levels, vmin =200, vmax =650)
    clb= f.colorbar(surf, extend='both',shrink=0.8, aspect=10)
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')
    clb.set_label('hardness (HV)', labelpad=15, y=0.5, rotation=-90, fontsize = 10)
    ax.set_title('no pre-heat weld')
    plt.show()
