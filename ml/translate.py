from transformers import AutoModelForSeq2SeqLM,MarianTokenizer
import warnings
warnings.filterwarnings("ignore")

en_ru_tokenizer = MarianTokenizer.from_pretrained("ml/models/opus-mt-en-ru", local_files_only=True)#  Helsinki-NLP
en_ru_model = AutoModelForSeq2SeqLM.from_pretrained("ml/models/opus-mt-en-ru", local_files_only=True)
# en_ru_tokenizer.save_pretrained('ml/models/opus-mt-en-ru')
# en_ru_model.save_pretrained('ml/models/opus-mt-en-ru')

def en2ru(text):
    """Делает перевод английского слова/словосочетания на русский

    Args:
        text (str): _description_

    Returns:
        str: исходное слово/словосочетание 
    """
    global en_ru_tokenizer
    global en_ru_model
    batch = en_ru_tokenizer([text], return_tensors="pt")
    generated_ids = en_ru_model.generate(**batch)
    answer=en_ru_tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return answer.lower()

if __name__=='__main__':
    print(en2ru('How are you?'))