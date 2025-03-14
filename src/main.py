# Gera a interface para consulta (Pode ser substituida)
import streamlit as st


from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import torch
from langchain_huggingface import ChatHuggingFace
from langchain_community.llms import HuggingFaceHub

from dotenv import load_dotenv

load_dotenv()

# Configuração do StreamLit
st.set_page_config(page_title="Seu assistente virtual", page_icon="")
st.title("Seu assistente virtual")
# st.button("Botão")
# st.chat_input("Digite sua mensagem")

model_class = "hf_hub" # hf_hub, openai, ollama

# temperatura baixa = baixa criatividade do modelo
def model_hf_hub(model = "meta-llama/Meta-Llama-3-8B-Instruct", temperature = 0.1):
    llm = HuggingFaceHub(repo_id = model, 
                         model_kwargs={
                                        "temperature": temperature,
                                        "return_full_text": False,
                                        "max_new_tokens": 512
                                        })
    
    return llm

def model_openai(model = "gpt-40-mini", temperature = 0.1):
    llm = ChatOpenAI(mode = model, temperature = temperature)

    return llm

def model_ollama(model = "phi3", temperature = 0.1):
    llm  = ChatOllama(model = model, temperature = temperature)

    return llm

def model_response(user_query, chat_history, model_class):

    # Carregamento da LLM configurada
    if (model_class == "hf_hub"): llm = model_hf_hub()

    if (model_class == "openai"): llm = model_openai()

    if (model_class == "ollama"): llm = model_ollama()

    # Definição dos prompts
    system_prompt = """
        Vocẽ é um assistente prestativo e está respondendo perguntas gerais. Responda em {language}
"""

    language = "português"

    # Adequando pipeline

    user_prompt = "{input}"

    # para modelos da hugging face, o formato do prompt do usuário muda
    if (model_class.startswith("hf")):
        user_prompt = "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n{input}<|eot_id|><|start_header_id|>"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", user_prompt)
    ])

    # Criação da chain
    chain = prompt_template | llm | StrOutputParser()

    # Retorno da resposta
    return chain.stream({
        "chat_history": chat_history,
        "input": user_query,
        "language": language
    })

# Se já existe um histórico de chat na sessão
if ("chat_history" not in st.session_state):
    st.session_state.chat_history = [AIMessage(content="Olá, sou o seu assistente virtual. Como posso lhe ajudar?")]

for message in st.session_state.chat_history:
    # Se a mensagem foi gerada pela IA
    if (isinstance(message, AIMessage)):
        with st.chat_message("AI"):
            st.write(message.content)

    if (isinstance(message, HumanMessage)):
        with st.chat_message("Human"):
            st.write(message.content)

user_query = st.chat_input("Digite sua mensagem aqui")

if ((user_query is not None) and (user_query != "")):
    st.session_state.chat_history.append(HumanMessage(content = user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        resp = st.write_stream(model_response(user_query, st.session_state.chat_history, model_class))

        st.session_state.chat_history.append(AIMessage(content = resp))