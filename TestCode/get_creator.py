from os import error
from lib.mylib import *
import pandas as pd
from multiprocessing import Pool
import time
from tqdm import tqdm

mint_query_template = '''
{
  mints(first: 1, orderBy: timestamp, orderDirection: asc, where:{ pair: "%s" }) {
      amount0
      amount1
      to
      sender
      timestamp
 }
}
''' 
def run_query(query):

    # endpoint where you are making the request
    request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
                            '',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))

datas = pd.read_csv('Creator_list_v1.1.csv',encoding='utf-8-sig').to_dict('records')
len(datas)

proxy_contracts = [
'0x5e5a7b76462e4bdf83aa98795644281bdba80b88',
'0x000000000092c287eb63e8c2c30b4a74787054f8',
'0x0f4676178b5c53ae0a655f1b19a96387e4b8b5f2',
'0xdf65f4e6f2e9436bc1de1e00661c7108290e8bd3',
'0xdb73dde1867843fdca5244258f2fd4b6dc7b154e',
'0xbdb1127bd15e76d7e4d3bc4f6c7801aa493e03f0',
'0x8f84c1d37fa5e21c81a5bf4d3d5f2e718a2d8eb4',
'0x908521c8e53e9bb3b8b9df51e2c6dd3079549382',
'0x85aa7f78bdb2de8f3e0c0010d99ad5853ffcfc63',
'0x909d05f384d0663ed4be59863815ab43b4f347ec',
'0xb4a2810e9d0f1d4d2c0454789be80aaeb9188480',
'0x96fc64f7fe4924546b9204fe22707e3df04be4c8',
'0x226e390751a2e22449d611bac83bd267f2a2caff'
]



query_address = []
for data in tqdm(datas,desc="개발자 찾기:"):
    if(data['token00_creator_address'] in proxy_contracts):
        query = mint_query_template % data['id']
        response = run_query(query)
        creator_address = response['data']['mints'][0]['to']
        data['token00_creator_address'] = creator_address        



pd.DataFrame(datas).to_csv('Creator_list_v1.2.csv',encoding='utf-8-sig',index=False)

