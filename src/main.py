import consts as consts
import models as models

import streamlit as st # Gera a interface para consulta (Pode ser substituida)
from langchain_core.messages import AIMessage, HumanMessage # Mensagens no stream

from dotenv import load_dotenv

load_dotenv()

# Configuração do StreamLit
st.set_page_config(page_title=consts.MESSAGE_PAGE_TITLE, page_icon=consts.MESSAGE_PAGE_ICON)
st.title(consts.MESSAGE_TITLE)

vrModelClass = consts.MODEL_CLASS_HF_HUB

# Se não existe histórico de conversa, cria uma nova mensagem com origem na AI
if ("chat_history" not in st.session_state):
    st.session_state.chat_history = [AIMessage(content=consts.MESSAGE_AI_STARTUP)]

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

# Buscando a mensagem digitada pelo usuário
user_query = st.chat_input(consts.MESSAGE_INPUT_PLACEHOLDER)

# Se existe mensagem do usuário, envia para a AI
if ((user_query is not None) and (user_query != "")):
    st.session_state.chat_history.append(HumanMessage(content = user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        resp = st.write_stream(models.model_response(user_query, st.session_state.chat_history, vrModelClass))

        st.session_state.chat_history.append(AIMessage(content = resp))