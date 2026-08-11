# Dashboard - Estação Meteorológica

Dashboard para vizualização dos dados coletados por uma estação meteorológica do câmpus do IFSC.

O projeto possui dois componentes principais:

- `serial_reader.py`: Realiza a leitura dos dados enviados pela estação e armazena os dados na pasta `dados/`
- `app.py`: executa o dashboard web, utilizando os dados armazenados para gerar as vizualização.

---

## Estrutura do projeto

```text
dashboard/
├── config/
│   └── credenciais.json
│
├── dados/
│   ├── dados_estacao.csv
│   └── status.json
│
├── static/
│   ├── graficos.js
│   ├── script.js
│   └── style.css
│
├── templates/
│   ├── graficos.html
│   └── index.html
│
├── app.py
├── serial_reader.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── start.sh
└── README.md
```
---

## Execução utilizando Python

Recomenda-se utilizar um ambiente virutal(`venv`) para instalar e executar o projeto diretamente no sistema.

1. **Criar o ambiente virtual**
````bash
    - python3 -m venv venv
````

2. **Acessar ambiente virtual**
````bash
    - source venv/bin/activate
````

3. **Instalar as dependências**
````bash
    - pip install -r requirements.txt
````

4. **Executar o leitor da estação**
````bash
    - python3 serial_reader.py
````

Para que o leitor funcione, a estação metereológica deve estar conectrada ao computador.

A porta serial utilizada pelo projeto é:
`/dev/ttyUSB0`

5. **Executar o dashboard**

O dashboard deve ser executado em outro terminal na pasta do projeto.

Certifique-se que está dentro dentro do ambiente virtual.
````bash
    - python3 app.py
````
O dashoboard estará disponível em:
`http://localhost:5000`

---
**Desativar o ambiente virtual**

Quando terminar de utilizar o projeto:
`deactivate`

---

## Execução utilizando Docker

O projeto também pode ser executado utilizando Docker e Docker Compose.

Nesse modo, o `start.sh` inicia os dois processos:
- `serial_render.py`
- `app.py`


1. **Verificar o Serviço do Docker**

Verificar se o serviço do Docker está em execução:
````bash
sudo systemctl status docker
````

Caso esteja parado:
````bash
sudo systemctl start docker
````

2. **Contruir a imagem Docker**

Na pasta do projeto:
````bash
docker compose build
````

Caso seja necessário recontruir a imagem completamente:
````bash
docker compose build --no-cache
````

3. **Inicar o container**

Para inciciar o container em primeiro plano:
````bash
docker compose up
````

Para iniciar o container em segundo plano:
````bash
docker compose up -d
````

Para contruir a imagem e iniciar o container em um único comando:
````bash
docker compose up -d --build
````

4. **Verificar se o container está funcionando**
````bash
docker ps
````

O container deve aparecer com o nome de `estacao_dashboard`