# % pip install anthropic python-dotenv
# the above command will only work for macos/linux because % is not present in window in windows we use !
#
# ! pip install anthropic python-dotenv
# we can also use uv to install the anthropic sdk and python-dotenv sdk but to do so we have to first import the sys
# import sys
# ! uv pip install anthropic python-dotenv -- python {sys.executable}

from dotenv import load_dotenv  #basically importing environment variable
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

response = client.messages.create(
    model=model,  #basically these are all the attributes we gonna pass to the user
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "what is quantum physics"}
    ]
)
print(response.content[0].text)


#these are the helper function which are we gonna use to pass the previous messages

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages):
    message = client.messages.create(
        model=model,  #basically these are all the attributes we gonna pass to the user
        max_tokens=1000,
        messages=messages
    )
    return message.content[0].text

messages_block= []
add_user_message(messages_block,"what is quantum computing")
print(messages_block)

answer = chat(messages_block)
add_assistant_message(messages_block, answer)

add_user_message(messages_block, "write another sentence")
answer = chat(messages_block)
print(answer)