import os
import utils.consts as consts
import utils.profiles as profiles

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader

# Esta função lerá os arquivos de um diretório e salvará em um formato que possa ser lido pela IA
def config_retriever(doc_list, profile):
    docs = []

    # lendo os documentos e carregando
    for file in doc_list:
        file_path = os.path.join(consts.DIRECTORY_ASSETS, file)

        nome, extensao = os.path.splitext(file_path)

        print(nome, " ", extensao)

        if (extensao == ".pdf"):
            loader = PyPDFLoader(file_path)

        if (extensao == ".py"):
            loader = TextLoader(file_path, encoding="latin-1")

        if (extensao == ".ytb"):
            loader = TextLoader(file_path)

        if (extensao == ".wbt"):
            loader = TextLoader(file_path)

        if (extensao == ".docx"):
            loader = Docx2txtLoader(file_path)

        if (extensao == ".mp4t"):
            loader = TextLoader(file_path)

        print(" lendo o arquivo ", file_path)

        docs.extend(loader.load())

    print(" efetuando o split")

    # Divisão em pedaços de texto / split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    splits = text_splitter.split_documents(docs)

    print(" embedding...")

    # Embedding
    embeddings = HuggingFaceEmbeddings(model_name = consts.EMBEDDING_FAST)

    print(" armazenando....")

    # Armazenamento
    vectorstore = FAISS.from_documents(splits, embeddings)

    file_store = profiles.get_profile_by_index(profile)["faiss_db"]

    print(" arquivo: " + file_store)

    vectorstore.save_local(file_store)

    print ("    configurando o retriever")

    # Configuração do retriever
    retriever = vectorstore.as_retriever(search_type = "similarity", search_kwargs={'k': 2, 'fetch_k': 7})

    print ("    retriever feito")

    return retriever

def config_retriever_from_index_file(profile):
    embeddings = HuggingFaceEmbeddings(model_name = consts.EMBEDDING_FAST)


    file_store = profiles.get_profile_by_index(profile)["faiss_db"]

    vectorstore = FAISS.load_local(file_store, embeddings,allow_dangerous_deserialization=True)

    # Usar 'similarity' é mais rápido que 'mmr'. Reduzir k para 2-3 documentos.
    # Mudar de mmr (mais lento, mas diverso) para similarity (mais rápido)
    retriever = vectorstore.as_retriever(search_type = "similarity", search_kwargs={'k': 2})

    return retriever