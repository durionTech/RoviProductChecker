import pandas as pd
studentNames=['Lydia','Durga','Aldarin','Gideon']
s=pd.Series(studentNames)
print(s)
department=['IT','HR','Sales','Networking']
s=pd.Series(data=studentNames,index=department)
s=pd.Series(department,['I','II','III','IV'])
print(s)

df=pd.DataFrame({
    'Name':['Lydia Durga','Sam','Gideon'],
    'age':[22,33,90],
    'role':['CEO','OH','Manager']
})
print(df)
df['location']=['Bangalore','Chennai','Hyderabad']
from tabulate import tabulate
print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
