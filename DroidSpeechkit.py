import speech_recognition as recog
from gtts import gTTS as gt
import soundfile as sf
sr=recog.Recognizer()

def listen(filename):
    with recog.AudioFile(filename) as source:
        audio_text = sr.listen(source)
        try:
            print('Преобразование речи...')
            text = sr.recognize_google(audio_text,language="ru")
            print(text)
            return text
        except:
            return "Я промолчю"

def say(text):
    tts = gt(text=text,lang="ru")
    tts.save("cache.mp3")

def ogg_2_wav():
    data, samplerate = sf.read('cache.ogg')
    sf.write('cache.wav', data, samplerate)