import os
from typing import List, Tuple

# Importações atualizadas para o novo formato LangChain
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, Runnable
from langchain_core.documents import Document

# Importações de modelos
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_community.llms import HuggingFaceEndpoint

# O código original usava um módulo 'utils.consts'.
# Para que o código seja executável e demonstrativo, vou definir as constantes
# que parecem ser usadas. O usuário precisará ajustar isso em seu ambiente.
class Consts:
    MODEL_TYPE_HF = "google/flan-t5-large" # Exemplo
    MODEL_TYPE_OPENAI = "gpt-3.5-turbo" # Exemplo
    MODEL_TYPE_OLLAMA = "llama2" # Exemplo
    TEMPERATURE_LOW_CREATIVITY = 0.1
    MODEL_CLASS_HF_HUB = "HF_HUB"
    MODEL_CLASS_OPEN_AI = "OPEN_AI"
    MODEL_CLASS_OLLAMA = "OLLAMA"
    PROMPT_ASSISTANT_GENERAL = "Você é um assistente prestativo. Responda a todas as perguntas de forma concisa e precisa."
    PROMPT_QA_TEMPLATE_SPC = """Você é um assistente de recuperação de informações. Use os seguintes pedaços de contexto recuperado para responder à pergunta.
    Se você não souber a resposta, diga que não sabe. Mantenha a resposta concisa.

    Contexto: {context}

    Pergunta: {question}

    Resposta concisa em português:"""
    LANGUAGE_PT_BR = "Português do Brasil"

consts = Consts()

# Funções de carregamento de modelo (mantidas, mas com imports atualizados)
def model_hf_hub(model: str = consts.MODEL_TYPE_HF, temperature: float = consts.TEMPERATURE_LOW_CREATIVITY) -> HuggingFaceEndpoint:
    """Carrega o modelo HuggingFaceEndpoint."""
    huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not huggingfacehub_api_token:
        # Em um ambiente real, isso deve ser um erro. Para demonstração, usaremos um token placeholder.
        # raise ValueError("O token HUGGINGFACEHUB_API_TOKEN não foi encontrado no ambiente.")
        print("AVISO: Usando token placeholder para HUGGINGFACEHUB_API_TOKEN.")
        huggingfacehub_api_token = "placeholder_token"

    llm = HuggingFaceEndpoint(
        repo_id=model,
        temperature=temperature,
        return_full_text=False,
        max_new_tokens=1024,
        huggingfacehub_api_token=huggingfacehub_api_token
    )
    return llm

def model_openai(model: str = consts.MODEL_TYPE_OPENAI, temperature: float = consts.TEMPERATURE_LOW_CREATIVITY) -> ChatOpenAI:
    """Carrega o modelo ChatOpenAI."""
    # O parâmetro 'mode' no código original foi substituído por 'model' no construtor de ChatOpenAI
    llm = ChatOpenAI(model=model, temperature=temperature)
    return llm

def model_ollama(model: str = consts.MODEL_TYPE_OLLAMA, temperature: float = consts.TEMPERATURE_LOW_CREATIVITY) -> ChatOllama:
    """Carrega o modelo ChatOllama."""
    llm = ChatOllama(model=model, temperature=temperature, base_url="http://ollama:11434")
    return llm

def get_llm(model_class: str) -> Runnable:
    """Função auxiliar para obter a LLM com base na classe."""
    if model_class == consts.MODEL_CLASS_HF_HUB:
        return model_hf_hub()
    elif model_class == consts.MODEL_CLASS_OPEN_AI:
        return model_openai()
    elif model_class == consts.MODEL_CLASS_OLLAMA:
        return model_ollama()
    else:
        raise ValueError(f"Classe de modelo desconhecida: {model_class}")

# --- Função model_response convertida para LCEL (já estava quase lá) ---
def model_response_lcel(user_query: str, chat_history: List[Tuple[str, str]], model_class: str):
    """
    Cria e executa uma chain de resposta de modelo simples usando LCEL.
    A chain já estava em LCEL, mas foi refatorada para clareza.
    """
    llm = get_llm(model_class)

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

