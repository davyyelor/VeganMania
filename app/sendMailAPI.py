from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import ssl
import smtplib


def send_email(email_receiver, contraseña):
    password = 'rzxz jhtf lbxf tqus'
    email_sender = 'veganmaniiaa@gmail.com'

    subject = "Recuperación de Contraseña"
    body = f"""\
    Estimado/a usuario/a,

    Se ha generado una nueva contraseña para tu cuenta. A continuación, encontrarás los detalles:

    Nueva contraseña: {contraseña}

    Por motivos de seguridad, te recomendamos cambiar esta contraseña por una que te resulte más fácil de recordar. Si tienes alguna pregunta o necesitas ayuda, no dudes en contactar con el administrador de la aplicación.

    Atentamente,
    El equipo de VeganMania
    """

    # Crear un objeto MIMEMultipart
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = email_sender
    msg['To'] = email_receiver

    # Adjuntar el cuerpo del mensaje
    msg.attach(MIMEText(body, 'plain'))

    # Adjuntar una imagen
    with open('static/images/veganMania.png', 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment', filename="imagen.jpg")
        msg.attach(img)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_sender, password)
        server.send_message(msg)
        print("Correo enviado")