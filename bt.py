from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import random

hugging_face_model_repo="Grossmend/rudialogpt3_medium_based_on_gpt2"
print("Loading "+hugging_face_model_repo.split("/")[-1]+" model")
tokenizer = AutoTokenizer.from_pretrained(hugging_face_model_repo)
model = AutoModelForCausalLM.from_pretrained(hugging_face_model_repo)

def temperature_cor(temp):
    t=temp-35.8
    if t <= 0:t=0.01
    return t
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

def format(text):
    tokens_count = len(tokenizer.encode(text))
    if tokens_count <= 15:l='1'
    elif tokens_count <= 50:l='2'
    elif tokens_count <= 256:l='3'
    else:l='-'
    return f"|0|{l}|"+ text + tokenizer.eos_token+"|1|-|"

def tgenerate(tokens,temp=36.6):
    return model.generate(
        tokens,
        num_return_sequences=1,
        max_length=512,
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=50,
        top_p=0.9,
        temperature = temperature_cor(temp),
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id
    )

def generate(tokens):
    return model.generate(
        tokens,
        num_beams=3,
        num_return_sequences=1,
        max_length=512,
        no_repeat_ngram_size=3,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id
    )
def answer(in_text):
    f=format(in_text)
    print(f)
    tokens=tokenizer.encode(f, return_tensors="pt")
    out=generate(tokens)
    out_text=tokenizer.decode(out[0])[len(f):]
    return out_text.replace("</s>","")
def history_answer(lst):
    text=list_to_dialo(lst)
    print(text)
    tokens=tokenizer.encode(text, return_tensors="pt")
    out=generate(tokens)
    out_text=tokenizer.decode(out[0])[len(text):]
    return out_text.replace("</s>","")
"""
while 1:
    temp+=random.randint(-1,1)/10
    input_user = input("<===  User: ")
    print(".... Печатает\r",end='')
    bot_input_ids = tokenizer.encode(f"|0|{get_length_param(input_user)}|" + input_user + tokenizer.eos_token +  "|1|1|", return_tensors="pt")

    #bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids


    print("                  ",end='')
    print(f"\n{temp}°C RuGPT: {tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)}\n")
    step=1
"""
