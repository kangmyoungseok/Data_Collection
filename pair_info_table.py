import pymysql 
import pandas as pd

conn = pymysql.connect(host='localhost', user='root', password='rkdaudtjr1!', charset='utf8') 
cursor = conn.cursor() 

#DB 만들기
sql = "CREATE DATABASE bobai_web" 
cursor.execute(sql)
conn.commit() 
conn.close() 


conn = pymysql.connect(host='localhost', user='root', password='rkdaudtjr1!', db='bobai_web', charset='utf8') 
cursor = conn.cursor()

## 테이블 만들기
sql = '''CREATE TABLE Pair_Info (
    Pair_id char(36) NOT NULL PRIMARY KEY,
    Name varchar(32),
    Symbol varchar(20),
    Creator char(36),
    Created_Timestamp timestamp,
    Is_Scam Bool,
    Created_At_Blocknumber int(4)
) 
''' 
##
cursor.execute(sql) 


#API로 데이터 불러오고
datas = pd.read_csv('Pairs_v2.1.csv',encoding='utf-8-sig').to_dict('records')
len(datas)

#저장하기 .. 
sql = "INSERT INTO user (email, department) VALUES (%s, %s)"
sql = '''
INSERT INTO Pair_INFO VALUES(%s,%s,%s,%s,'123',%s,%s,%s)
'''



for data in datas:
    Pair_id = data['id']
    Name = data['token00.name']
    Symbol = data['token00.symbol']
    Creator = data[]
    cursor.execute(sql,("developer_lim@limsee.com", "AI")) 


conn.commit() 
conn.close() 

conn.close() 