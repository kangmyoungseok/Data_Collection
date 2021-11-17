import json
import requests
from bs4 import BeautifulSoup
import re 


query_pairs = '''
{
 pairs(first: 1000, orderBy: createdAtBlockNumber, orderDirection: desc, where:{createdAtTimestamp_lt : %s}) {
   id
   token0{
    id
    symbol
    name
    txCount
    totalLiquidity
    decimals
  }
   token1{
    id
    symbol
    name
    txCount
    totalLiquidity
    decimals
  }
   reserve0
   reserve1
   totalSupply
   reserveUSD
   reserveETH
   txCount
   createdAtTimestamp
   createdAtBlockNumber
 }
}
''' 


query_latest = '''
{
 pairs(first: 1000, orderBy: createdAtBlockNumber, orderDirection: desc, where: {createdAtTimestamp_gt:%s}) {
   id
   token0{
    id
    symbol
    name
    txCount
    totalLiquidity
    decimals
  }
   token1{
    id
    symbol
    name
    txCount
    totalLiquidity
    decimals
  }
   reserve0
   reserve1
   totalSupply
   reserveUSD
   reserveETH
   txCount
   createdAtTimestamp
   createdAtBlockNumber
 }
}
''' 


def get_creatorAddress(token_id):
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
              creator_address = 'Fail to get Creator Address'
    
    return creator_address


def run_query(query):

    # endpoint where you are making the request
    request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
                            '',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))


def switch_token(result):
    for pair in result['data']['pairs']:
        if (int(pair['token0']['txCount']) > int(pair['token1']['txCount'] )):
            pair['reserve00'] = pair['reserve1']
            pair['token00'] = pair['token1']
        else:
            pair['reserve00'] = pair['reserve0']
            pair['token00'] = pair['token0']


query_pairs = '''
{
 pairs(first: 1000, orderBy: createdAtBlockNumber, orderDirection: desc, where:{createdAtTimestamp_lt : %s}) {
   id
   token0{
    id
    symbol
    name
    txCount
    totalLiquidity
    decimals
  }
   token1{
    id
    symbol
    name
    txCount
    totalLiquidity
    decimals
  }
   reserve0
   reserve1
   totalSupply
   reserveUSD
   reserveETH
   txCount
   createdAtTimestamp
   createdAtBlockNumber
 }
}
''' 


