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
# DB에 추가하기

query = query_latest % str(last_timestamp)
result = run_query(query)
switch_token(result)

sql = '''
INSERT INTO Pair_INFO(id, token00_id, token00_name, token00_symbol, token00_creator, token00_decimals, reserveETH, txCount, createdAtTimestamp, isChange, isScam) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
'''

for pair in result['data']['pairs']:
    if((pair['token0']['symbol'] != 'WETH') and (pair['token1']['symbol'] !='WETH' )):
      continue
    if((pair['token00']['txCount'] == 0) or (pair['token00']['txCount'] == '0') or (pair['txCount'] == '0')):
      continue
    
    try:

        id = pair['id']
        token00_id = pair['token00']['id']
        token00_name = pair['token00']['name']
        token00_symbol = pair['token00']['symbol']
        token00_creator = get_creatorAddress(id)
        token00_creator = is_proxy(token00_creator, id)  #proxy면 바꾸기
        token00_decimals = pair['token00']['decimals']
        reserveETH = pair['reserveETH']
        txCount = pair['txCount']
        createdAtTimestamp = pair['createdAtTimestamp']
        isChange = False
        isScam = False


        cursor.execute(sql,(id,token00_id,token00_name,token00_symbol,token00_creator,token00_decimals,reserveETH,txCount,createdAtTimestamp,isChange,isScam))
    except:
        print(id + 'fail')




conn.commit()
conn.close() 