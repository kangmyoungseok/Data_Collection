import pymysql 
import pandas as pd
from mylib import *

conn = pymysql.connect(host='localhost', user='root', password='rkdaudtjr1!', charset='utf8mb4') 
cursor = conn.cursor() 

#DB 만들기
sql = 'Drop database bobai_web'
sql = "CREATE DATABASE bobai_web" 
cursor.execute(sql)
conn.commit() 
conn.close() 


conn = pymysql.connect(host='localhost', user='root', password='rkdaudtjr1!', db='bobai_web', charset='utf8mb4') 
cursor = conn.cursor()


## 테이블 만들기
sql = '''CREATE TABLE Pair_Info (
    PairId char(50) NOT NULL PRIMARY KEY,
    TokenId char(50) NOT NULL,
    Name varchar(100),
    Symbol varchar(100),
    Creator char(50),
    CreatedAtTimestamp char(15),
    IsScam Bool,
    Decimals int
) CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
''' 
##
cursor.execute(sql) 


#API로 데이터 불러오고
datas = pd.read_csv('Pairs_v2.3.csv',encoding='utf-8-sig').to_dict('records')

#예제...
#sql = "delete from pair_info;"
#sql = "ALTER TABLE table_name MODIFY COLUMN ex_column varchar(16) NULL;"
#sql = "ALTER table pair_INFO modify column name varchar(100);"
#sql = "Alter table pair_INfo modify column symbol varchar(100);"
#sql = "INSERT INTO user (email, department) VALUES (%s, %s)"
#cursor.execute(sql)

#저장하기 .. 
sql = '''
INSERT INTO Pair_INFO(PairId, TokenId, Name, Symbol, Creator, CreatedAtTimestamp, IsScam, Decimals) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
'''


for data in datas:
    try:
        Pair_id = data['id']
        Token_id = data['token00.id']
        Name = data['token00.name']
        Symbol = data['token00.symbol']
        Creator = data['creator_address']
        CreatedAtTimestamp = data['createdAtTimestamp']
        IsScam = False
        Decimals = data['token00.decimals']
        cursor.execute(sql,(Pair_id,Token_id,Name,Symbol,Creator,CreatedAtTimestamp,IsScam,Decimals)) 
    except:
        print(Pair_id)
        print(Name)

conn.commit()
conn.close() 


## DB가 있는 상태에서 업데이트 하는 코드
## DB에는 위에 코드로 Pairs_v2.3.csv 파일의 내용이 들어가 있어야 한다.

conn = pymysql.connect(host='localhost', user='root', password='rkdaudtjr1!', db='bobai_web', charset='utf8mb4') 
cursor = conn.cursor()

sql = "select CreatedAtTimestamp from pair_info order by createdAtTimestamp desc limit 0,1"
cursor.execute(sql)
result = cursor.fetchall()
last_timestamp = result[0][0]
last_timestamp
len(result['data']['pairs'])
# TheGraph에서 일반적인 정보를 먼저 불러오기. 바로 뒤에서 Creator 찾는 코드 돌려야 함
datas = []
query = query_latest % str(last_timestamp)
result = run_query(query)
switch_token(result)
pair = result['data']['pairs'][0]
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