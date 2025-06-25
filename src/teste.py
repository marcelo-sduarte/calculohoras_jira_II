import win32
from win32 import win32cred

def save_credential(target_name, username, password):

        # Converte a senha para uma string
        password_str = str(password)
        # Define a estrutura da credencial como um dicionário
        cred = {
            'TargetName': target_name,
            'Type': win32cred.CRED_TYPE_GENERIC,
            'UserName': username,
            'CredentialBlob': password_str,
            'Persist': win32cred.CRED_PERSIST_LOCAL_MACHINE
        } 
        # Salva a credencial no cofre de senhas do Windows   
        win32cred.CredWrite(cred)

def get_credential(target_name):        
    try:
        # Tenta obter a credencial do cofre de senhas do Windows
        cred = win32cred.CredRead(target_name, win32cred.CRED_TYPE_GENERIC)

        # Decodifica a senha de bytes para uma string UTF-16
        password_decoded = cred['CredentialBlob'].decode('utf-16')

        # Retorna o nome de usuário e a senha
        return cred['UserName'], password_decoded
    except Exception as error:
        if error.winerror == 1168:  # ERROR_NOT_FOUND
            return None, None
        else:
            print(f"> error message: ", error)






#save_credential(target_name="email_cadmus",password="MA@msd41", username="marcelo.duarte@cadmus.com.br")
user, senha = get_credential("token_jira")
print(f"USER: {user} SENHA: {senha}")