# Profiles
PROFILE_DEVELOPER = 0
PROFILE_SPECIALIST = 1

# Model classes
MODEL_CLASS_HF_HUB  = 0
MODEL_CLASS_OPEN_AI = 1
MODEL_CLASS_OLLAMA  = 2

# Models
MODEL_TYPE_HF     = "meta-llama/Meta-Llama-3-8B-Instruct"
MODEL_TYPE_OPENAI = "gpt-40-mini"
MODEL_TYPE_OLLAMA = "phi3"

MODEL_TYPE_HF_JURIDICO = "DIACDE/NER_identificacao_termos_juridicos_complexos_TJGO"

# Embeddings
EMBEDDING_BAAI = "BAAI/bge-m3"

# Temperature
TEMPERATURE_LOW_CREATIVITY = 0.1 # temperatura baixa = baixa criatividade do modelo

# Language
LANGUAGE_PT_BR = "português"

# Messages
MESSAGE_PAGE_TITLE        = "Seu assistente virtual"
MESSAGE_PAGE_ICON         = ""
MESSAGE_TITLE             = "Seu assistente virtual"
MESSAGE_AI_STARTUP        = "Olá, sou o seu assistente virtual. Como posso lhe ajudar?"
MESSAGE_AI_STARTUP_JURIDICO = "Olá, sou o seu assistente virtual jurídico. Como posso lhe ajudar?"
MESSAGE_AI_STARTUP_DEVELOPER = "Olá, sou o seu desenvolvedor virtual. Como posso lhe ajudar?"
MESSAGE_INPUT_PLACEHOLDER = "Digite sua mensagem aqui"

# Prompts
PROMPT_ASSISTANT_GENERAL = """
        Vocẽ é um assistente prestativo e está respondendo perguntas gerais. Responda em {language}
"""

PROMPT_QA_TEMPLATE = """Você é um assistente virtual prestativo e está respondendo perguntas gerais.
Use os seguintes pedaços de contexto recuperado para responder à pergunta.
Se você não sabe a resposta, apenas diga que não sabe. Mantenha a resposta concisa.
Responda em português. \n\n
Pergunta: {input} \n
Contexto: {context}"""

PROMPT_QA_TEMPLATE_DEV = """Você é um assistente virtual prestativo e está respondendo perguntas relacionadas a desenvolvimento de software.
Use os seguintes pedaços de contexto recuperado para responder à pergunta.
Se você não sabe a resposta, apenas diga que não sabe. Mantenha a resposta concisa.
Responda em português. \n\n
Pergunta: {input} \n
Contexto: {context}"""

PROMPT_QA_TEMPLATE_SPC = """Você é um assistente virtual prestativo e está respondendo perguntas jurídicas.
Use os seguintes pedaços de contexto recuperado para responder à pergunta.
Se você não sabe a resposta, apenas diga que não sabe. Mantenha a resposta concisa.
Responda em português. \n\n
Pergunta: {input} \n
Contexto: {context}"""

# Directories and files
DIRECTORY_ASSETS = "./assets/"
DIRECTORY_TEMP = "./temp/"
DIRECTORY_VECTORSTORE = "./assets/vectorstore/db_faiss"
DIRECTORY_VECTORSTORE_DEV = "./assets/vectorstore_dev/db_faiss"
DIRECTORY_VECTORSTORE_SPC = "./assets/vectorstore_spc/db_faiss"
FAISS_FILE = "./assets/vectorstore/db_faiss"
FAISS_FILE_DEV = "./assets/vectorstore_dev/db_faiss"
FAISS_FILE_SPC = "./assets/vectorstore_spc/db_faiss"

# Youtube read URL
YOUTUBE_READ_VIDEO = "https://www.youtube.com/watch?v="
YOUTUBE_READ_PLAYLIST = "https://www.youtube.com/watch?list="