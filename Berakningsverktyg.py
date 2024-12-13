import openpyxl
import pandas as pd
import math
import numpy as np
import Ångtabell as tab
from numpy.dtypes import StringDType

#Calculation tool for recommending products to customers at Ventim AB

def maxSpeed(category,med):
    if med == 'vatten':
        return 5
    if med == 'ånga':
        if category == 'Vridspjällventiler':
            return 70
        if category == 'Styrda reglerventiler':
            return 150
        if category == 'Självverkande reglerventiler':
            return 250
    
    else:
        print('Ogiltigt medium')
        return 0

def calcSpeed(DN,med):
    if med == 'vatten':
        return 353*Q/(numData[i][1]**2)
    
    if med == 'ånga':
        b = tab.getDens(p2)
        Vdrift = Q*b*(T+273)/(p2*273)
        return 353*Vdrift/(DN**2)
    
    else:
        print('Ogiltigt medium')
        return 0

#Recieve customer specifications
print('Kv:, 0 om okänd')
Kv = float(input())
print('Q:, 0 om okänd')
Q = float(input())
print('P1:')
p1= float(input())
print('P2:')
p2 = float(input())
print('Medium:')
medium = input()
print('Temperatur på medium')
T = float(input())
print('Önskat material:')
material = input()
#gjutjärn JL1040


#Calculate potential missing values 
if medium == 'vatten':
    if Q == 0:
        Q = 1.25*Kv*math.sqrt((abs(p2-p1))/0.996);
    
    if Kv == 0:
        Kv = Q*math.sqrt(0.996/abs(p2-p1));
    
if medium == 'ånga':
    if Q == 0:
        Q = Kv*math.sqrt(abs(p2-p1)*abs(p1+p2))/40.7;
        
    if Kv == 0:
        Kv = 40.7*Q*math.sqrt(abs(p2-p1)*abs(p1+p2));
    
        
#Acquire data on available Ventim products
fileName = 'Products_20241205_160850.xlsx'
doc = pd.read_excel(fileName, index_col=None, na_values=['NA'])

NameIdx = doc.columns.get_loc('Artikelbeskrivning') 
MaterialIdx = doc.columns.get_loc('"Ventilhus (id: ArticleBodyMaterial)"')
KvIdx = doc.columns.get_loc('Kv-värde m³/h')
DNIdx = doc.columns.get_loc('DN')
MaxTempIdx = doc.columns.get_loc('Max temp')
MinTempIdx = doc.columns.get_loc('Min temp')
PriceIdx = doc.columns.get_loc('Pris (kr/st)')
CategoryIdx = doc.columns.get_loc('Produkttyp,sv-SE')
AvailableIdx = doc.columns.get_loc('Publicerad i Ventim')

data = doc.to_numpy()
dim = data.shape

for i in range(1,dim[0]):
    for j in range(1,dim[1]):
        if pd.isnull(data[i][j]):
            data[i][j] = 0

#Separate numbers and strings into different arrays
numData = np.empty((dim[0],5),dtype=float)
for i in range(0,dim[0]-1):
    numData[i][0] = float(data[i][KvIdx])
for i in range(0,dim[0]-1):
    numData[i][1] = float(data[i][DNIdx])    
for i in range(0,dim[0]-1):
    numData[i][2] = float(data[i][MaxTempIdx])
for i in range(0,dim[0]-1):
    numData[i][3] = float(data[i][MinTempIdx])
for i in range(0,dim[0]-1):
    numData[i][4] = float(data[i][PriceIdx])
    
strData = np.empty((dim[0],4),dtype=StringDType())
for i in range(0,dim[0]-1):
    strData[i][0] = data[i][NameIdx]
for i in range(0,dim[0]-1):
    strData[i][1] = data[i][MaterialIdx]
for i in range(0,dim[0]-1):
    strData[i][2] = data[i][CategoryIdx]
for i in range(0,dim[0]-1):
    strData[i][3] = data[i][AvailableIdx]

#The sixth column is 1 if the product fulfills the requirement
numData = np.concatenate((numData, np.zeros((dim[0],1),dtype=float)),axis=1)

# Calculate which products match specifications
for i in range(0, dim[0]):
    #Kv, speed and correct material
    if numData[i][0] > Kv: 
        if calcSpeed(numData[i][1],medium) < maxSpeed(strData[i][2],medium) and material == strData[i][1]:
            # Temperature and availability
            if T < numData[i][2] and T > numData[i][3] and strData[i][3] == 'ja':
                #Take only the smallest variant of each product
                noBetter = True
                for j in range(0,i):
                    if numData[j][5] == 1:
                        if strData[i][1] == strData[j][1] and numData[i][1] > numData[j][1]:
                            noBetter = False
                if noBetter:
                    numData[i][5] = 1

# Recommend the cheapest working option 

#min = 100000000
#minIdx = -1

#for i in dim:
#    if data[PriceIdx][i] < min:
#        min = data[PriceIdx][i]
#        minIdx = i
        
        
for i in range(0, dim[0]-1):
    if numData[i][5] == 1:
        print(strData[i][0])
        
        
