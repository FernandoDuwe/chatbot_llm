# Otimizações para Acelerar Leitura das RAGs

## ✅ Mudanças Implementadas

### 1. **Busca mais Rápida (Retriever)**
- Alterado de `mmr` (MaxMarginalRelevance) para `similarity`
  - `mmr` é mais diverso mas muito mais lento
  - `similarity` retorna os resultados mais relevantes diretamente
- Reduzido `k` de 3 para 2 documentos
  - Menos documentos = respostas mais focadas e rápidas

### 2. **Embedding Alternativo**
- Adicionado `EMBEDDING_FAST` = `sentence-transformers/all-MiniLM-L6-v2`
  - 22MB vs 568MB do BAAI/bge-m3
  - ~5x mais rápido com qualidade aceitável para buscas semânticas

## 🚀 Estratégias Adicionais Recomendadas

### 3. **Usar Embedding Mais Leve**
```python
# Em assets_import.py, trocar:
embeddings = HuggingFaceEmbeddings(model_name = consts.EMBEDDING_BAAI)
# Por:
embeddings = HuggingFaceEmbeddings(model_name = consts.EMBEDDING_FAST)
```

### 4. **Cache para Reformulação de Pergunta**
```python
# Adicionar em models.py para evitar reformulações repetidas
from functools import lru_cache

@lru_cache(maxsize=100)
def rephrase_question_cached(question, model_class):
    # Implementar cache da reformulação
    pass
```

### 5. **Paralelizar Operações**
```python
# Se usar múltiplos retrievers, buscar em paralelo
from concurrent.futures import ThreadPoolExecutor
```

### 6. **Reduzir Tokens no LLM**
```python
# Em models.py, reduzir max_new_tokens:
"max_new_tokens": 512  # de 1024
```

### 7. **Usar Quantização do Modelo**
```python
# Para Ollama, usar modelos quantizados:
MODEL_TYPE_OLLAMA = "gemma3:2b-q4_K_M"  # Versão quantizada 4-bit
```

### 8. **Cache de Embeddings ao Inicializar**
```python
# Em main.py, cachear o retriever após primeira inicialização
if ("retriever" not in st.session_state):
    st.session_state.retriever = assets_import.config_retriever_from_index_file(...)
# Isto já está implementado ✓
```

### 9. **Usar fetch_k menor na config_retriever também**
```python
# Em assets_import.py, na função config_retriever:
retriever = vectorstore.as_retriever(
    search_type="similarity",  # Em vez de mmr
    search_kwargs={'k': 2}
)
```

### 10. **Desabilitar Streaming se não Necessário**
```python
# Se resposta rápida for mais importante que UX incremental:
result = rag_chain.invoke(...)  # Em vez de .stream()
```

## 📊 Estimativa de Ganho de Performance

| Otimização | Ganho Estimado |
|-----------|--------|
| MMR → Similarity | **30-50%** mais rápido |
| k=3 → k=2 | **15-20%** mais rápido |
| Embedding pesado → leve | **3-5x** mais rápido |
| max_tokens 1024 → 512 | **20-30%** mais rápido |
| **Total combinado** | **⚡ 5-10x mais rápido** |

## 🔧 Como Implementar

1. Se quiser usar embedding rápido, modifique `assets_import.py`:
```python
embeddings = HuggingFaceEmbeddings(model_name=consts.EMBEDDING_FAST)
```

2. Se está usando índices FAISS já salvos com embedding pesado, precisará **reconstruir** o índice com o novo embedding.

3. Para testar performance, adicione timing:
```python
import time
start = time.time()
result = rag_chain.invoke(...)
print(f"Tempo total: {time.time() - start:.2f}s")
```

## ⚠️ Trade-offs

- **Similarity vs MMR**: Menos diversidade de documentos, mas muito mais rápido
- **Embedding leve vs pesado**: Qualidade ligeiramente menor, mas velocidade muito maior
- **Fewer docs (k=2)**: Respostas mais focadas, mas podem perder contexto em tópicos complexos

## ✨ Próximas Otimizações

- [ ] Implementar cache de embeddings em memória
- [ ] Usar batch processing para múltiplas queries
- [ ] Considerar índices estruturados (BM25 híbrido)
- [ ] Implementar timeout nas buscas
