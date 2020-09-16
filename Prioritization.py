import pandas as pd

attributedata = pd.read_excel('O:/Halogen Rosetta Stone_WIP.xlsm')
print(attributedata.columns)
reportdata = pd.read_excel('O:/Halogen Position Attribute Prioritization.xlsx', sheet_name = "Position")
GCIRreportdata=pd.read_excel('O:/Halogen Position Attribute Prioritization.xlsx', sheet_name= "GCIR Positions")
print(reportdata.columns)
print(GCIRreportdata.columns)
viewdata = pd.DataFrame()
View = []
Attribute = []
GCIRviewdata = pd.DataFrame()
GCIRView=[]
GCIRAttribute = []

class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1
                 
for index, row in reportdata.iterrows():
    report =  reportdata.iloc[index,3]
    view = reportdata.iloc[index,8]
    for index, row in attributedata.iterrows():
        placeholder = attributedata.iloc[index,7]
        placeholder = S(placeholder)
        report = S(report)
        if  placeholder in report:
            View.append(view)
            attribute=str(attributedata.iloc[index,0])
            Attribute.append(attribute)
viewdata.insert(0,"View",View)
viewdata.insert(1,"Attribute",Attribute)
print(viewdata)

for index, row in GCIRreportdata.iterrows():
    report =  GCIRreportdata.iloc[index,3]
    newview = GCIRreportdata.iloc[index,7]
    for index, row in attributedata.iterrows():
        placeholder = attributedata.iloc[index,7]
        placeholder = S(placeholder)
        report = S(report)
        if  placeholder in report:
            print(newview)
            print(report)
            GCIRView.append(report)
            attribute=str(attributedata.iloc[index,0])
            GCIRAttribute.append(attribute)
GCIRviewdata.insert(0,"View",GCIRView)
GCIRviewdata.insert(1,"Attribute",GCIRAttribute)
print(GCIRviewdata)

#viewdata.to_excel('O:/Attributes for Position Prioritization.xlsx', index=False)
GCIRviewdata.to_excel('O:/GCIR Attributes for Position Prioritization.xlsx')
