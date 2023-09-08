import traceback
import openai
from prompt import Prompt
import random
import json
from extractor import extract_prompts
from config import Config
from chatbot import Normal_ChatBot,SD_ChatBot


def normal_conversation(api_key, api_base, prompt_instance):
    examples = list(zip(prompt_instance.chatbot_prompt_example_input, prompt_instance.chatbot_prompt_example_output))
    normal_bot = Normal_ChatBot(Config.MODEL_NAME, api_key, api_base, prompt_instance.chatbot_system_prompt[0],
                                examples)

    print("Normal ChatBot is ready to chat!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        response = normal_bot.chat(user_input)
        print("Bot:", response)


def generate_prompts_from_description(api_key, api_base, character_description):
    # Initialize the prompt generator
    prompt_generator = Prompt()

    # Call the prompt generator
    prompt_generator.call_prompt(character_description=character_description)

    # Create an instance of the SD_ChatBot to generate the image prompt
    examples = list(zip(prompt_generator.sd_prompt_example_input, prompt_generator.sd_prompt_example_output))
    sd_bot = SD_ChatBot(Config.MODEL_NAME, api_key, api_base, prompt_generator.sd_system_prompt[0], examples)

    # Generate the image prompt from the character description
    image_prompt = sd_bot.generate_image_prompt(character_description)

    # Extract prompts (assuming the extract_prompts function is available)
    prompt, negative_prompt = extract_prompts(image_prompt)

    return {
        "prompt": prompt,
        "negative_prompt": negative_prompt
    }

def test_generate_prompt():
    api_key=Config.API_KEY
    api_base=Config.API_BASE
    character_description="I would like to talk with Bezos, Amazon's Founder"
    prompt_dict =generate_prompts_from_description(api_key,api_base,character_description)
    prompt = prompt_dict['prompt']
    negative_prompt = prompt_dict['negative_prompt']
    print("prompt",prompt)
    print("negative_prompt",negative_prompt)

if __name__=="__main__":
    test_generate_prompt()

