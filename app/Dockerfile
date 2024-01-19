FROM python:3.6

# Instala gunicornz
RUN pip install gunicorn

EXPOSE 5000
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
COPY app.py /app

CMD gunicorn -w 4 -b 0.0.0.0:5000 app:app
