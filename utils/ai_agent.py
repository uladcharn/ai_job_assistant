import openai
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key = os.environ.get('API_KEY_OPENAI')

_ = load_dotenv()

class Agent:
    def __init__(self, prompt=""):
        self.prompt = prompt
        self.messages = []
        if self.prompt:
            self.messages.append({"role": "system", "content": prompt})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = openai.ChatCompletion.create(
                        model="gpt-4o-mini", 
                        temperature=0.2,
                        messages=self.messages)
        return completion.choices[0].message.content
        
