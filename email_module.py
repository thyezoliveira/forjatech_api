import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

# Lista de emails para receber a notificação
RECIPIENT_LIST = ["thyezoliveira.homeoffice@gmail.com"]

# Configurações do servidor SMTP (usando variáveis de ambiente)
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

def send_budget_email(orcamento):
    """
    Envia um email de notificação sobre um novo pedido de orçamento.
    """
    if not all([SMTP_USER, SMTP_PASSWORD]):
        print("As credenciais SMTP (SMTP_USER, SMTP_PASSWORD) não estão configuradas nas variáveis de ambiente. O email não será enviado.")
        return

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Novo Pedido de Orçamento: {orcamento.assunto}"
    msg['From'] = SMTP_USER
    msg['To'] = ", ".join(RECIPIENT_LIST)

    html_body = f"""
    <html>
    <body>
        <h2>Novo Pedido de Orçamento Recebido</h2>
        <p><strong>Empresa:</strong> {orcamento.nomeEmpresa}</p>
        <p><strong>Ramo:</strong> {orcamento.ramoEmpresa}</p>
        <p><strong>Email:</strong> {orcamento.emailContato}</p>
        <p><strong>Telefone:</strong> {orcamento.telefone}</p>
        <p><strong>Assunto:</strong> {orcamento.assunto}</p>
        <p><strong>Descrição:</strong></p>
        <p>{orcamento.descricaoDetalhada}</p>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, RECIPIENT_LIST, msg.as_string())
            print("Email de notificação enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")

