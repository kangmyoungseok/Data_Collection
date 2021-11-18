import pymysql
import csv
import pandas as pd

conn = pymysql.connect(host='localhost', user='root', password='rkdaudtjr1!', db='bobai_web', charset='utf8mb4') 
cursor = conn.cursor()

#feature : 테이블 명
def make_csv(feature):
    column = []
    sql = "show full columns from %s" %feature
    cursor.execute(sql)
    rows = cursor.fetchall()
    for i in range(len(rows)):
        column.append(rows[i][0])

    sql = "select * from %s" %feature
    cursor.execute(sql)
    rows = cursor.fetchall()

    rows = list(rows)
    
    f = open('%s.csv'%feature, 'w', encoding='utf-8-sig', newline = '')
    wr = csv.writer(f)

    wr.writerow(column)

    for i in range(len(rows)):
        wr.writerow(rows[i])
    f.close()
    
    conn.close()

make_csv('pair_info')