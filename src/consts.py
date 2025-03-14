# Model classes
MODEL_CLASS_HF_HUB  = 0
MODEL_CLASS_OPEN_AI = 1
MODEL_CLASS_OLLAMA  = 2

# Models
MODEL_TYPE_HF     = "meta-llama/Meta-Llama-3-8B-Instruct"
MODEL_TYPE_OPENAI = "gpt-40-mini"
MODEL_TYPE_OLLAMA = "phi3"

# Temperature
TEMPERATURE_LOW_CREATIVITY = 0.1 # temperatura baixa = baixa criatividade do modelo

# Language
LANGUAGE_PT_BR = "português"

# Messages
MESSAGE_PAGE_TITLE        = "Seu assistente virtual"
MESSAGE_PAGE_ICON         = ""
MESSAGE_TITLE             = "Seu assistente virtual"
MESSAGE_AI_STARTUP        = "Olá, sou o seu assistente virtual. Como posso lhe ajudar?"
MESSAGE_INPUT_PLACEHOLDER = "Digite sua mensagem aqui"

# Prompts
PROMPT_ASSISTANT_GENERAL = """
        Vocẽ é um assistente prestativo e está respondendo perguntas gerais. Responda em {language}
"""