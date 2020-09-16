import pandas as pd

newdata=pd.read_excel('O:/api.xlsx')
newdata=newdata.explode('Application(s) Impacted')
newdata.to_excel('O:/api2.xlsx')
