#Etherplorer API / Etherscan Crawling으로 Creator Address를 구한다.
from pandas.core.frame import DataFrame
from requests import Request, Session
import pandas as pd
import json
from bs4 import BeautifulSoup
import re # 추가
from urllib.request import urlopen
import requests
import time
from multiprocessing import Pool
import glob
import os


def split_csv(total_csv):
    rows = pd.read_csv(total_csv,chunksize=5000)
    file_count = 0
    for i, chuck in enumerate(rows):
        chuck.to_csv('./result/out{}.csv'.format(i))
        file_count = file_count+1 
    return file_count

def merge_csv():
  input_file = r'./result/'
  output_file = r'./result/result2.csv'

  allFile_list = glob.glob(os.path.join(input_file, 'fout*')) # glob함수로 sales_로 시작하는 파일들을 모은다
  allFile_list.sort()
  print(allFile_list)

  all_Data = []
  for file in allFile_list:
    records = pd.read_csv(file).to_dict('records') 
    all_Data.extend(records)

  DataFrame(all_Data).to_csv(output_file,encoding='utf-8-sig',index=False)
  

def get_creatorAddress(data):
    token_id = data['token00.id']
    repos_url = 'https://api.ethplorer.io/getAddressInfo/'+token_id+'?apiKey=EK-4L18F-Y2jC1b7-9qC3N'
    response = requests.get(repos_url).text
    repos = json.loads(response)    #json 형태로 token_id에 해당하는 정보를 불러온다.
    
    try:
        creator_address = repos['contractInfo']['creatorAddress']
        print('find by ethplorer :' + token_id)
    except:     #오류가 나면 이더스캔에서 크롤링
         url = 'https://etherscan.io/address/'+token_id
         try:
             response = requests.get(url,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'})
             page_soup = BeautifulSoup(response.text, "html.parser")
             Transfers_info_table_1 = str(page_soup.find("a", {"class": "hash-tag text-truncate"}))
             creator_address = re.sub('<.+?>', '', Transfers_info_table_1, 0).strip()
             print('find by etherscan :' + token_id)
         except Exception as e:  #이더스캔 크롤링까지 에러나면 'Error'로 표시
              print(e)
              timeout_count = 0
              while(timeout_count<2):
                  try:
                      print('timeout in, address' + token_id)
                      time.sleep(20)
                      timeout_count = timeout_count + 1
                      response = requests.get(repos_url).text
                      repos = json.loads(response)
                      creator_address = repos['contractInfo']['creatorAddress']
                      break
                  except:
                      creator_address = 'Error'

    data['creator_address'] = creator_address
    return data

if __name__=='__main__':
    file_name = 'error_list.csv'
    file_count = split_csv(file_name)

    for i in range(file_count):         #하나의 파일 단위로 Creator Address 불러오고, 해당 초기 유동성풀 이더값 구해온다.
        file_name = './result/out{}.csv'.format(i)
        datas = pd.read_csv(file_name).to_dict('records')
        datas_len = len(datas)
        try:
            p = Pool(4)
            count = 0
            result = []
            for ret in p.imap(get_creatorAddress,datas):
                print(2)
                count = count+1
                result.append(ret)
                if(count % 200 == 0):
                    print("Process Rate : {}/{} {}%".format(count,datas_len,int((count/datas_len)*100)))
            p.close()
            p.join()
        except Exception as e:
            print(4)
            print(e)
        print(result)
        print('=======')
            
        df = pd.DataFrame(result)
        file_name = './result/fout{}.csv'.format(i)
        df.to_csv(file_name,encoding='utf-8-sig',index=False)
    
merge_csv()