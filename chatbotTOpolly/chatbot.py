import traceback
import openai
from prompt import Prompt
import random
import json
from extractor import extract_prompts
from config import Config



class ChatBot:

    def __init__(self, model_name, api_key, api_base, system_prompt, examples):
        self.model_name = model_name
        openai.api_key = api_key
        openai.api_base = api_base
        self.examples = examples
        self.messages = [{"role": "system", "content": system_prompt}]
        for example in examples:
            # print("example",example)
            # print("example_type",type(example))
            user_message, assistant_message = example
            self.messages.append({"role": "user", "content": user_message})
            self.messages.append({"role": "assistant", "content": assistant_message})

    def query(self, user_input):
        try:
            self.messages.append({"role": "user", "content": user_input})
            output = openai.ChatCompletion.create(
                model=self.model_name,
                messages=self.messages,
            )
            total_tokens = output["usage"]["total_tokens"]
            if total_tokens > 4000:
                self.messages = [self.messages[0]]
                for example in self.examples:
                    user_msg, assistant_msg = example
                    self.messages.append({"role": "user", "content": user_msg})
                    self.messages.append({"role": "assistant", "content": assistant_msg})
                return "Sorry, the conversation was too long and has been reset."

            answer = output["choices"][0]["message"]["content"]
            self.messages.append({"role": "assistant", "content": answer})
            return answer
        except Exception as error:
            traceback.print_exc()
            return str('Error: ' + str(error))


class ChatBotBase:
    def __init__(self, model_name, api_key, api_base, system_prompt, examples):
        self.bot = ChatBot(model_name, api_key, api_base, system_prompt, examples)

    def query(self, user_input):
        return self.bot.query(user_input)


class SD_ChatBot(ChatBotBase):
    def generate_image_prompt(self, description):
        return self.query(description)


class Normal_ChatBot(ChatBotBase):
    def __init__(self, model_name, api_key, api_base, system_prompt, example):
        super().__init__(model_name, api_key, api_base, system_prompt, example)

    def chat(self, user_input):
        return self.query(user_input)



