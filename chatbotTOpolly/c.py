import chatbot
from chatbot import SD_ChatBot, Normal_ChatBot 
import prompt
import extractor
import polly

class ChatBotInterface:
    
    def __init__(self, description):
        self.description = description
        prompt_ = prompt.Prompt()
        prompt_.call_prompt(character_description=description)
        model_name = "gpt-3.5-turbo"
        api_key = "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"
        api_base = "https://api.openai.com/v1"

        # SD ChatBot

        system_prompt = prompt_.sd_system_prompt[0]
        examples = list(zip(prompt_.sd_prompt_example_input, prompt_.sd_prompt_example_output))
        self.img_bot = SD_ChatBot(model_name, api_key, api_base, system_prompt, examples)

        # Normal ChatBot

        system_prompt = prompt_.chatbot_system_prompt[0]
        examples = list(zip(prompt_.chatbot_prompt_example_input, prompt_.chatbot_prompt_example_output))
        self.chat_bot = Normal_ChatBot(model_name, api_key, api_base, system_prompt, examples)

        # Text to Video

        self.ttv = polly.TextToVideo("aigc-bj-team1", "http://127.0.0.1:7860/", "Joey")
        response = self.img_bot.generate_image_prompt(description)
        i_prompt, i_neg_prompt = extractor.extract_prompts(response)

        print('\nPrompt ##########################\n')

        print(i_prompt)

        print('\nNeg Prompt ######################\n')

        print(i_neg_prompt)

        bot_img = self.ttv.gen_img(i_prompt, i_neg_prompt, '/root/bot_img.png')
        self.bot_img_local = bot_img
        print('bot_img_local')
        print(self.bot_img_local)
            
    def chat(self, user_input):
        
        response = self.chat_bot.chat(user_input)
        self.ttv.clear_tmp()
        audio_s3 = self.ttv.tts(response, "audio.mp3")
        audio_local = self.ttv.download_to_tmp(audio_s3, "audio.mp3")
        print(audio_local)
        print(self.bot_img_local)
        result_s3 = self.ttv.gen_sad_talker(audio_local, self.bot_img_local, "result.mp4")
        self.video_local = self.ttv.download_to_tmp(result_s3, "result.mp4")
        
        
        
        
        
        
        
        
        
    

        
        
