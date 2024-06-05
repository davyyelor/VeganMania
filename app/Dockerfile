FROM python:3.6

# Instala gunicorn
RUN pip install gunicorn

EXPOSE 5000
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
COPY app.py /app

# Asegúrate de copiar el archivo de configuración de Gunicorn
COPY gunicorn_config.py /app

CMD gunicorn -c /app/gunicorn_config.py app:app
