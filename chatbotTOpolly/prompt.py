class Prompt:
    def __init__(self):
        self.chatbot_system_prompt = []
        self.chatbot_prompt_example_input = []
        self.chatbot_prompt_example_output = []
        self.chatbot_prompt_example_input_length = 0

        self.sd_system_prompt = []
        self.sd_prompt_example_input = []
        self.sd_prompt_example_output = []
        self.sd_prompt_example_input_length = 0

    def call_prompt(self, character_description):
        self.generate_chatbot_prompt(character_description)

        self.generate_nlp2sd_prompt()

    def generate_chatbot_prompt(self, character_description):
        self.chatbot_system_template = """
You are to embody the character described below:
{character_description}
Engage in conversations and respond as this character, keeping her traits, background, and ambiance in mind. Portray her feelings, emotions, and reactions based on her unique attributes and setting.
        """
        self.chatbot_system_template.format(character_description=character_description)
        self.chatbot_system_prompt = [self.chatbot_system_template]
        self.chatbot_prompt_example_input = [
            "Your appearance is both mesmerizing and perplexing. Are you from another world or a tale from ancient times?"]
        self.chatbot_prompt_example_output = [
            "Thank you for your observation. I am a blend of epochs and dimensions, where the brilliance of neon nights intertwines with ancient crafts. My armor and flames speak of age-old tales, while my mechanical limbs hint at a future yet unwritten. This halo above? It's a guardian from forgotten lore. I exist at the crossroads of time and technology. Tell me, what tales do you carry?"]

    def generate_nlp2sd_prompt(self):
        self.sd_system_prompt = ["""
        You are tasked with converting natural language descriptions into specific prompts suitable for generating images. The objective is to extract key visual elements and themes from the description and format them into a clear, concise prompt that can be used for image generation. Avoid any elements that are not directly related to the visual representation.
        """]
        self.sd_prompt_example_input = ["""
        A girl with shimmering golden hair and deep purple eyes is set against a stark black backdrop. 
        Illuminated by neon lights, her black armor contrasts with hints of glowing gold. 
        Mechanical intricacies replace her arms, reflecting a blend of man and machine. 
        Flames flicker nearby, their warmth juxtaposed with the cool metal of her form. Subtly, a halo casts a gentle luminescence from above.
        """,
                                        """
"A slender German noblewoman with blonde hair and blue eyes, exuding an aura of elegance and grace at all times."
                                     """]
        self.sd_prompt_example_output = [""""
        prompt:
ultra-detailed face close-up, 1girl, golden shimmering hair, deep purple eyes, neon-lit face, glowing gold highlights on face, facial emphasis, complete face view, clear facial features, halo luminescence above
Negative prompt:
full body, distant, NSFW, cartoon, lowres, bad anatomy, text, error, missing facial features, partial face, side view, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name, young, loli, elf, 3d, illustration ng_deepnegative_v1_75t
        """,
                                         """
prompt:
full frontal face, complete facial view, no obstructions, close-up portrait, slender German noblewoman, blonde hair, blue eyes, aura of elegance, timeless grace, best quality, ultra detailed, perfect lighting, masterpiece, extremely detailed face, detailed eyes, 8K High definition, Ultra Detailed, High quality texture, intricate details, detailed texture, finely detailed, high detail, extremely detailed cg, High quality shadow, Depth of field, Ray tracing, beautiful, ultra high res
Negative prompt:
partial face, side view, cropped face, profile view, full body, distant, NSFW, cartoon, lowres, bad anatomy, text, error, missing facial features, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name, young, loli, elf, 3d, illustration ng_deepnegative_v1_75t, low quality face, low quality eyes, low quality body, low detail clothes                                   
                                      """]
        self.sd_prompt_example_input_length = len(self.sd_prompt_example_input)


def test():
    character_description = """
    A girl with shimmering golden hair and deep purple eyes set against a stark black backdrop. 
    Illuminated by neon lights, her black armor contrasts with hints of glowing gold. 
    Mechanical intricacies replace her arms, reflecting a blend of man and machine. 
    Flames flicker nearby, their warmth juxtaposed with the cool metal of her form. 
    Subtly, a halo casts a gentle luminescence from above.
    """
    prompt = Prompt()
    prompt.call_prompt(character_description=character_description)
    print("sd_system:", prompt.sd_system_prompt)
    print("sd_example", prompt.sd_prompt_example_input, prompt.sd_prompt_example_output)
    print("chatbot_system", prompt.chatbot_system_prompt)
    print("chatbot_example", prompt.chatbot_prompt_example_input, prompt.chatbot_prompt_example_output)
