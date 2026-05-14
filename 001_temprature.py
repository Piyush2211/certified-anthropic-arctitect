from dotenv import load_dotenv
from anthropic import Anthropic
load_dotenv()
client= Anthropic()
model= "claude-sonnet-4-6"
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
    "system":system,
    "temperature":temprature
  }
  response= client.messages.create(**params)
  return response.content[0].text

def add_assistant_message(messages,text):
   assistent_message={
     "role":"assistant",
     "content":text
   }
   messages.append(assistent_message)

messages_block = []
while True:
  user_input=input("-->")
  print("--->",user_input)
  add_user_message(messages_block,user_input)
  answer=chat(messages_block,system="you are a senior python devloper who has to junior engineer ",temprature=1)