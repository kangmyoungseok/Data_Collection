# Data_Collection
웹 페이지에 띄워줄 데이터들 모으기

DB : bobai_web
ID : root
PW : rkdaudtjr1!
table : Pair_Info

업데이트는 2가지 관점이 있다.
1. 주기적(대충 30분?)으로 Newest토큰을 부르고 추가된 애들의 정보를 부르는 업데이트
2. 일정 시간(3시간/24시간)마다 업데이트 -> 얘네는 한 1000개 내외의 데이터를 업데이트 할 것

# 1. make_pairInfo_DB.py
첫 DB 생성. 기존 Pairs_v2.3파일에서 있던 데이터들을 DB에 저장한다.

# 1.update_pairInfo_DB.py
기존에 있던 DB에서 가장 최근의 TimeStamp를 가져와서 그 시간 이후에 생성된 토큰들만 다시 정보를 업데이트


# 2. LP_Lock.py
 - Ethplorer API로 LP Token의 탑 홀더를 불러와서 LP Lock / LP avg / LP stdev 구했음
 - 결과 : Pairs_v2.4.csv

# 2. LP_Lock_update.py
 - 1번에서 몇개가 추가되면... 기존에 ......???

 


# 일단 현재까지 모아놓은 데이터 파일들 DB에 집어 넣고, 그다음 업데이트 코드를 짠다.
# Pair.py 실행
# 21.11.16 일까지 모은 데이터 Pairs_v2.1.csv 뽑고
# 없는 정보 : Creator Address 
# Creator_list.csv에서 전에 모아놨던 Creator 일단 붙여 넣고 없는거 Creator.py에서 더 뽑자

# 1.copy_creator.py 에서 이전에 있던 파일에서 Creator 찾아서 넣었고  --> Pairs_v2.2.csv
# 2. Creator.py 돌리면 없는 애들 Creator 찾는다. -> Error_list.csv -> 찾은애들 기존 Creator_list.csv에 더한뒤 -> Pairs_v2.3.csv
# 그러면 이제 Creator까지 끝


# 이제 DB에 넣어 보자

