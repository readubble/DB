#-*- coding: utf-8 -*-
import os
import ast
import openai
import pymysql
import paramiko
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser
import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
ssh_host = os.environ["ssh_host"]
ssh_port = os.environ["ssh_port"]
ssh_user = os.environ["ssh_user"]
home = expanduser('~')
myPkey = paramiko.RSAKey.from_private_key_file(home + os.environ["dir"])
sql_hostname=os.environ["sql_hostname"]
sql_username=os.environ["sql_username"]
sql_password=os.environ["sql_password"]


f = open("info.txt", 'r') #title, writer, image, category, genre, difficulty
data = f.read().split("\n")

f = open("content.txt", 'r') #content
data_content = f.read()


openai.api_key=os.environ["api-key"]

text = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role":"user", "content":data_content+"\n이 글에 대해서 [주제문 1문장, 첫 번째 키워드, 두 번째 키워드, 세 번째 키워드, 5줄 이내의 요약문, [문제]]의 형식으로 답변해주되, 문제는 [[문제내용, [보기 번호1의 내용], [보기 번호2의 내용], [보기 번호3의 내용], 정답번호(숫자만)]] 의 형태로 총 3개를 만들어줘."}
    ]
)

text = text.choices[0].message.content
print(text)

print("내용이 마음에 든다면 [주제문 1문장, 첫 번째 키워드, 두 번째 키워드, 세 번째 키워드, 5줄 이내의 요약문, [문제내용, [보기 번호1의 내용], [보기 번호2의 내용], [보기 번호3의 내용], 정답번호(숫자만)] 의 형태로 재입력 해주세요. 재입력된 형태로 DB에 저장됩니다.")
text = input()
text = ast.literal_eval(text)
with SSHTunnelForwarder( (ssh_host, ssh_port), ssh_username=ssh_user, ssh_pkey=myPkey, remote_bind_address=(sql_hostname,3306)) as tunnel:
        conn = pymysql.connect(host=sql_hostname, user=sql_username, password=sql_password, db=os.environ["sql_db"], port=tunnel.local_bind_port)
        query = "INSERT INTO article(atc_title, atc_writer, atc_text, atc_photo_in, cg_id, genre, difficulty, ans_kwd1, ans_kwd2, ans_kwd3, ans_topic, ans_smr)" \
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        query_2 = "INSERT INTO quiz(tb_article_id, quiz_no, quiz_question, quiz_ans)" \
               "VALUES (%s, %s, %s, %s)"
        query_3 = "INSERT INTO quiz_item(tb_article_id, tb_quiz_no, item_no, item_value)" \
               "VALUES(%s, %s, %s, %s)"
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, (data[0], data[1], data_content, data[2], data[3], data[4], data[5],
                                     text[1], text[2], text[3], text[0], text[4]) )
                k = int(cur.lastrowid)
                for i in range(3):
                    cur.execute(query_2, (k, i+1, text[5][i][0], int(text[5][i][4])))
                    for j in range(1,4):
                        cur.execute(query_3, (k, i+1, j, text[5][i][j]))
            conn.commit()


