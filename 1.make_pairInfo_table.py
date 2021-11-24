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
    id char(50) NOT NULL PRIMARY KEY,
    token00_id char(50) NOT NULL,
    token00_name varchar(100),
    token00_symbol varchar(100),
    token00_creator char(50),
    token00_decimals int,
    reserveETH float,
    txCount int,
    createdAtTimestamp char(15),
    isChange Bool,
    isScam Bool,
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
INSERT INTO Pair_INFO(id, token00_id, token00_name, token00_symbol, token00_creator, token00_decimals, reserveETH, txCount, createdAtTimestamp, isChange, isScam) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
'''


for data in datas:
    try:
        id = data['id']
        token00_id = data['token00.id']
        token00_name = data['token00.name']
        token00_symbol = data['token00.symbol']
        token00_creator = data['creator_address']
        token00_decimals = data['token00.decimals']
        reserveETH = data['reserveETH']
        txCount = data['txCount']
        createdAtTimestamp = data['createdAtTimestamp']
        isChange = False
        isScam = False

        cursor.execute(sql,(id,token00_id,token00_name,token00_symbol,token00_creator,token00_decimals,reserveETH,txCount,createdAtTimestamp,isChange,isScam)) 
    except Exception as e:
        print(e)
        

conn.commit()
conn.close() 
