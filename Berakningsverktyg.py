import pandas as pd
import math
import numpy as np

#Calculation tool for recommending products to customers at Ventim AB

#Recieve customer specifications
Kv = input()
Q = input()
p1= input()
p2 = input()
medium = input()



#Calculate potential missing values 
if medium == 'vatten':
        if Q == 0:
            Q = 1.25*Kv*math.sqrt((p2-p1)/0.996);
        
    
        if Kv == 0:
            Kv = Q*math.sqrt(0.996/(p2-p1));
            


#Acquire data on available Ventim products
fileName = 'Products_20241205_160850.xlsx'
doc = pd.read_excel(fileName, index_col=None, na_values=['NA'])

NameIdx = doc.columns.get_loc('Namn,sv-SE') 
MaterialIdx = doc.columns.get_loc('"Ventilhus (id: ArticleBodyMaterial)"')
KvIdx = doc.columns.get_loc('Kv-värde m³/h')
DNIdx = doc.columns.get_loc('DN')
MaxTempIdx = doc.columns.get_loc('Max temp')
MinTempIdx = doc.columns.get_loc('Min temp')
PriceIdx = doc.columns.get_loc('Pris (kr/st)')

data = doc.to_numpy()

dim = data.shape()
data = np.concatenate((data, np.zeros(1,dim[1])), axis = 1)

# Calculate which products match specifications

for i in range(0, len(doc)):
    if data[KvIdx][i] > Kv:
        V = 353*Q/data[DNIdx][i]
        if V < 5:
            data[dim[0]][i] = 1

# Recommend the cheapest working option 

min = 100000000
minIdx = -1

for i in dim:
    if data[PriceIdx][i] < min:
        min = data[PriceIdx][i]
        minIdx = i
        
        
print(data[NameIdx][minIdx])