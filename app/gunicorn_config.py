# gunicorn_config.py
workers = 4  # Puedes ajustar este número según la cantidad de núcleos de tu CPU
timeout = 120
bind = "0.0.0.0:5000"
