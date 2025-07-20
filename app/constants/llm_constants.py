"""
Author: nikhil.anand
Created at: 19/07/25
"""

# Tiny Llama Constants
TINY_LLAMA_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
TINY_LLAMA_MODEL_TEMPERATURE = 0.2
TINY_LLAMA_MODEL_MAX_NEW_TOKENS = 200
TINY_LLAMA_MODEL_DO_SAMPLE = False
TINY_LLAMA_MODEL_PERSONALIZATION_PROMPT = """
<|system|>
Personalize horoscopes in exactly 1-2 brief sentences. Maximum 15 words per sentence. DO NOT CROSS THIS LIMIT IN ANY CASE.
Use the person's name. NO signatures, NO "Best wishes", NO "[Your Name]", NO greetings. Just the horoscope content.
Example format: 
"[Name], today brings new opportunities for you. 
Your Leo energy will guide important decisions. 
Trust your instincts when choosing your path."
<|user|>
Rewrite this horoscope personally for {name}: {horoscope}
<|assistant|>
{name}, 
"""

# GPT2 Model Constants
GPT2_MODEL = "gpt2"
GPT2_MODEL_TEMPERATURE = 0.3
GPT2_MODEL_MAX_NEW_TOKENS = 150
GPT2_MODEL_DO_SAMPLE = True
GPT2_MODEL_PERSONALIZATION_PROMPT = """
Personalize this horoscope for {name} in exactly 3 brief sentences. 
Maximum 15 words per sentence. Use the person's name. NO signatures, NO "Best wishes", NO "[Your Name]", NO greetings.
Just the horoscope content.
Original horoscope: {horoscope}
{name}, """

# Translation Model Constants
HELSINKI_MODEL = "Helsinki-NLP/opus-mt-en-hi"
INDIC_TRANS2_MODEL = "ai4bharat/indictrans2-en-indic-1B"
INDIC_TRANS2_TOKENIZER = "ai4bharat/indictrans2-en-indic-1B"
