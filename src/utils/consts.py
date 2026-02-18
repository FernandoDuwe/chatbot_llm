OLLAMA_PATH = "http://127.0.0.1:11434"

# Profiles
PROFILE_DEVELOPER = 0
PROFILE_SPECIALIST = 1

# Model classes
MODEL_CLASS_HF_HUB  = 0
MODEL_CLASS_OPEN_AI = 1
MODEL_CLASS_OLLAMA  = 2

# Models
MODEL_TYPE_HF     = "microsoft/phi-4"  #"meta-llama/Meta-Llama-3-8B-Instruct"
MODEL_TYPE_OPENAI = "gpt-40-mini"
MODEL_TYPE_OLLAMA = "qwen2.5-coder:0.5b"  # "llama3.2:3b" # "llama3.1:8b"

MODEL_TYPE_HF_JURIDICO = "DIACDE/NER_identificacao_termos_juridicos_complexos_TJGO"

# Embeddings
EMBEDDING_BAAI = "BAAI/bge-m3"
EMBEDDING_FAST = "sentence-transformers/all-MiniLM-L6-v2"  # Alternativa mais rápida e leve

# Temperature
TEMPERATURE_LOW_CREATIVITY = 0.1 # temperatura baixa = baixa criatividade do modelo
TEMPERATURE_BALANCED = 0.5 # temperatura equilibrada para melhor qualidade

# Language
LANGUAGE_PT_BR = "Português do Brasil"

# Generation parameters
MAX_NEW_TOKENS_SHORT = 512  # Para respostas curtas
MAX_NEW_TOKENS_MEDIUM = 1024  # Para respostas médias
MAX_NEW_TOKENS_LONG = 2048  # Para respostas longas
TOP_P = 0.9  # Para diversidade controlada nas respostas
TOP_K = 50  # Limita tokens a considerar

# Messages
MESSAGE_PAGE_TITLE        = "Seu assistente virtual"
MESSAGE_PAGE_ICON         = ""
MESSAGE_TITLE             = "Seu assistente virtual"
MESSAGE_AI_STARTUP        = "Olá, sou o seu assistente virtual. Como posso lhe ajudar?"
MESSAGE_AI_STARTUP_JURIDICO = "Olá, sou o seu assistente virtual jurídico. Como posso lhe ajudar?"
MESSAGE_AI_STARTUP_DEVELOPER = "Olá, sou o seu desenvolvedor virtual. Como posso lhe ajudar?"
MESSAGE_INPUT_PLACEHOLDER = "Digite sua mensagem aqui"

# Prompts
PROMPT_ASSISTANT_GENERAL = """Você é um assistente prestativo. Responda a todas as perguntas de forma concisa e precisa."""

PROMPT_QA_TEMPLATE_DEV = """Você é um especialista em desenvolvimento de software com profundo conhecimento em Python.

INSTRUÇÕES:
1. Use o contexto recuperado como base para exemplos de código
2. Forneça soluções práticas e testadas
3. Explique o "por quê" antes do "como"
4. Use formatação de código com sintaxe highlighting (```python ... ```)
5. Inclua comentários no código explicando pontos-chave
6. Se houver múltiplas abordagens, compare-as
7. Cite a fonte ou arquivo do contexto
8. Se não souber, admita e sugira recursos para aprender
9. Crie exemplos, se necessário

Pergunta: {input}

Contexto do repositório:
{context}

Resposta técnica detalhada em português:"""

# Directories and files
DIRECTORY_ASSETS = "./assets/"
DIRECTORY_TEMP = "./temp/"
DIRECTORY_VECTORSTORE = "./assets/vectorstore/db_faiss"
DIRECTORY_VECTORSTORE_DEV = "./assets/vectorstore_dev/db_faiss"
DIRECTORY_VECTORSTORE_SPC = "./assets/vectorstore_spc/db_faiss"
FAISS_FILE = "./assets/vectorstore/db_faiss"
FAISS_FILE_DEV = "./assets/vectorstore_dev/db_faiss"
FAISS_FILE_SPC = "./assets/vectorstore_spc/db_faiss"

PROFILE_CONFIG = "./config/profiles.json"

# Youtube read URL
YOUTUBE_READ_VIDEO = "https://www.youtube.com/watch?v="
YOUTUBE_READ_PLAYLIST = "https://www.youtube.com/watch?list="