from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import config as config
import scheduler
import work_with_db as db
from multiprocessing import Process
import request_for_translate

dp = Dispatcher(config.BOT)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Пока что я тебе ничего не скажу!")



@dp.message_handler()
async def translate_message(msg: types.Message):
    """Приём английского слова, его перевод и составление произношения, занесение данных в БД
    Args:
        msg (types.Message): _description_
    """
    
    trnsl,pron=request_for_translate.create_translate_and_pron(msg.text)
    dict_of_data={'user_id':msg.from_user.id,
                  'eng_word':msg.text.lower(),
                  'rus_word':trnsl,
                  'pron':pron}
    db.add_new_word(dict_of_data)
    await config.BOT.send_message(msg.from_user.id, f'ENG: *{msg.text}*, RUS: *{trnsl}*', parse_mode= 'Markdown')
    await config.BOT.send_audio(msg.from_user.id,pron,title=msg.text)


if __name__ == '__main__': 
    
    # cr_tbl_sql = """DROP TABLE IF EXISTS words"""
    # db.execute_query(cr_tbl_sql)
    
    cr_tbl_sql = """
        CREATE TABLE IF NOT EXISTS words (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR (50) NOT NULL,
            eng_word VARCHAR (100) NOT NULL,
            rus_word VARCHAR (100),
            transcrib VARCHAR (100),
            repeat_status INT DEFAULT 0,
            examples VARCHAR (200),
            date_create date DEFAULT CURRENT_DATE,
            language VARCHAR (5) DEFAULT 'eng',
            pron bytea 
        )
    """
    db.execute_query(cr_tbl_sql)

    # proc2 = Process(target=request_for_translate.dummy)
    # proc2.start()
    executor.start_polling(dp)
    
    
# TODO
# реализовать механизм запоминания и повторения
# не производить перевод эли такое слово есть в словаре

# настроить индексацию по столбцу eng_word
# BAN 
# translate for batches
# microservice for ml