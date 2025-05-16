# Chatbot_llm

## _Modelo IA para treinamento_

Formatos suportados para treinamento: PDF, vídeos do Youtube e arquivos Docx.

## Configuração

Crie um arquivo .env (baseado no arquivo .env.example) e informe a chave de API da Hugging Face

## Instalação

A aplicação rodará em um container Docker, sendo necessarío o seguinte comando para instalação

Instalar a imagem do Python e as dependências necessárias

```sh
docker compose up -d
```

## Lendo arquivos PDFs

Para que a IA leia os arquivos PDFs, coloque-os no diretório ./assets/

## Lendo transcrições de vídeos do Youtube

Para efetuar a aprendizagem de vídeos no Youtube, o vídeo deve ser transcrito para o formato txt.

Para transcrever os vídeos, adicione os IDs dos vídeos no arquivo ./config/youtube_import_list.json, em seguida, execute o seguinte comando:

```sh
python ./src/transcript_youtube_data.py
```

## Lendo páginas WEB

Para que a IA leia as suas páginas WEB, adicione a url no arquivo ./config/web_import_list.json.

Execute o arquivo abaixo para efetuar a leitura das páginas

```sh
python ./src/transcript_webpage_data.py
```

## Lendo arquivos mp4

Para que a IA leia as suas páginas WEB, adicione os arquivos na pasta ./temp.

Execute o arquivo abaixo para efetuar a leitura das páginas

```sh
python ./src/transcript_mp4_data.py
```

## Efetuando o treinamento da IA

Devido a questões de performance, separamos a fase de treinamento da fase de execução, para efetuar o treinamento,execute o seguinte comando:

```sh
python ./src/training.py
```

## Ollama - Baixando o modelo correspondente

O modelo Ollama rodará localmente, para isso, o modelo deve ser baixado no container:

```sh
docker exec -it ollama ollama pull phi3
```

## Execução

Entrando no container

```sh
docker exec -t <ID_DO_CONTAINER> /bin/bash
```

Executando o projeto, usando o StreamLit

```sh
streamlit run ./src/main.py
```

Para acessar o chat, acesse a URL: http://localhost:8501/

## Extensões utilizadas

Extensões geradas pela ferramenta durante a fase transcrição

- .ytb - Vídeos transcritos do Youtube
- .wbt - Páginas web transcritas
- .mp4t - Vídeos mp4 transcritos
