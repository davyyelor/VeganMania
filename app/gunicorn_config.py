# gunicorn_config.py
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1  # Ajusta esto según tu entorno
timeout = 120
bind = "0.0.0.0:5000"