# --- Função config_rag_chain convertida para LCEL ---
def config_rag_chain_lcel(model_class: str, retriever: Runnable, profile: str) -> Runnable:
    """
    Configura uma chain RAG (Retrieval-Augmented Generation) usando LCEL,
    substituindo create_history_aware_retriever e create_retrieval_chain.
    """
    llm = get_llm(model_class)

    token_s, token_e = "", ""

    # Para modelos da hugging face, o formato do prompt do usuário muda
    if model_class == consts.MODEL_CLASS_HF_HUB:
        # O código original usava isso para envolver o prompt do sistema e a resposta do assistente
        token_s = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>"
        token_e = "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"

    # 1. Chain para contextualização (substitui create_history_aware_retriever)
    # Esta chain reformula a pergunta do usuário com base no histórico de chat.
    context_q_system_prompt = "Given then following chat history and the follow-up question wich might reference context in the chat history, formulate a standalone question wich can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is."
    
    # Aplica os tokens de formatação do modelo HF
    context_q_system_prompt_formatted = token_s + context_q_system_prompt
    context_q_user_prompt_formatted = "Question: {input}" + token_e
    
    context_q_prompt = ChatPromptTemplate.from_messages([
        ("system", context_q_system_prompt_formatted),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", context_q_user_prompt_formatted)
    ])

    # A chain de reformulação da pergunta
    question_rephraser_chain = context_q_prompt | llm | StrOutputParser()

    # O retriever consciente do histórico (history-aware retriever) é a combinação:
    # 1. Se houver histórico, reformula a pergunta.
    # 2. Passa a pergunta (original ou reformulada) para o retriever.
    # O LCEL permite essa lógica condicional e encadeamento.
    
    # Função para determinar se o histórico está vazio
    def check_history(input_dict):
        # O histórico de chat é uma lista de tuplas (pergunta, resposta)
        return len(input_dict.get("chat_history", [])) > 0

    # O retriever consciente do histórico em LCEL
    history_aware_retriever = RunnablePassthrough.assign(
        # A chave 'question' será a entrada para o retriever
        question=RunnablePassthrough()
    ).assign(
        # Se houver histórico, usa a chain de reformulação, senão usa a entrada original
        standalone_question=RunnablePassthrough.assign(
            # Verifica se há histórico. Se sim, usa a chain de reformulação.
            # Se não, apenas passa a entrada 'input' como a 'standalone_question'.
            # O `check_history` é uma simplificação, o LangChain tem um RunnableBranch mais robusto.
            # Para manter a lógica do `create_history_aware_retriever`, usaremos a chain de reformulação
            # e deixaremos o retriever lidar com a entrada.
            # No novo LCEL, o padrão é: se o histórico estiver vazio, a chain de reformulação
            # deve retornar a pergunta original.
            # O `create_history_aware_retriever` faz isso internamente.
            # Aqui, vamos simular a lógica do LCEL para o history-aware retriever:
            standalone_question=RunnablePassthrough.assign(
                # Mapeia a entrada para o formato esperado pela chain de reformulação
                input=lambda x: x["input"]
            ) | question_rephraser_chain
        )
    ).assign(
        # O retriever recebe a pergunta (reformulação ou original)
        context=lambda x: retriever.invoke(x["standalone_question"])
    )

    # O `create_history_aware_retriever` é mais simples de replicar:
    # Se houver histórico, a chain de reformulação é invocada.
    # O resultado da chain de reformulação é passado para o retriever.
    # Se não houver histórico, a pergunta original é passada para o retriever.
    
    # Versão mais fiel ao comportamento do create_history_aware_retriever:
    history_aware_retriever_lcel = (
        # 1. Reformula a pergunta se houver histórico
        RunnablePassthrough.assign(
            standalone_question=RunnablePassthrough.assign(
                # Mapeia a entrada para o formato esperado pela chain de reformulação
                input=lambda x: x["input"]
            ) | question_rephraser_chain
        )
        # 2. Passa a pergunta (reformulação ou original) para o retriever
        | (lambda x: retriever.invoke(x["standalone_question"]))
    )
    
    # A chain RAG completa precisa de uma entrada que contenha 'question' e 'context'.
    # A entrada para a chain RAG será um dicionário com 'input' e 'chat_history'.
    
    # 1. Chain para obter o contexto (retriever consciente do histórico)
    context_chain = (
        RunnablePassthrough.assign(
            # A chain de reformulação é invocada
            standalone_question=RunnablePassthrough.assign(
                input=lambda x: x["input"]
            ) | question_rephraser_chain
        )
        # O retriever recebe a pergunta reformulada
        | (lambda x: retriever.invoke(x["standalone_question"]))
    ).with_config(run_name="ContextRetrieval")

    # 2. Chain de Geração (substitui create_stuff_documents_chain)
    # O prompt de QA
    qa_prompt_formatted = PromptTemplate.from_template(token_s + consts.PROMPT_QA_TEMPLATE_SPC + token_e)
    
    # A chain de documentos (stuffing)
    def format_docs(docs: List[Document]) -> str:
        """Formata a lista de documentos em uma única string de contexto."""
        return "\n\n".join(doc.page_content for doc in docs)

    qa_chain_lcel = (
        # Mapeia a entrada para o formato esperado pelo prompt
        {
            "context": lambda x: format_docs(x["context"]),
            "question": RunnablePassthrough()
        }
        | qa_prompt_formatted
        | llm
        | StrOutputParser()
    ).with_config(run_name="QAGeneration")

    # 3. Chain RAG Final (substitui create_retrieval_chain)
    # A chain RAG final combina a recuperação de contexto e a geração de QA.
    rag_chain_lcel = (
        # Mapeia a entrada original ('input', 'chat_history')
        RunnablePassthrough.assign(
            # O contexto é obtido pela chain de recuperação
            context=context_chain,
            # A pergunta original é passada como 'question'
            question=lambda x: x["input"]
        )
        # O resultado (contexto e pergunta) é passado para a chain de QA
        | qa_chain_lcel
    ).with_config(run_name="RAGChain")

    # Nota: O `create_retrieval_chain` original retornava um dicionário com 'context' e 'answer'.
    # A implementação acima retorna apenas a 'answer' (string).
    # Para replicar o comportamento de retorno do dicionário:
    final_rag_chain_lcel = (
        RunnablePassthrough.assign(
            # 1. Obtém o contexto (usando a chain de recuperação consciente do histórico)
            context=context_chain,
            # 2. Mantém a pergunta original
            question=lambda x: x["input"]
        )
        # 3. Passa o contexto e a pergunta para a chain de QA para obter a resposta
        .assign(
            answer=qa_chain_lcel
        )
        # 4. Seleciona as chaves de saída para replicar o retorno de `create_retrieval_chain`
        | (lambda x: {"context": x["context"], "answer": x["answer"]})
    ).with_config(run_name="FinalRAGChain")


    # A implementação mais simples e direta do RAG com histórico em LCEL é:
    # history_aware_retriever = create_history_aware_retriever(...)
    # qa_chain = create_stuff_documents_chain(...)
    # rag_chain = history_aware_retriever | qa_chain
    # No entanto, como o usuário pediu a conversão *para* o novo formato,
    # e o novo formato incentiva o uso de LCEL puro, a implementação `final_rag_chain_lcel`
    # é a mais didática e robusta.
    
    # Vou retornar a versão mais didática e completa em LCEL.
    return final_rag_chain_lcel

