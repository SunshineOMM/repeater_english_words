import time
import asyncio
import psycopg2
import config
import ml.translate as translate
import ml.text2speech as text2speech
import warnings
warnings.filterwarnings("ignore")

# def dummy():
#     asyncio.run(time_loop())

# def get_id_and_eng_words():
#     try:
#         conn = psycopg2.connect(**config.DBPARAMS)
#         cur = conn.cursor()
#         sql_query="SELECT id,eng_word FROM words WHERE rus_word IS NULL"
#         cur.execute(sql_query)
#         id_engwords=list(cur.fetchall())
        
#         return id_engwords 
#     except Exception as e:
#         print(f"{type(e).__name__}: {e}")
#         print(f"Query: {cur.query}")
#         conn.rollback()
#         cur.close()

# def make_translate():
#     id_engwords = get_id_and_eng_words()
#     if len(id_engwords)<=0:
#         return
#     node_ids=[i[0] for i in id_engwords]
#     eng_words=[i[1] for i in id_engwords]
#     translates=[translate.en2ru(eng_word) for eng_word in eng_words]
#     try:
#         conn = psycopg2.connect(**config.DBPARAMS)
#         cur = conn.cursor()
#         sql_query_rus='UPDATE words SET rus_word = %(rus_word)s WHERE id=%(id)s'
#         # TODO
#         # sql_query_transcrib='UPDATE words SET transcrib = %(transcrib)s WHERE id=%(id)s'
#         for i,node_id in enumerate(node_ids):      
#             cur.execute(sql_query_rus,{'rus_word':translates[i],'id':node_id})
#             # TODO
#             #cur.execute(sql_query_transcrib,{'transcrib':transcribs[i],'id':node_id})
#     except Exception as e:
#         print(f"{type(e).__name__}: {e}")
#         print(f"Query: {cur.query}")
#         conn.rollback()
#         cur.close()
#     else:
#         conn.commit()
#         print(f'Add translate')
        
# async def time_loop():
#     while True:
#         time.sleep(10)
#         make_translate()       

def create_translate_and_pron(text):
    trnslt=translate.en2ru(text)
    audio_pron=text2speech.get_audio_pron(text)
    return trnslt, audio_pron



if __name__=="__main__":
    text='I love you, my Sasha!'
    trnslt=translate.en2ru(text)
    print(f'translate:{trnslt}')
    audio_pron=text2speech.get_audio_pron(text)
    with open(f'{text}.wav', 'wb') as f:
        f.write(audio_pron)