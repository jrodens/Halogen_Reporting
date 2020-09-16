import pandas as pd
import itertools
from itertools import repeat

q1 = pd.read_excel('O:/book4.xlsx')
q1list=[]
view=[]
toexcel=pd.DataFrame()
for index,row in q1.iterrows():
    q1len = len(q1.iloc[index, 7].split(","))
    q1list.append(q1.iloc[index, 7].split(","))
    i = 0
    while  i < (q1len):
        view.append(q1.iloc[index,1])
        i=i+1
    
    #print(q1.iloc[index, 7].split(","))
q1split = list(itertools.chain.from_iterable(q1list))
s=set()
toexcel.insert(0,"View", view)
toexcel.insert(1,"Att",q1split)
toexcel.to_excel('O:/attlista.xlsx', index=False)
print("You output has been saved")