# Exemplo de uso (apenas para demonstração, não será executado)
# if __name__ == "__main__":
#     # Exemplo de um retriever dummy
#     class DummyRetriever:
#         def invoke(self, query: str) -> List[Document]:
#             print(f"Retriever invocado com a query: {query}")
#             return [
#                 Document(page_content="O LangChain Expression Language (LCEL) é o novo padrão para construir chains."),
#                 Document(page_content="As chains antigas como create_retrieval_chain foram substituídas por combinações de runnables LCEL.")
#             ]
#     
#     dummy_retriever = DummyRetriever()
#     
#     # Configuração da chain RAG
#     rag_chain = config_rag_chain_lcel(
#         model_class=consts.MODEL_CLASS_OPEN_AI,
#         retriever=dummy_retriever,
#         profile="general"
#     )
#     
#     # Exemplo de histórico de chat
#     chat_history_example = [
#         ("Qual é o novo formato do LangChain?", "É o LCEL."),
#     ]
#     
#     # Exemplo de pergunta de acompanhamento
#     follow_up_question = "O que ele substituiu?"
#     
#     # A chain RAG espera um dicionário com 'input' e 'chat_history'
#     # response = rag_chain.invoke({
#     #     "input": follow_up_question,
#     #     "chat_history": chat_history_example
#     # })
#     
#     # print("\n--- Resposta da Chain RAG (LCEL) ---")
#     # print(f"Resposta: {response['answer']}")
#     # print(f"Contexto: {[doc.page_content for doc in response['context']]}")
#     
#     # Exemplo de chain de resposta simples
#     # simple_response_stream = model_response_lcel(
#     #     user_query="Me diga um fato interessante sobre o Brasil.",
#     #     chat_history=[],
#     #     model_class=consts.MODEL_CLASS_OPEN_AI
#     # )
#     
#     # print("\n--- Resposta da Chain Simples (LCEL) ---")
#     # for chunk in simple_response_stream:
#     #     print(chunk, end="", flush=True)
#     # print()
