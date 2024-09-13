# Python 3.12.4 이미지를 기반으로 설정
FROM python:3.12.4-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
  gcc \
  libmariadb-dev-compat \
  pkg-config \
  libgl1-mesa-glx \        
  libglib2.0-0 \           
  libsm6 \                 
  libxrender1 \            
  libxext6 \               
  libjpeg62-turbo-dev \   
  libpng-dev              

# 필요한 파일 복사
COPY . /app

# pip 업그레이드
RUN pip install --upgrade pip

# TensorFlow 설치 - 휠 파일 직접 지정
RUN pip install https://storage.googleapis.com/tensorflow/versions/2.17.0/tensorflow_cpu-2.17.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# tf-keras 설치
RUN pip install tf-keras

# 종속성 설치
RUN pip install -r requirementsfordocker.txt

# Gunicorn으로 앱 실행
CMD exec gunicorn -b :$PORT app:app