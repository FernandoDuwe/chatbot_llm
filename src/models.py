import consts as consts

from langchain_core.prompts import MessagesPlaceholder

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import torch
from langchain_huggingface import ChatHuggingFace
from langchain_community.llms import HuggingFaceHub

def model_hf_hub(model = consts.MODEL_TYPE_HF, temperature = consts.TEMPERATURE_LOW_CREATIVITY):
    llm = HuggingFaceHub(repo_id = model, 
                         model_kwargs={
                                        "temperature": temperature,
                                        "return_full_text": False,
                                        "max_new_tokens": 512
                                        })
    
    return llm

def model_openai(model = consts.MODEL_TYPE_OPENAI, temperature = consts.TEMPERATURE_LOW_CREATIVITY):
    llm = ChatOpenAI(mode = model, temperature = temperature)

    return llm

def model_ollama(model = consts.MODEL_TYPE_OLLAMA, temperature = consts.TEMPERATURE_LOW_CREATIVITY):
    llm  = ChatOllama(model = model, temperature = temperature)

    return llm

def model_response(user_query, chat_history, model_class):

    # Carregamento da LLM configurada
    if (model_class == consts.MODEL_CLASS_HF_HUB): llm = model_hf_hub()

    if (model_class == consts.MODEL_CLASS_OPEN_AI): llm = model_openai()

    if (model_class == consts.MODEL_CLASS_OLLAMA): llm = model_ollama()

    # Adequando pipeline
    user_prompt = "{input}"

    # Para modelos da hugging face, o formato do prompt do usuário muda
    if (model_class == consts.MODEL_CLASS_HF_HUB):
        user_prompt = "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n{input}<|eot_id|><|start_header_id|>"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", consts.PROMPT_ASSISTANT_GENERAL),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", user_prompt)
    ])

    # Criação da chain
    chain = prompt_template | llm | StrOutputParser()

    # Retorno da resposta
    return chain.stream({
        "chat_history": chat_history,
        "input": user_query,
        "language": consts.LANGUAGE_PT_BR
    })