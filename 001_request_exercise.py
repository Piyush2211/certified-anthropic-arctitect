from dotenv import load_dotenv
from anthropic import Anthropic
load_dotenv()
client = Anthropic()
model= 'claude-sonnet-4.6'
def add_user_message(messages, text):
    user_message = {
        "role":"user",
        "content":text
    }
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message={
        "role":"assistant",
        "content":text
    }
    messages.append(assistant_message)

def chat(messages):
    response = client.messages.create(
        model = model, 
        max_tokens= 1000,
        messages = messages 
    )
    return response.content[0].text


message_block = []

while True:
    user_input= input("-->")
    print("-->",user_input)
    add_user_message(message_block,user_input)
    answer = chat(message_block)
    print(answer)
    add_assistant_message(message_block,answer)

    
