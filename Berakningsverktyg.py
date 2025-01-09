import openpyxl
import pandas as pd
import math
import numpy as np
import Ångtabell as tab
import DonSelector as ds
from numpy.dtypes import StringDType

#Calculation tool for recommending products to customers at Ventim AB

def maxSpeed(category,med):
    if med == 'vatten':
        return 4.5
    if med == 'ånga' or med == 'luft':
        if category == 'Vridspjällventiler' or 'Mjuktätande vridspjällventiler':
            return 70
        if category == 'Styrda reglerventiler':
            return 150
        if category == 'Självverkande reglerventiler':
            return 250
        else:
            print('Ny kategori, uppdatering krävs')
            return 0
    else:
        print('Ogiltigt medium')
        return 0

def calcSpeed(DN,med):
    if med == 'vatten':
        return 353*Q/(DN**2)
    
    if med == 'ånga':
        b = tab.getSteamDens(p2)
        Vdrift = Q*b*(T+273)/(p2*273)
        return 353*Vdrift/(DN**2)
    
    if med == 'luft':
        b = tab.getAirDens(p2,T)
        Vdrift = Q*b*(T+273)/(p2*273)
        return 353*Vdrift/(DN**2)
    
    else:
        print('Ogiltigt medium')
        return 0

#Recieve customer specifications
#print('Kv:, 0 om okänd')
#Kv = float(input())
print('Q:')
Q = float(input())
print('P1:')
p1= float(input())
print('P2:')
p2 = float(input())
print('Medium:')
medium = input()
#vatten
#ånga
#luft
#övrig

print('Temperatur på medium')
T = float(input())
print('Önskat material:')
material = input()
#gjutjärn JL1040
#segjärn JS1030
#ingen preferens
print('Önskat don')
don = input()
#vet ej
#elmanöverdon


#Special cases when qualified employee should make the decision
if p2/p1 < 1/2:
    print('Risk för cavitation, kontakta kunnig på Ventim')
    exit(0)
if medium == 'övrig':
    print('Detta program stödjer inte andra medium, kontakta kunnig på Ventim')
    exit(0)
if medium == 'ånga':
    Pvap = tab.VapourizationPressure(T)
    if Pvap < p2:
        print('Risk för flashing,kontakta kunnig på Ventim')
        exit(0)

    
#Calculate potential missing values 
if medium == 'vatten':
    #if Q == 0:
    #    Q = 1.25*Kv*math.sqrt((abs(p2-p1))/0.996);
    
    #if Kv == 0:
        Kv = Q*math.sqrt(0.996/abs(p2-p1));
    
if medium == 'ånga' or medium == 'luft':
    #if Q == 0:
    #    Q = Kv*math.sqrt(abs(p2-p1)*abs(p1+p2))/40.7;
        
    #if Kv == 0:
        Kv = 40.7*Q*math.sqrt(abs(p2-p1)*abs(p1+p2));
    
        
#Acquire data on available Ventim products
fileName = 'Products_20241205_160850.xlsx'
doc = pd.read_excel(fileName, index_col=None, na_values=['NA'])

ArtNbrIdx = doc.columns.get_loc('Artikelnummer')
Name1Idx = doc.columns.get_loc('Artikelbeskrivning')
Name2Idx = doc.columns.get_loc('Namn,sv-SE')
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
numData = np.zeros((dim[0],7),dtype=float)
strData = np.zeros((dim[0],5),dtype=StringDType())
k = 0
for i in range(0,dim[0]-1):
    if len(data[i][ArtNbrIdx]) == 6:
        #Kv-value
        numData[k][0] = float(data[i][KvIdx])
        #Dn-value
        numData[k][1] = float(data[i][DNIdx])    
        #Max temperature
        numData[k][2] = float(data[i][MaxTempIdx])
        #Min temperature
        numData[k][3] = float(data[i][MinTempIdx])
        #Prize
        numData[k][4] = float(data[i][PriceIdx])
        #The sixth column represents whether the product is to be recommended
        #Original index
        numData[k][6] = float(i)
        
        #Name, desciptive
        strData[k][0] = data[i][Name1Idx]
        #Name, classification
        strData[k][1] = data[i][Name2Idx]
        #Material of the article
        strData[k][2] = data[i][MaterialIdx]
        #Product category, data must be improved
        strData[k][3] = data[i][CategoryIdx]
        #Product availabilty
        strData[k][4] = data[i][AvailableIdx]
        
        k += 1
        
numData = numData[~np.all(numData == 0, axis=1)]
strData = strData[~np.all(strData == 0, axis=1)]

dim = numData.shape

# Calculate which products match specifications
for i in range(0, dim[0]):
    #Kv and speed
    if numData[i][0] > Kv and calcSpeed(numData[i][1],medium) < maxSpeed(strData[i][3],medium):
        #Correct material
        if material == strData[i][2] or material == 'ingen preferens':
            #Temperature and availability
            if T < numData[i][2] and T > numData[i][3] and strData[i][4] == 'Ja':
                #Take only the smallest variant of each product
                noBetter = True
                for j in range(0,i):
                    if numData[j][5] == 1:
                        if strData[i][1] == strData[j][1] and numData[i][1] > numData[j][1]:
                            noBetter = False
                if noBetter:
                    numData[i][5] = 1

# Recommend the cheapest working options

numAlts = 0
for i in range(0,dim[0]-1):
    if numData[i][5] == 1:
        numAlts += 1

if numAlts == 0:
    print('Inga artiklar uppfyllde kraven, eller så har felaktig data matats in')
    exit(0)
    

while numAlts > 3:
    maxPrize = 0
    maxIdx = -1
    for i in range(0, dim[0]-1):
        if numData[i][4] > maxPrize and numData[i][5] == 1:
            maxPrize = numData[i][4]
            maxIdx = i
    
    numData[maxIdx][5] = 0
    numAlts -= 1

        
#Print options
if don == 'vet ej':        
    for i in range(0, dim[0]-1):
        if numData[i][5] == 1:
            print(strData[i][1] +' '+ strData[i][0])
else:
    ds.chooseDon(fileName,numData[:,6],numData[:,5],don)
        
        
