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
