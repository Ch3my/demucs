FROM python:3

WORKDIR /usr/src/app

RUN python3 -m pip install -U demucs

COPY . .

CMD ["python", "./App.py"]