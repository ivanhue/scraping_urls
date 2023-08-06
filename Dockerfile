FROM python:3.11-slim

# ADD /src/pruebas.py .


# COPY requirements.txt .
ADD /src/run.py .

# WORKDIR /app
COPY . .


RUN pip install -r requirements.txt

RUN python -m nltk.downloader punkt wordnet omw-1.4 stopwords


# docker run --rm -it $(docker build -q .)
ENTRYPOINT ["python", "/src/run.py"]