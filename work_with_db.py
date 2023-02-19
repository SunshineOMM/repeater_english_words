import config 
import psycopg2
from configparser import ConfigParser
from typing import Dict
from random import shuffle

def connect():    
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**config.DBPARAMS)
        cur = conn.cursor()
        
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def create_db(db_name) -> None:
    conn = psycopg2.connect(**config.DBPARAMS)
    cur = conn.cursor()

    # "CREATE DATABASE" requires automatic commits
    conn.autocommit = True
    sql_query = f"CREATE DATABASE {db_name}"

    try:
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        cur.close()
    else:
        # Revert autocommit settings
        conn.autocommit = False

def execute_query(sql_query: str,) -> None:
    conn = psycopg2.connect(**config.DBPARAMS)
    cur = conn.cursor()
    try:       
        # Execute the table creation query
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {sql_query}")
        conn.rollback()
        cur.close()
    else:
        # To take effect, changes need be committed to the database
        conn.commit()

def add_new_word(dict_of_data)-> None:
    try:
        conn = psycopg2.connect(**config.DBPARAMS)
        cur = conn.cursor()
        sql = """INSERT INTO words(user_id,eng_word, rus_word, pron) VALUES(%(user_id)s,%(eng_word)s,%(rus_word)s,%(pron)s)"""
        cur.execute(sql, dict_of_data)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()
    else:
        # To take effect, changes need be committed to the database
        conn.commit()
        print(f'Add word:{dict_of_data["eng_word"]}')
        
def get_n_random_words(user_id,n):
    try:
        conn = psycopg2.connect(**config.DBPARAMS)
        cur = conn.cursor()
        sql_query='''SELECT * FROM words WHERE user_id=%(user_id)s'''
        cur.execute(sql_query,{'user_id':user_id})
        words=list(cur.fetchall())
        print(words)
        shuffle(words)
        return words if len(words)<=n else words[:n]
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()
      
def get_all_user_ids():
    try:
        conn = psycopg2.connect(**config.DBPARAMS)
        cur = conn.cursor()
        sql_query='''SELECT user_id FROM words'''
        cur.execute(sql_query)
        users=set(cur.fetchall())
        print(users)
        return users
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()       
        
def get_id_not_translate_words():
    try:
        conn = psycopg2.connect(**config.DBPARAMS)
        cur = conn.cursor()
        sql_query='''SELECT id FROM words WHERE rus_word=NULL'''
        cur.execute(sql_query)
        users=set(cur.fetchall())
        print(users)
        return users
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()      
        
def get_info_about_word(eng_word):
    conn = psycopg2.connect(**config.DBPARAMS)
    cur = conn.cursor()
    sql_query='''SELECT eng_word, rus_word, pron FROM words WHERE eng_word=%(eng_word)s'''
    try:    
        cur.execute(sql_query,{'eng_word':eng_word})
        info=cur.fetchone()
        return info
    except Exception as e:
        return None