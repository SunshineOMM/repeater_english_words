from espnet2.bin.tts_inference import Text2Speech
import IPython.display as ipd
import joblib
import warnings
warnings.filterwarnings("ignore")

#text2speech = Text2Speech.from_pretrained("espnet/kan-bayashi_ljspeech_vits")
#joblib.dump(text2speech,'ml/models/kan-bayashi_ljspeech_vits/text2speech.joblib')
text2speech=joblib.load('ml/models/kan-bayashi_ljspeech_vits/text2speech.joblib')

def get_audio_pron(text):
    wav = text2speech(text)["wav"]
    audio=ipd.Audio(wav, rate=text2speech.fs)
    return audio.data

if __name__=='__main__':
    text='I am fine and you'
    audio_pron=get_audio_pron(text)
    with open(f'{text}.wav', 'wb') as f:
        f.write(audio_pron)