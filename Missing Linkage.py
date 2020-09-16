import pandas as pd

df = pd.DataFrame()
df = pd.read_excel('O:/AttValidation.xlsx')
print(df)

class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1
            
missing=[]
for index,row in df.iterrows():
    links = df.iloc[index,7]
    if "NYCRSA" in S(links):
        missing.append(0)
    else:
        missing.append(1)
df.insert(8,"Missing",missing)
df=df[(df['Missing'] == 1)]
df.to_excel('O:/results.xlsx', index=False)
print(df)
