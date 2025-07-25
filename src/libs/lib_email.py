import pieces
from gvars import *
"""
Funcoes para envio de email
"""
def send_email(EmailTo, Subject,Body,Co=None,output_path=None, nameFile=None):
    try:
        #get credentials
        username, password = pieces.lib_process.get_credential(target_name=EMAIL_TARGET)
        # Configurações do email
        subject = Subject
        # Criar objeto MIMEMultipart
        msg = pieces.MIMEMultipart()
        msg['From'] = username
        msg['To'] = EmailTo  
        msg['Co'] = Co
        msg['Subject'] = subject
        # Corpo do email (texto)
        msg.attach(pieces.MIMEText(Body, 'plain'))
        if output_path:
            # Anexo
            with open(output_path, 'rb') as file:
                part = pieces.MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
            pieces.encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={nameFile}')
            msg.attach(part)

        # Conectar ao servidor SMTP
        servidor = pieces.smtplib.SMTP(EMAIL_SMTP, EMAIL_PORT)
        servidor.starttls()
        #Autentica
        servidor.login(str(username), str(password))
        # Enviar a mensagem
        servidor.send_message(msg)
        print('Email enviado com sucesso!')  
    except Exception as error:
        pieces.lib_logging.logger.info(f"> send_email error message: {error}")
    