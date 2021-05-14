#python 3.9.4
#C:\Users\foodDBproject\lib

#-*- coding: utf-8 -*-


# LOCALDATA 지방행정인허가정보 데이터셋 삽입
# http://www.localdata.go.kr/platform/rest/TO0/openDataApi?authKey=



#import xml.etree.ElementTree as ET

#import urllib.request

from xml.etree.ElementTree import parse

import datetime

import time

import sys

import pymysql

now = time.localtime()




# localdata 공공데이터에서 내려받은 xml파일이 저장된 위치
# 경로표시에서 \를 하나만 붙이면 유니코드 오류 있음. 2개 사용하기.

url = "C:\\Users\\Documents\\식품DB\\localdata\\fulldata_07_21_01_P_위탁급식영업.xml"



tree = parse(url) #xml 파일 불러오기

root = tree.getroot() #result

header = root.find("header")

totalCount = header.find("paging").findtext("totalCount") #30411

body = root.find("body")

rows = body.find("rows")

#for row in rows.iter("row")
