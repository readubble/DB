import csv
import pymysql
import pandas as pd
import pymysql
import paramiko
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser
import os

# 파일 리스트를 저장할 리스트 생성
file_list = []

# 현재 디렉토리에서 .csv 파일만 찾아서 파일 리스트에 추가
for file in os.listdir('.'):
    if file.endswith('.csv'):
        file_list.append(file)
file_list.sort()
print(file_list)

# 코드 1,2 공통 : 원격 DB 연결
ssh_host = 
ssh_port = 
ssh_user = 
home = expanduser('~')
myPkey = paramiko.RSAKey.from_private_key_file(home + '')
sql_hostname=
sql_username=
sql_password=

with SSHTunnelForwarder( (ssh_host, ssh_port), ssh_username=ssh_user, ssh_pkey=myPkey, remote_bind_address=(sql_hostname,3306)) as tunnel:
     conn = pymysql.connect(host='', user=sql_username, password=sql_password, db='', port=tunnel.local_bind_port, charset='utf8mb4')

     # 코드1 : 파일 여러개 읽기
     for file in file_list:
          with open(file, "r", encoding='utf-8') as csv_file:
               csv_reader = csv.reader(csv_file)
               header = next(csv_reader)
               curs = conn.cursor()
               for row in csv_reader:
                    target_code = row[0]
                    word_nm = row[1]
                    word_mean = row[2]
                    sql = "INSERT INTO dict(target_code, word_nm, word_mean) values (%s, %s, %s)"
                    curs.execute(sql, (target_code, word_nm, word_mean))
               conn.commit()
               curs.close()

     # 코드2 : 파일 1개 읽기
     # file = open("word_data_50000.csv", "r", encoding='utf-8')  # 파일 열기, "r" : 읽기 전용
     # csv_reader = csv.reader(file)
     # header = next(csv_reader)
     # curs = conn.cursor()
     # for row in csv_reader:
     #      target_code = row[0]
     #      word_nm = row[1]
     #      word_mean = row[2]
     #      sql = "INSERT INTO dict(target_code, word_nm, word_mean) values (%s, %s, %s)"
     #      curs.execute(sql, (target_code, word_nm, word_mean))
     # 
     #      print("target_code: ", target_code, " word_nm: ", word_nm, " word_mean: ", word_mean)
     # 
     # print("Complete")
     # conn.commit()
     # file.close()
     # conn.close()



