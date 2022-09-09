FROM python

WORKDIR /opt/demo/
COPY /app .

RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

ENTRYPOINT python app.py
