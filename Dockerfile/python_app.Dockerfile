FROM python:3.10
WORKDIR /app
COPY ./config/dependencies.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r dependencies.txt