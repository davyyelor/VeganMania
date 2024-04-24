import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, receiver_email, subject, message):
    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Add body to the email
    msg.attach(MIMEText(message, "plain"))

    # Create SMTP session
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")

# Email details
sender_email = "d02668507@gmail.com"
sender_password = "Maruri.1"
receiver_email = "davidelorzag@gmail.com"
subject = "Hello"
message = "Hello, this is a test email from David!"

# Send email
send_email(sender_email, sender_password, receiver_email, subject, message)
