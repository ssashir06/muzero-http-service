FROM python:3.8

RUN apt-get update &&\
    apt-get install -y swig &&\
    apt-get clean

WORKDIR /app
COPY submodules/muzero-general/requirements.txt submodules/muzero-general/
COPY src/requirements.txt src/
COPY requirements.txt .
RUN pip install -r requirements.txt &&\
    pip cache purge

COPY submodules submodules
COPY src src
COPY models models

CMD uvicorn src.main:app --port 8000 --host 0.0.0.0