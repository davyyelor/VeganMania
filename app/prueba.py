from flask import Flask, request, render_template
import random
import string
import smtplib
import os
from itsdangerous import URLSafeTimedSerializer
from secrets import choice

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Lee la clave secreta desde las variables de entorno
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def generar_contraseña():
    longitud = 12
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(choice(caracteres) for _ in range(longitud))

def generar_token(correo):
    token = serializer.dumps(correo)
    return token

def enviar_correo(correo, token):
    servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    servidor_smtp.starttls()
    servidor_smtp.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
    enlace = f"http://localhost:5000/recuperarContraseña/{token}"
    mensaje = f"Accede al siguiente enlace para recuperar tu contraseña: {enlace}"
    servidor_smtp.sendmail(os.getenv('EMAIL_USER'), correo, mensaje)
    servidor_smtp.quit()

@app.route('/recuperarContraseña', methods=['GET', 'POST'])
def recuperar_contraseña():
    if request.method == 'POST':
        correo = request.form.get('email')
        # Verificar si el correo existe en tu base de datos
        if correo_valido(correo):
            token = generar_token(correo)
            enviar_correo(correo, token)
            return "Se ha enviado un correo con el enlace de recuperación de contraseña."
        else:
            return "La dirección de correo electrónico no está registrada."
    else:
        return render_template('recuperar_contraseña.html')

@app.route('/recuperarContraseña/<token>')
def mostrar_contraseña(token):
    try:
        correo = serializer.loads(token, max_age=3600)
        # Aquí deberías permitir al usuario cambiar su contraseña
        nueva_contraseña = generar_contraseña()
        return f"Tu nueva contraseña es: {nueva_contraseña}"
    except:
        return "El enlace de recuperación de contraseña es inválido o ha expirado."

if __name__ == '__main__':
    app.run(debug=True)

