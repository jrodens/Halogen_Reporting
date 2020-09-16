import pandas as pd
import itertools

q1 = pd.read_excel('O:/book3.xlsx')
q1list=[]
view=[]
toexcel=pd.DataFrame()
for index,row in q1.iterrows():
    q1list.append(q1.iloc[index, 8].split(","))
    view.append(q1.iloc[index,0])
    print(q1.iloc[index, 8].split(","))
q1split = list(itertools.chain.from_iterable(q1list))
s=set()
toexcel.insert(0,"View", view)
toexcel.insert(1,"Att",q1split)
toexcel.to_excel('O:/attlistb.xlsx', index=False)
