import os
import utils.consts as consts
from typing import List, Tuple

# Importações atualizadas para o novo formato LangChain
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, Runnable
from langchain_core.documents import Document

from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# Importações de modelos
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint

def model_hf_hub(model = consts.MODEL_TYPE_HF, temperature = consts.TEMPERATURE_BALANCED):
    huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")  # Busca o token do .env
    if not huggingfacehub_api_token:
        raise ValueError("O token HUGGINGFACEHUB_API_TOKEN não foi encontrado no ambiente.")


    llm = HuggingFaceEndpoint(repo_id = model,
                              temperature = temperature,
                              return_full_text = False,
                              max_new_tokens = consts.MAX_NEW_TOKENS_LONG,
                              huggingfacehub_api_token=huggingfacehub_api_token
                              )
    
    return llm

def model_openai(model = consts.MODEL_TYPE_OPENAI, temperature = consts.TEMPERATURE_BALANCED):
    llm = ChatOpenAI(mode = model, temperature = temperature)

    return llm

def model_ollama(model = consts.MODEL_TYPE_OLLAMA, temperature = consts.TEMPERATURE_BALANCED):
    llm  = ChatOllama(model=model, temperature=temperature, base_url=consts.OLLAMA_PATH)

    return llm

def model_response(user_query, chat_history, model_class):

    # Carregamento da LLM configurada
    if (model_class == consts.MODEL_CLASS_HF_HUB): llm = model_hf_hub()

    if (model_class == consts.MODEL_CLASS_OPEN_AI): llm = model_openai()

    if (model_class == consts.MODEL_CLASS_OLLAMA): llm = model_ollama()

    # Adequando pipeline
    user_prompt_template = "{input}"

    # Para modelos da hugging face, o formato do prompt do usuário muda
    if model_class == consts.MODEL_CLASS_HF_HUB:
        # O formato de prompt para HF é específico e mantido
        user_prompt_template = "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n{input}<|eot_id|><|start_header_id|>"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", consts.PROMPT_ASSISTANT_GENERAL),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", user_prompt_template)
    ])

    # A chain já usa o formato LCEL (pipe |)
    chain = prompt_template | llm | StrOutputParser()

    # Retorno da resposta (stream)
    return chain.stream({
        "chat_history": chat_history,
        "input": user_query,
        "language": consts.LANGUAGE_PT_BR
    })



def config_rag_chain(model_class, retriever, profile):

    # Carregamento da LLM configurada
    if (model_class == consts.MODEL_CLASS_HF_HUB): llm = model_hf_hub()

    if (model_class == consts.MODEL_CLASS_OPEN_AI): llm = model_openai()

    if (model_class == consts.MODEL_CLASS_OLLAMA): llm = model_ollama()

    token_s, token_e = "", ""

    # Para modelos da hugging face, o formato do prompt do usuário muda
    if model_class == consts.MODEL_CLASS_HF_HUB:
        token_s = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>"
        token_e = "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"

    # Prompt para reformulação da pergunta
    contextualize_q_system_prompt = "Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is."

    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", token_s + contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "Question: {input}" + token_e),
    ])

    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

    # Prompt para QA
    qa_system_prompt = consts.PROMPT_QA_TEMPLATE_DEV.replace("{input}", "{context}")

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", token_s + qa_system_prompt + token_e),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return rag_chain