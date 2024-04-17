FROM python:3.11.9-slim

# Adicione o usuário não privilegiado
RUN useradd -ms /bin/bash python

# Defina o diretório de trabalho como /home/python/app
WORKDIR /home/python/app

# Copie o arquivo requirements.txt e instale as dependências como root
COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt

# Volte ao usuário não privilegiado
USER python

# Mantenha o container em execução

# CMD [ "tail", "-f", "/dev/null" ] -- ANTES


CMD [ "flask", "run", "--host=0.0.0.0" ]
