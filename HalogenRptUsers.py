import pandas as pd


ViewList = pd.read_excel('O:/viewlista.xlsx', sheet_name= 'Report List')
buu = pd.read_excel('O:/viewlista.xlsx', sheet_name = 'Raw BO Usage')

#print(ViewList)
#print(buu)


newdata = pd.merge(ViewList,buu,how = 'left')

print(newdata)
newdata.replace('', "N/A", inplace=True)
newdata.to_excel('O:/newdata.xlsx', index=False)
