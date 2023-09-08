import re


def extract_prompts(text):
    prompt_pattern = re.compile(r'(?i)Prompt:\s*(.*?)(?=Negative prompt:|$)', re.S)
    negative_prompt_pattern = re.compile(r'(?i)Negative prompt:\s*(.*)', re.S)

    prompt_match = prompt_pattern.search(text)
    negative_prompt_match = negative_prompt_pattern.search(text)

    prompt = prompt_match.group(1).strip() if prompt_match else None
    negative_prompt = negative_prompt_match.group(1).strip() if negative_prompt_match else None

    return prompt, negative_prompt
