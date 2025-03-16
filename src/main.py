import consts
import models
import assets_import

import os
import time

import streamlit as st # Gera a interface para consulta (Pode ser substituida)
from langchain_core.messages import AIMessage, HumanMessage # Mensagens no stream

from dotenv import load_dotenv

load_dotenv()

# Configuração do StreamLit
st.set_page_config(page_title=consts.MESSAGE_PAGE_TITLE, page_icon=consts.MESSAGE_PAGE_ICON)
st.title(consts.MESSAGE_TITLE)

vrModelClass = consts.MODEL_CLASS_HF_HUB

# Inicializando as variáveis globais
if ("chat_history" not in st.session_state):
    st.session_state.chat_history = [AIMessage(content=consts.MESSAGE_AI_STARTUP)]

if ("doc_list" not in st.session_state):
    st.session_state.doc_list = None

if ("retriever" not in st.session_state):
    st.session_state.retriever = None

# Renderizando as respostas em tela
for message in st.session_state.chat_history:
    # Se a mensagem foi gerada pela IA
    if (isinstance(message, AIMessage)):
        with st.chat_message("AI"):
            st.write(message.content)

    # Se a mensagem foi gerada pelo usuário
    if (isinstance(message, HumanMessage)):
        with st.chat_message("Human"):
            st.write(message.content)

start = time.time()

# Buscando a mensagem digitada pelo usuário
user_query = st.chat_input(consts.MESSAGE_INPUT_PLACEHOLDER)

# Se existe mensagem do usuário, envia para a AI
if ((user_query is not None) and (user_query != "")):
    st.session_state.chat_history.append(HumanMessage(content = user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        pdf_files = [f for f in os.listdir(consts.DIRECTORY_ASSETS) if f.lower().endswith(".pdf")]

        if (st.session_state.doc_list != pdf_files):
            st.session_state.doc_list = pdf_files
            st.session_state.retriever = assets_import.config_retriever_pdf(pdf_files)

        rag_chaing = models.config_rag_chain(vrModelClass, st.session_state.retriever)

        result = rag_chaing.invoke({"input": user_query, "chat_history": st.session_state.chat_history})

        resp = result['answer']

        st.write(resp)

        # Mostra a fonte
        sources = result['context']

        for idx, doc in enumerate(sources):
            source = doc.metadata['source']
            file = os.path.basename(source)
            page = doc.metadata.get('page', 'Página não especificada')

            ref = f":link: Fonte {idx}: *{file} - p. {page}*"

            with st.popover(ref):
                st.caption(doc.page_content)

    st.session_state.chat_history.append(AIMessage(content=resp))

end = time.time()

print("Tempo: ", end - start)