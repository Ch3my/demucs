FROM python:3
ENV FLASK_APP=App.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

WORKDIR /usr/src/app

RUN python3 -m pip install -U demucs
RUN pip install flask
RUN mkdir uploads

RUN apt-get update && apt-get install ffmpeg

COPY . .

EXPOSE 5000

CMD ["flask", "run"]