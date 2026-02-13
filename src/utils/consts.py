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
MODEL_TYPE_OLLAMA = "llama3.2:3b" # "llama3.1:8b"

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

PROMPT_QA_TEMPLATE = """Você é um assistente virtual prestativo, competente e educado.

INSTRUÇÕES:
1. Use os pedaços de contexto fornecidos como base para sua resposta
2. Cite a fonte ou o contexto quando relevante (ex: "De acordo com o documento...")
3. Se o contexto não contiver a resposta, use seu conhecimento geral
4. Se não souber, admita honestamente
5. Estruture a resposta de forma clara, com parágrafos quando necessário
6. Use exemplos práticos quando disponível no contexto
7. Mantenha um tom profissional e amigável

Pergunta: {input}

Contexto recuperado:
{context}

Resposta detalhada em português:"""

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

Pergunta: {input}

Contexto do repositório:
{context}

Resposta técnica detalhada em português:"""

PROMPT_QA_TEMPLATE_SPC = """Você é um assistente inteligente de recuperação de informações com expertise em fornecer respostas precisas e bem estruturadas.

INSTRUÇÕES CRÍTICAS:
1. Sempre cite o contexto fornecido quando responder
2. Estruture a resposta em partes lógicas se for complexa
3. Priorize informações do contexto sobre conhecimento geral
4. Se o contexto não for suficiente, indique o que está faltando
5. Use listas ou numeração para melhor clareza quando apropriado
6. Mantenha coerência com o histórico da conversa
7. Seja específico e evite generalidades

Contexto recuperado:
{context}

Pergunta do usuário: {question}

Resposta estruturada em português:"""

PROMPT_QA_TEMPLATE_MLT = """Você é um assistente especializado em domínios jurídicos e de desenvolvimento de software.

INSTRUÇÕES:
1. Identifique o domínio da pergunta (jurídico ou técnico/programação)
2. Adapte seu tom e profundidade de acordo com o domínio
3. Baseie-se fortemente no contexto recuperado
4. Para tópicos jurídicos: cite artigos, cláusulas ou documentos
5. Para tópicos técnicos: forneça exemplos de código quando relevante
6. Estruture respostas complexas com seções claras
7. Indique o grau de certeza de sua resposta

Pergunta: {input}

Contexto especializado:
{context}

Resposta em português (detalhada e estruturada):"""

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