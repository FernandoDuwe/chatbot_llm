# Chatbot_llm

## _Modelo IA para treinamento_

## Instalação

A aplicação rodará em um container Docker, sendo necessarío o seguinte comando para instalação

Instalar a imagem do Python e as dependências necessárias

```sh
docker compose up -d
```

Entrando no container

```sh
docker exec -t <ID_DO_CONTAINER> /bin/bash
```

Executando o projeto, usando o StreamLit

```sh
streamlit run ./src/main.py
```

## Configuração

Crie um arquivo .env (baseado no arquivo .env.example) e informe a chave de API da Hugging Face

## Execução

Para acessar o chat, acesse a URL: http://localhost:8080/
