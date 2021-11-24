import pandas as pd
import requests
import json
from math import sqrt
from tqdm import tqdm

Locker_address = [
'0x663a5c229c09b049e36dcc11a9b0d4a8eb9db214',
'0xc77aab3c6d7dab46248f3cc3033c856171878bd5',
'0xDBF72370021baBAfbCeb05aB10f99Ad275c6220A',
'0x17e00383A843A9922bCA3B280C0ADE9f8BA48449',
'0xE2fE530C047f2d85298b07D9333C05737f1435fB',
'0xC77aab3c6D7dAb46248F3CC3033C856171878BD5',
'0x1Ba00C14F9E8D1113028a14507F1394Dc9310fbD',
'0x000000000000000000000000000000000000dead' ]

def get_holders(token_id):
    repos_url = 'https://api.ethplorer.io/getTopTokenHolders/'+token_id+'?apiKey=EK-4L18F-Y2jC1b7-9qC3N&limit=100'
    response = requests.get(repos_url).text
    repos = json.loads(response)    #json 형태로 token_id에 해당하는 정보를 불러온다.
    return repos['holders']


def calc_LP_distribution(holders):
    count = 0
    for holder in holders:
        if(holder['share'] < 0.01 ):
            break
        count = count +1

    LP_avg = 100 / count
    var = 0
    for i in range(count):
        var = var + (holders[i]['share'] - LP_avg) ** 2
    
    LP_stdev = sqrt(var)

    return LP_avg,LP_stdev

def get_Lock_ratio(holders):
    for holder in holders:
        if(holder['address'] in Locker_address):
            return holder['share']
    
    return 0

def get_Creator_ratio(holders,creator_address):
    for holder in holders:
        if(holder['address'] == creator_address):
            return holder['share']
    return 0




# 지금은 DB가 없으니까 파일에서 읽고 나중에는 DB에서 추가되는 코드로 바꿔야 한다.

datas = pd.read_csv('Pairs_v2.3.csv',encoding='utf-8-sig').to_dict('records')
# datas2 = pd.read_csv('Pairs_LPLock_v2.3.csv',encoding='utf-8-sig').to_dict('records')
# len(datas2)
# id_list = []
# for data in datas2:
#     id_list.append(data['id'])
# len(id_list)

# datas3 = []
# for i in range(len(datas)):
#     if(datas[i]['id'] in id_list):
#         continue
#     else:
#         datas3.append(datas[i])
        
# len(datas3)    

# datas = datas3

result = []
error_list = []
for data in tqdm(datas,desc="Processsing rate"):
    #일단 홀더들 구하고
    creator_address = data['creator_address']
    try:
        holders = get_holders(data['id'])
        Lock_ratio = get_Lock_ratio(holders)
        LP_avg, LP_stdev = calc_LP_distribution(holders)
        LP_Creator_ratio = get_Creator_ratio(holders,creator_address)
        data['holders'] = holders
        data['Lock_ratio'] = Lock_ratio
        data['LP_avg'] = LP_avg
        data['LP_stdev'] = LP_stdev
        data['LP_Creator_ratio'] = LP_Creator_ratio
        result.append(data)
    except:
        error_list.append(data)


#에러 난 부분 무한 루프
try:
    count = 1
    while(len(error_list) > 0):
        print('%d 번째 에러 반복문 실행. 현재 남은 에러 리스트 길이 : %d' %(count,len(error_list)))
        for data in tqdm(error_list,desc="에러리스트 진행률"):
            creator_address = data['creator_address']
            try:
                holders = get_holders(data['id'])
                Lock_ratio = get_Lock_ratio(holders)
                LP_avg, LP_stdev = calc_LP_distribution(holders)
                LP_Creator_ratio = get_Creator_ratio(holders,creator_address)
                data['holders'] = holders
                data['Lock_ratio'] = Lock_ratio
                data['LP_avg'] = LP_avg
                data['LP_stdev'] = LP_stdev
                data['LP_Creator_ratio'] = LP_Creator_ratio
                result.append(data)
                del error_list[error_list.index(data)]
            except Exception as e:
                print(e)
        pd.DataFrame(result).to_csv('./drive/MyDrive/Pairs_LPLock_v2.3.csv',encoding='utf-8-sig',index=False)
        count = count + 1
 
except KeyboardInterrupt:
    print('중지')
    print('에러 리스트 반복 횟수 : {}'.format(count))

pd.DataFrame(result).to_csv('./drive/MyDrive/Pairs_LPLock_v2.3.csv',encoding='utf-8-sig',index=False)