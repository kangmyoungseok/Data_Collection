import pymysql 
import pandas as pd
from mylib import *

## DB가 있는 상태에서 업데이트 하는 코드
## DB에는 위에 코드로 Pairs_v2.3.csv 파일의 내용이 들어가 있어야 한다.

conn = pymysql.connect(host='localhost', user='root', password='rkdaudtjr1!', db='bobai_web', charset='utf8mb4') 
cursor = conn.cursor()

sql = "select CreatedAtTimestamp from pair_info order by createdAtTimestamp desc limit 0,1"
cursor.execute(sql)
result = cursor.fetchall()
last_timestamp = result[0][0]
last_timestamp

# TheGraph에서 일반적인 정보를 먼저 불러오기. 바로 뒤에서 Creator 찾는 코드 돌려야 함
datas = []
query = query_latest % str(last_timestamp)
result = run_query(query)
switch_token(result)
for pair in result['data']['pairs']:
    if((pair['token0']['symbol'] != 'WETH') and (pair['token1']['symbol'] !='WETH' )):
      continue
    if((pair['token00']['txCount'] == 0) or (pair['token00']['txCount'] == '0') or (pair['txCount'] == '0')):
      continue
    
    try:
        pair_id = pair['id']
        token_id = pair['token00']['id']
        name = pair['token00']['name']
        symbol = pair['token00']['symbol']
        createdAtTimestamp = pair['createdAtTimestamp']
        decimals = pair['token00']['decimals']
        creator_address = get_creatorAddress(token_id)
        datas.append({'id':pair_id, 'token_id' : token_id, 'name' : name, 'symbol':symbol, 'createdAtTimestamp' : createdAtTimestamp,'decimals' : decimals,'creator_address' : creator_address})
    except:
        print(pair_id + 'faile')

#datas에 새로 추가된 데이터들 다 넣어 놨으니까 DB에 넣기만 하면 댄다.

#DB에 추가하기
sql = '''
INSERT INTO Pair_INFO(PairId, TokenId, Name, Symbol, Creator, CreatedAtTimestamp, IsScam, Decimals) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
'''

for data in datas:
    Pair_id = data['id']
    Token_id = data['token_id']
    Name = data['name']
    Symbol = data['symbol']
    CreatedAtTimestamp = data['createdAtTimestamp']
    Decimals = data['decimals']
    IsScam = False
    Creator = data['creator_address']
    cursor.execute(sql,(Pair_id,Token_id,Name,Symbol,Creator,CreatedAtTimestamp,IsScam,Decimals))
conn.commit()
conn.close() 