# python 이미지를 baseimage로 하여 django환경을 container로 패키징하기
FROM  python:3.10.5
# python 3.7.7 버전의 컨테이너 이미지를 base이미지
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apt-get -y update
RUN apt-get -y install build-essential
#파일 편집할 때 쓰일 vim 설치
RUN apt-get -y install vim

RUN apt-get -y install virtualenv

RUN python3 -m pip install --upgrade pip


# RUN mkdir /BBlink_backend
WORKDIR /BBlink_backend
ADD . /BBlink_backend

RUN pip3 install -r /requirements.txt
# WORKDIR /c/Users/shiny/WorkSpace/BBlink_backend
# WORKDIR은 cd와 같은 명령으로, 작업 경로를 /usr/src/app으로 이동합니다.
# CMD에서 설정한 실행 파일이 실행될 디렉터리를 지정해주어야 한다.

# WORKDIR /BBlink_backend
#/c/Users/shiny/WorkSpace/BBlink_backend
# manage.py를 실행할 수 있는 디렉토리로 이동합니다.

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# 이동한 디렉토리에서 django를 가동시켜주는 코드를 작성합니다. 여기서 port는 8000로 실행시키겠습니다.

EXPOSE 8000
# django 서버의 포트를 8000로 지정하였으므로 Docker의 컨테이너 또한 8000 포트를 열어줍니다.