from dotenv import load_dotenv
from anthropic import Anthropic
import json
load_dotenv()
client=Anthropic()
model="sonnet-4-6"

def add_user_message(messages,text):
    user_message={
        "role":"user",
        "content":text
    }
    messages.append(user_message)

def chat(messages,system=None,temprature=0.0):
    params={
        "model":model,
        "max_tokens":1000,
        "messages":messages,
        "temprature":temprature,
    }    
    if system:
        params["system"]=system
    response=client.messages.create(params)

    return response.content[0].text    

def add_assistant_message(messages,text):
    assistant_message={
        "role":"assistant",
        "content":text
    }
    messages.append(assistant_message)

message_block=[]
add_user_message(message_block,"genrate a very short event bridge role in json")
add_assistant_message(message_block,"```json")
text= chat(message_block,stop_sequence=["```"])
json.loads(text.strip())

prompt="""Genrate three different sample AWS CLI commands. Each should be very short"""

add_user_message(message_block,prompt)
add_assistant_message(message_block,"Here are all three commands in  a single block without any comments:\n```bash")
text= chat(message_block,stop_sequence=["```"])

