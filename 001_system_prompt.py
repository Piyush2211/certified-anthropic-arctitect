from dotenv import load_dotenv
from anthropic import Anthropic
load_dotenv()
client= Anthropic()
model= 'claude-sonnet-4.7'
def add_user_message(messages,text):
  user_message={
    "role":"user",
    "content":text
    
  }
  messages.append(user_message)


def chat(messages,system=None):# so basically in create function we cannot pass the system prompt to null in order to handle this we have to pass the parameters as dictionary with ** this will unpack the dictionary
  
  params = {
    "model":model,
    "max_tokens":1000,
    "messages":messages,
     
  }
  if system:
    params["system"]:system
  response= client.messages.create(**params )#so basically rather than defining every attribute of create function we have created params and added optional handling to either add system prompt or not and pass the arguments as dictionary and we can unpack them with **
  return response.content[0].text

def add_assistent_message(messages,text):
  assistant_message={
    "role":"assistant",
    "content":text
  }
  messages.append(assistant_message)

message_block= []
system_prompt=""" your are a tester who has will test the pr created by the user
"""
while True:
  user_input= input("-->")
  print("-->"+user_input)
  add_user_message(message_block,user_input)
  answer = chat(message_block,system=system_prompt)
  add_assistent_message(answer) 