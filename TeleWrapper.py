import telebot
import bt
import base64 as b64
import zlib
#import importlib
#import Bot_SEED
import DroidSpeechkit as d
bot = telebot.TeleBot("NONONO")
print("Bot is active")

def encode_story(txt):
	return b64.b64encode(zlib.compress(txt.encode(),9)).decode()+">--DialogID--<\n\n"
def decode_story(txt):
	return zlib.decompress(b64.b64decode(txt)).decode()
@bot.message_handler(commands=['start'])
def send_start(message):
	bot.reply_to(message, bt.answer("Привет"))

@bot.message_handler(commands=['how'])
def send_start(message):
	bot.reply_to(message, "Я Amadeus, и сейчас я объясню тебе свой механизм работы!")
	bot.send_message(message.chat.id,"В моём основании лежит [нейросеть RuGPT3 transformer обученная сбербанком](https://huggingface.co/sberbank-ai/rugpt3large_based_on_gpt2)",parse_mode="markdown")
	bot.send_message(message.chat.id,"А точнее [вот эта версия](https://huggingface.co/Grossmend/rudialogpt3_medium_based_on_gpt2) дообученная для диалогов 1 на 1",parse_mode="markdown")
	bot.send_message(message.chat.id,"Каждое твое сообщение [превращается в токены](https://huggingface.co/docs/transformers/main_classes/tokenizer) и скармливается ей",parse_mode="markdown")
	bot.send_message(message.chat.id,">DialogID< - это архив-строка в которой зашифрован весь предшествующий диалог")
	bot.send_message(message.chat.id,"Если хочешь продолжать уже начатый разговор то просто отвечай на сообщения бота в которых есть DialogID кнопочкой 'ответить' и он будет отвечать ориентируясь на историю диалога")
	bot.send_message(message.chat.id,"Для синтеза голоса используется [API гугла](https://pypi.org/project/gTTS/) как и для [распознавания речи](https://pypi.org/project/SpeechRecognition/)",parse_mode="markdown")
@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "✅ Нажмите /start что бы бот первый начал диалог\n⤴️ Вы можете писать самостоятельные сообщения\n🔃 Или отвечать на сообщения содержащие DialoID для продолжения разговора\n✴️ Так-же я умею принимать и отправлять голосовые)\n🆘 Если текущий диалог зашёл в тупик или нейросеть зациклилась смело пишите новое самостоятельное сообщение)")
"""
@bot.message_handler(commands=['a'])
def echo_am(message):
	message.text=" ".join(message.text.split(" ")[1:])
	import Bot_SEED
	Bot_SEED=importlib.reload(Bot_SEED)
	bot.reply_to(message, bt.history_answer(Bot_SEED.history+[message.text]))
"""
def message_worker(message):
	try:
		old=message.reply_to_message.text.split(">--DialogID--<\n\n")
		print(old)
		story=eval(decode_story(old[0]))+[old[1]]+[message.text]
		ans=bt.history_answer(story)
	except:
		story=[message.text]
		ans=bt.answer(message.text)
	print(ans)
	return encode_story(str(story))+ans
@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.send_chat_action(message.from_user.id, 'typing')
	ans=message_worker(message)
	print(ans)
	bot.reply_to(message, ans)


@bot.message_handler(content_types=['voice'])
def echo_audio(message):
	bot.send_chat_action(message.from_user.id, 'record_audio')
	file_info = bot.get_file(message.voice.file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	with open("cache.ogg", 'wb') as new_file:
		new_file.write(downloaded_file)
	d.ogg_2_wav()
	try:
		message.text=d.listen("cache.wav")
	except:
		return None
	print(message.text)
	ans=message_worker(message)
	print(ans)
	d.say(ans.split(">--DialogID--<\n\n")[-1])
	bot.reply_to(message, ans)
	bot.send_voice(message.chat.id, open("cache.mp3","rb"))
bot.infinity_polling()