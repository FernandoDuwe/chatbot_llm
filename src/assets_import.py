import os
import consts

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# Esta função lerá os arquivos de um diretório e salvará em um formato que possa ser lido pela IA
def config_retriever_pdf(doc_list):
    docs = []

    print(doc_list)

    # lendo os documentos e carregando
    for file in doc_list:
        file_path = os.path.join(consts.DIRECTORY_ASSETS, file)

        loader = PyPDFLoader(file_path)

        docs.extend(loader.load())

    # Divisão em pedaços de texto / split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    splits = text_splitter.split_documents(docs)

    # Embedding
    embeddings = HuggingFaceEmbeddings(model_name = consts.EMBEDDING_BAAI)

    # Armazenamento
    vectorstore = FAISS.from_documents(splits, embeddings)
    vectorstore.save_local(consts.DIRECTORY_VECTORSTORE)

    # Configuração do retriever
    retriever = vectorstore.as_retriever(search_type = "mmr", search_kwargs={'k': 3, 'fetch_k': 4})

    return retriever