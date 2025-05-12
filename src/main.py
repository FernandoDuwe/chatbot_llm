import utils.consts as consts
import utils.models as models
import utils.assets_import as assets_import
import utils.youtube_utils as youtube_utils
import utils.profiles as profiles

import os
import time

import streamlit as st # Gera a interface para consulta (Pode ser substituida)
from langchain_core.messages import AIMessage, HumanMessage # Mensagens no stream

from dotenv import load_dotenv

load_dotenv()

# Configuração do StreamLit
st.set_page_config(page_title=consts.MESSAGE_PAGE_TITLE, page_icon=consts.MESSAGE_PAGE_ICON)
st.title(consts.MESSAGE_TITLE)

# Adicionando botões para seleção de perfil
if "selected_profile" not in st.session_state:
    st.session_state.selected_profile = None

st.subheader("Com qual especialista você deseja conversar?:")

col1, col2 = st.columns(2)

profileList = profiles.get_profiles()

for idx, option in enumerate(profileList):
    if idx % 2 == 0:  # Alternar entre col1 e col2
        with col1:
            if st.button(option["name"]):  # Exibe o botão com o rótulo do JSON
                st.session_state.selected_profile = idx
    else:
        with col2:
            if st.button(option["name"]):  # Exibe o botão com o rótulo do JSON
                st.session_state.selected_profile = idx


# Verifica se o perfil foi selecionado
if st.session_state.selected_profile is None:
    st.warning("Por favor, selecione um especialista para continuar.")
    st.stop()

# Exibe o perfil selecionado

st.success(f"Especialista selecionado: " + profiles.get_profile_by_index(st.session_state.selected_profile)["name"])

vrModelClass = consts.MODEL_CLASS_HF_HUB

# Inicializando as variáveis globais
if ("chat_history" not in st.session_state):
    st.session_state.chat_history = [AIMessage(content=profiles.get_profile_by_index(st.session_state.selected_profile)["startup_message"])]

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
        if (st.session_state.retriever is None):
            st.session_state.retriever = assets_import.config_retriever_from_index_file(st.session_state.selected_profile)

        rag_chaing = models.config_rag_chain(vrModelClass, st.session_state.retriever, st.session_state.selected_profile)

        result = rag_chaing.invoke({"input": user_query, "chat_history": st.session_state.chat_history})

        resp = result['answer']

        st.write(resp)

        # Mostra a fonte
        sources = result['context']

        sources_rendered = []

        for idx, doc in enumerate(sources):
            source = doc.metadata['source']          
            file = os.path.basename(source)

            # Para não repetir os itens
            if (file in sources_rendered): continue

            sources_rendered.append(file)

            nome, extensao = os.path.splitext(file)

            # renderizando as respostas
            if (extensao == ".pdf"):
                page = doc.metadata.get('page', 'Página não especificada')

                ref = f":link: *{file} - p. {page}*"

                with st.popover(ref):
                    st.caption(doc.page_content)

            if (extensao == ".docx"):
                page = doc.metadata.get('page', 'Página não especificada')

                ref = f":link: *{file} - p. {page}*"

                with st.popover(ref):
                    st.caption(doc.page_content)

            if (extensao == ".ytb"):
                ref = f":link: *{youtube_utils.youtube_get_title(nome)} - Youtube*"
                
                with st.popover(ref):
                    st.video(consts.YOUTUBE_READ_VIDEO + file)

    st.session_state.chat_history.append(AIMessage(content=resp))

end = time.time()

print("Tempo: ", end - start)