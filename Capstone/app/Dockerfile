FROM python:3.9-slim-buster

COPY . .
RUN apt-get update 
RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install efficientnet-pytorch
RUN pip3 install -r requirements.txt
