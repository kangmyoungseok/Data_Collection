# Data_Collection
웹 페이지에 띄워줄 데이터들 모으기

DB : bobai_web
ID : root
PW : rkdaudtjr1!
table : Pair_Info

# 1. make_pairInfo_DB.py
첫 DB 생성. 기존 Pairs_v2.3파일에서 있던 데이터들을 DB에 저장한다.

# 2.update_pairInfo_DB.py
기존에 있던 DB에서 가장 최근의 TimeStamp를 가져와서 그 시간 이후에 생성된 토큰들만 다시 정보를 업데이트



# 일단 현재까지 모아놓은 데이터 파일들 DB에 집어 넣고, 그다음 업데이트 코드를 짠다.
# Pair.py 실행
# 21.11.16 일까지 모은 데이터 Pairs_v2.1.csv 뽑고
# 없는 정보 : Creator Address 
# Creator_list.csv에서 전에 모아놨던 Creator 일단 붙여 넣고 없는거 Creator.py에서 더 뽑자

# 1.copy_creator.py 에서 이전에 있던 파일에서 Creator 찾아서 넣었고  --> Pairs_v2.2.csv
# 2. Creator.py 돌리면 없는 애들 Creator 찾는다. -> Error_list.csv -> 찾은애들 기존 Creator_list.csv에 더한뒤 -> Pairs_v2.3.csv
# 그러면 이제 Creator까지 끝


# 이제 DB에 넣어 보자

