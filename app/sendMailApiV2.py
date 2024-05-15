import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
import ssl

password = 'rzxz jhtf lbxf tqus'
email_sender = 'veganmaniiaa@gmail.com'
destinatario = 'davidelorzag@gmail.com'

def send_email(email_receiver, opcion, link):
    if opcion == 0:
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = "Recuperación de Contraseña"

        with open('app/templates/mails/reset_password.html', 'r') as f:
            message = f.read()

        message = message.replace('{{link}}', link)  # Reemplazar {{link}} con el enlace real
        #message = message.replace('nombre', nombre)

        msg.attach(MIMEText(message, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        print("enviado")
        server.quit()        

    elif opcion == 1:
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = "Bienvenido a VeganMania"

        with open('app/templates/mails/welcomeMail.html', 'r') as f:
            message = f.read()

        #message = message.replace('link', link)
        #message = message.replace('nombre', nombre)

        msg.attach(MIMEText(message, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        print("enviado")
        server.quit()     

if __name__ == '__main__':
    send_email('davidelorzag@gmail.com', 0, link='http://localhost:5000/recuperarContraseña')