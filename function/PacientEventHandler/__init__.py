import logging
import smtplib
from email.message import EmailMessage
import azure.functions as func
import os

def enviar_email(destinatario, assunto, corpo):
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = os.environ["SMTP_EMAIL"]
    msg['To'] = destinatario
    msg.set_content(corpo)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(os.environ["SMTP_EMAIL"], os.environ["SMTP_PASSWORD"])
        server.send_message(msg)

def main(event: func.EventGridEvent):
    logging.info("Evento recebido: %s", event.event_type)

    data = event.get_json()

    if event.event_type == "PacienteRegistrado":
        nome = data.get("nome", "Paciente")
        email = data.get("email")
        assunto = "Bem-vindo ao MedFinder!"
        corpo = f"Olá {nome},\n\nSeu cadastro foi concluído com sucesso. Obrigado por usar o MedFinder!"
        enviar_email(email, assunto, corpo)

    elif event.event_type == "ConsultaAgendada":
        email = data.get("email")
        assunto = "Consulta confirmada!"
        corpo = f"Olá! Sua consulta com {data.get('medico')} está marcada para {data.get('data')}."
        enviar_email(email, assunto, corpo)

    else:
        logging.warning("Tipo de evento desconhecido: %s", event.event_type)
