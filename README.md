# AmadeusTelegramAI

![image](https://user-images.githubusercontent.com/52743561/195871902-093c7feb-7dba-4dcd-b542-cfda3a6f7640.png)

telegram - @AmadeusDroidXBot

# Поехали
Ну что-ж если ты это читаешь то тебя заинтересовал этот проектик.

Давно я хотел запились работающего диалогового бота

*Да такого* что-бы при разговоре ты думал: "Капец он гений"

Но учить нормальную нейронку с нуля на датасетах было слишком долго и бесполезно, а в связи с некоторыми обстоятельствами я еще и не могу использовать мощное железо.

IF-скусственные ELSE-теллекты меня в край задолбали а условная Яндекс-Алиса это вообще полнейший кринж - ИИ который даже ответы сам генерировать не умеет, а просто ищет подходящий в бд

## Что за GPT
<details>
<summary> <b>Раскрыть</b> </summary>

![image](https://user-images.githubusercontent.com/52743561/195866476-02545073-5806-4b20-beb4-49e7155d7560.png)

[**GPT-3 (Generative Pre-trained Transformer 3)**](https://ru.wikipedia.org/wiki/GPT-3) - архитектура conversation моделей разработанная в 2020

[**RuGPT-3 by sberbank**](https://huggingface.co/sberbank-ai/rugpt3large_based_on_gpt2) - аналог GPT3 обученный на русской литературе

[**RuDialoGPT-3**](https://huggingface.co/Grossmend/rudialogpt3_medium_based_on_gpt2) - это [fine-tune](https://huggingface.co/transformers/v4.8.2/training.html) RuGPT3 от энтузиастов, заточенный под продолжение не абстрактных текстов, а диалогов 1на1

>фууу, почему ты взял готовую а не обучил сам?

1. Она обучалась сбербанком в месяц на 128 вычислительных видеокартах 
2. Нейросеть отлично справляется с огромным спектром задач [см. примеры](https://habr.com/ru/company/sberbank/blog/528966/)
</details>

## Почему сбер не использует свою модель как чат-бота?
<details>
<summary> <b>Раскрыть</b> </summary>

![image](https://user-images.githubusercontent.com/52743561/195869657-56bb30d4-a644-49d9-bb09-9a42ef9c2f76.png)

1. Он может послать тебя матом во время диалога (если до этого конечно дойдёт)
2. Условной компании сложно как-то повлиять на уже готовую модель и заставить привлекать клиентов
3. Модель продолжает диалог, а не выполняет конкретные функции, она бесполезна как ассистент
</details>

## Дальше частичный разбор кода (не дописано)
<details>
<summary> <b>Раскрыть (не надо)</b> </summary>

![image](https://user-images.githubusercontent.com/52743561/195871433-42b145b4-a754-42cc-b6c4-63b6c840d32b.png)

Формат ввода у RuDialoGPT3 хитрый, и отличается от других GPT
[https://habr.com/ru/company/icl_services/blog/548244/](В этой статье чел разбирает тонкости)

# bt.py
По сути это обертка для модели, которая занимается форматированием данных.
```python
def list_to_dialo(lst):
    st=""
    speaker=(len(lst)+1)%2
    for i in lst:
        tokens_count = len(tokenizer.encode(i))
        if tokens_count <= 15:l='1'
        elif tokens_count <= 50:l='2'
        elif tokens_count <= 256:l='3'
        else:l='-'
        st+=f"|{speaker}|{l}|"+ i + tokenizer.eos_token
        speaker=(speaker+1)%2
    return st+f"|{speaker}|-|"
```
# TeleWrapper.py
Файл занимается основными функциями бота, такими как общение голосом, генерация архива разговора и т.д.

</details>
