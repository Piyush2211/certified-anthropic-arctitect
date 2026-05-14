from dotenv import load_dotenv
from anthropic import Anthropic
load_dotenv()
client= Anthropic()
model= 'claude-sonnet-4-6'

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
    response=client.messages.create(**params)
    return response.content[0].text

def add_assistant_message(messages,text):
    assistant_message={
        "role":"assistant",
        "content":text
    }
    messages.append(assistant_message)

messages_block=[]
while True:
    user_input=input("-->")
    print(user_input,"-->")
    add_user_message(messages_block,user_input)
    stream=client.messages.create(
                model=model,
                max_tokens=1000,
                messages=messages_block,
                stream=True#this argument is basically give us stream of events 
            )
    
    for event in stream:
        print(event) # so basically jabh hum stream argument pass karenge  hamare create function meh toh claude hame joh response dega uske andar vo saare events bhi dega jese MessageStart(yeh basically flag hai joh batah hai keh claude koh naaya message send hua hai )ContentBlockStart(yeh start of a new block koh define karta hai jisme metadata hota hai tool use etc kah)ContentBlockDelta(isme message chunks honge jisme text hoga joh user koh display karenge )ContentBlockStop(yeh event define karega keh current Content Block khatam ho chukka hai)MessageDelta(yeh basically define karega keh current message is complete)MessageStop(yeh end information aur metadata share karega current ended message kah)

    with client.messages.stream(
        model=model, # either hum create message seh bhi text extract kar sakte hai but antrhopic neh hame stream function iseh purpose keh liye hi diya hai isme hum saare attributes pass karenge model,max_tokens,messages
        max_tokens=1000,
        messages=messages_block
    ) as stream: 
        for text in stream.text_stream:#idhar hum text stream seh text extract kar rahe hai joh user koh show karna hai 
            print(text,end="")
    stream.get_final_message()        
