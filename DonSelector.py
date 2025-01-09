import math
import numpy as np
import openpyxl
import pandas as pd
from numpy.dtypes import StringDType

def chooseDon(fileName, indexes,isUsed, donChoice):

    doc = pd.read_excel(fileName, index_col=None, na_values=['NA'])
    data = doc.to_numpy()
    dim = data.shape
    
    for i in range(1,dim[0]):
        for j in range(1,dim[1]):
            if pd.isnull(data[i][j]):
                data[i][j] = 0
    k = 0
    active = False
    for i in range(1,dim[0]-1):
        if active and i < indexes[k+1]:
            if donChoice == data[i,doc.columns.get_loc('Manövrering')]:
                print(data[i][doc.columns.get_loc('Artikelbeskrivning')] + ' ' + data[i][doc.columns.get_loc('Namn,sv-SE')])
                k+=1
                active = False
        if i == indexes[k+1]:
            if active:
                print('Önskat don kunde ej hittas för ' + data[int(indexes[k])][doc.columns.get_loc('Artikelbeskrivning')])
            if k < len(indexes)-1:
                k+=1
            if isUsed[k] == 0:
                active = False
        if i == indexes[k] and isUsed[k] == 1:
            active = True
        
           
            