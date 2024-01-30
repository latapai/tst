FROM docker.io/python:3.10-slim

WORKDIR /usr/src/app

# OS Update
RUN apt-get update --allow-unauthenticated -y

COPY . ./

# RUN pip install --no-cache-dir -r Pipfile
#RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
#RUN pip install transformers 
RUN pip install -U cffi pip setuptools argon2_cffi chardet watchdog streamlit
RUN pip install --upgrade streamlit-extras
RUN pip install python-dotenv st-clickable-images 
RUN pip install --no-cahe-dir ibm-generative-ai

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8echo 

RUN mkdir -p /.streamlit
RUN chmod 777 /.streamlit

RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /.streamlit/credentials.toml'

RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
enableWebsocketCompression = false\n\
" > /.streamlit/config.toml'

CMD ["python", "-m", "streamlit", "run", "app/main.py", "--server.port=8080"]

EXPOSE 8080
