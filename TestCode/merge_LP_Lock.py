import pandas as pd

datas1 = pd.read_csv('Pairs_LPLock_v2.4.csv',encoding='utf-8-sig').to_dict('records')
datas2 = pd.read_csv('Pairs_LPLock_v2.3.csv',encoding='utf-8-sig').to_dict('records')


result = []
for data in datas1:
    result.append(data)

for data in datas2:
    result.append(data)

len(result)
pd.DataFrame(result).to_csv('Pairs_v2.4.csv',encoding='utf-8-sig',index=False)
