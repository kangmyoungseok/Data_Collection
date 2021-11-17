import pandas as pd

datas_creator = pd.read_csv('Creator_list.csv',encoding = 'utf-8-sig').to_dict('records')
datas = pd.read_csv('Pairs_v2.1.csv',encoding = 'utf-8-sig').to_dict('records')

for data in datas:
    id = data['id']
    for data_creator in datas_creator:
        if(data_creator['id'] == id):
            data['creator_address'] = data_creator['token00_creator_address']
            break
    

for data in datas:
    try:
        data['creator_address'] 
    except:
        data['creator_address'] = ''   


pd.DataFrame(datas).to_csv('Pairs_v2.2.csv',encoding = 'utf-8-sig',index=False)

error_list = []
for data in datas:
    if(data['creator_address'] == ''):
        error_list.append(data)

len(error_list)

pd.DataFrame(error_list).to_csv('error_list.csv',encoding = 'utf-8-sig',index = False)

