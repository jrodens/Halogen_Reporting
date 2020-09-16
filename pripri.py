import pandas as pd

HalPri = pd.read_excel('O:/HalPri.xlsx')
Attrs = pd.read_excel('O:/attr.xlsx')

HalPri.explode('Link')
print(HalPri)

Link=[]
Story=[]
for index, row in Attrs.iterrows():
    attribute = Attrs.iloc[index,1]
    for index, row in HalPri.iterrows():
        if attribute in HalPri.iloc[index,2]:
            Link.append(Attrs.iloc[index,0])
            Story.append(HalPri.iloc[index,1])

Priotization = pd.DataFrame()
Priotization.insert(0,"Story", Story)
Priotization.insert(1,"Link", Link)

Priotization.to_excel('O:/Prioritization4Halogen.xlsx')
