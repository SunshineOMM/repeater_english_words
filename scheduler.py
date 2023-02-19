from datetime import datetime
import time
import asyncio
import psycopg2
from random import shuffle
import config
import random as r

def dummy():
    asyncio.run(time_loop())

def get_all_user_ids():
    conn = psycopg2.connect(**{
            'host':"postgresql",
            'database':"postgres",
            'user':'postgres',
            'password':'postgres',
            'port':'5432'})
    cur = conn.cursor()
    try:       
        sql_query='''SELECT user_id FROM words'''
        cur.execute(sql_query)
        users=set(cur.fetchall())
        return users
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()       
 
def get_n_random_words(user_id,n):
    try:
        conn = psycopg2.connect(**{
            'host':"postgresql",
            'database':"postgres",
            'user':'postgres',
            'password':'postgres',
            'port':'5432'})
        cur = conn.cursor()
        sql_query='''SELECT eng_word,rus_word,pron FROM words WHERE user_id=%(user_id)s AND rus_word IS NOT NULL'''
        cur.execute(sql_query,{'user_id':user_id})
        words=list(cur.fetchall())
        shuffle(words)
        return words if len(words)<=n else words[:n]
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()

def prepare_messages():
    dict_of_messages=[]
    user_ids=get_all_user_ids()
    for user_id in user_ids:
        words=get_n_random_words(user_id,5)
        dict_of_messages.append({'words':words,'user_id':user_id[0]})
    return dict_of_messages
        
async def time_loop():
    while True:
        messages=prepare_messages()
        for message in messages:
            for eng, rus, pron in message['words']:
                if r.randint(0,500)%2==0:
                    await config.BOT.send_message(int(message['user_id']), f'<tg-spoiler>{eng}</tg-spoiler> - {rus}', parse_mode="HTML")
                    await config.BOT.send_audio(int(message['user_id']), pron, performer = "Performer", title = "Title")
                else:
                    await config.BOT.send_message(int(message['user_id']), f'{eng} - <tg-spoiler>{rus}</tg-spoiler>', parse_mode="HTML")
                    await config.BOT.send_audio(int(message['user_id']), pron, performer = "Performer", title = "Title")
        time.sleep(60)


if __name__=="__main__":
    print(datetime.now().strftime('%H:%M'))