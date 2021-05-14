#python 3.9.4
#C:\Users\foodDBproject\lib

#-*- coding: utf-8 -*-


# 식품의약안전처에서 제공해주는 인허가업소정보 XML형식

#url = "http://openapi.foodsafetykorea.go.kr/api/key/I2500/xml/1/1000"

# 식품의약안전처에서 제공해주는 인허가업소정보 JSON형식

#url = "http://openapi.foodsafetykorea.go.kr/api/key/I2500/json/1/1000"



import xml.etree.ElementTree as ET

import urllib.request

import datetime

import time

import sys

import pymysql

now = time.localtime()



# xml에서 뽑아낸 데이터를 데이터베이스에 저장한다

def db_insert(PRMS_DT, BSSH_NM, TELNO, LCNS_NO, PRSDNT_NM, INDUTY_NM, ADDR, LAST_UPDATE) :

    # DB Connect

    conn = pymysql.connect(host='localhost', user='root', password='',db='fooddb', charset='utf8')

    curs = conn.cursor()



    sql = """insert into company(PRMS_DT, BSSH_NM, TELNO, LCNS_NO, PRSDNT_NM, INDUTY_NM, ADDR, LAST_UPDATE) values(%s, %s, %s, %s, %s, %s, %s, %s)""";

    curs.execute(sql, (PRMS_DT, BSSH_NM, TELNO, LCNS_NO, PRSDNT_NM, INDUTY_NM, ADDR, LAST_UPDATE))

    conn.commit()

    conn.close()

    sys.exit(1)



# 전체 루프가 돌아간 횟수를 체크한다. 루프 한번에 데이터 1000개씩 가져옴.

chkValue = 1



# 데이터베이스에 데이터 업데이트 날짜 기록을 위한 현재 날짜 저장

CurrentTime = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)



# 식품의약안전처에서 제공해주는 인허가업소정보 API

url = "http://openapi.foodsafetykorea.go.kr/api/key/I2500/xml/%d/%d" % (1000*(chkValue-1)+1, 1000*chkValue)


tree = ET.ElementTree(file=urllib.request.urlopen(url)) #xml 불러오기

root = tree.getroot() #I2500



# API 실행결과를 불러와서 결과값이 있는 경우(INFO-000)에 정보를 받아온다.

result = root.find("RESULT")

if(result.findtext("CODE") == "INFO-000") :



    for row in root.iter("row") :

        print(chkValue,"번째 루프, row id는", row.attrib["id"])
        PRMS_DT = row.findtext("PRMS_DT")
        BSSH_NM = row.findtext("BSSH_NM")
        TELNO = row.findtext("TELNO")
        LCNS_NO = row.findtext("LCNS_NO")
        PRSDNT_NM = row.findtext("PRSDNT_NM")
        INDUTY_NM = row.findtext("INDUTY_CD_NM")
        ADDR = row.findtext("ADDR")



        if BSSH_NM :      # 업소명에 값이 비어있지 않을 때 DB에 투플 삽입 수행

            a = db_insert(PRMS_DT, BSSH_NM, TELNO, LCNS_NO, PRSDNT_NM, INDUTY_NM, ADDR, CurrentTime)     # 함수를 호출하여 수행



    chkValue += 1
    print("========================================")

        

else :
    print("E.O.D 종료")


print("전체 루프 횟수 :", chkValue-1)
