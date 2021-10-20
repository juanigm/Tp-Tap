FROM python:3.9

WORKDIR /app

COPY requeriments.txt /app/requeriments.txt

RUN pip install -r requeriments.txt

COPY . /app

CMD python app.py