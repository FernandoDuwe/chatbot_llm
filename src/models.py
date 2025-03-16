import consts

from langchain_core.prompts import MessagesPlaceholder

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

import torch
from langchain_huggingface import ChatHuggingFace
from langchain_community.llms import HuggingFaceHub

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

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



def config_rag_chain(model_class, retriever):

    # Carregamento da LLM configurada
    if (model_class == consts.MODEL_CLASS_HF_HUB): llm = model_hf_hub()

    if (model_class == consts.MODEL_CLASS_OPEN_AI): llm = model_openai()

    if (model_class == consts.MODEL_CLASS_OLLAMA): llm = model_ollama()

    token_s, token_e = "", ""

    # Para modelos da hugging face, o formato do prompt do usuário muda
    if (model_class == consts.MODEL_CLASS_HF_HUB):
        token_s, token_e = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>", "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"

    context_q_system_prompt = "Given then following chat history and the follow-up question wich might reference context in the chat history, formulate a standalone question wich can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is."
    context_q_system_prompt = token_s + context_q_system_prompt
    context_q_user_prompt = "Question: {input}" + token_e
    context_q_prompt = ChatPromptTemplate.from_messages([
        ("system", context_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", context_q_user_prompt)
    ])

    # Chain para contextualização
    histore_aware_retriever = create_history_aware_retriever(llm=llm, retriever = retriever, prompt = context_q_prompt)

    qa_prompt = PromptTemplate.from_template(token_s + consts.PROMPT_QA_TEMPLATE + token_e)

    qa_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(histore_aware_retriever, qa_chain)

    return rag_chain