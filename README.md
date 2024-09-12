# teste_pratico_python
Repósitório com a finalidade de demonstrar as habilidades com Python com relação à integração de APIs externas, persistência dos dados obtidos e de gerar uma análise dos mesmo.

# Requisitos

- Python 3.12 (versão do Python utilizada para o desenvolvimento)
- PostgreSQL (banco de dados)

# Bibliotecas Principais Utilizadas

- pandas
- flask
- requests
- psycopg2-binary
- python-dotenv

# Primeiros passos

## Chave API

1. Este projeto trabalha com a API do [AviationStack](https://aviationstack.com/). É necessário criar uma conta para poder gerar uma chave de API, que será utilizada.

> [!NOTE]
> A conta gratuita tem várias limitações. O projeto foi elaborado em cima dessa versão.

## Instalação

1. Depois de clonar este projeto em sua máquina, crie um ambiente virtual para poder instalar todos as bibliotecas utilizadas no projeto. Isso é feito através do comando

`python -m venv .venv`

2. Para ativar o ambiente virtual, rode algum dos seguintes códigos:

- Para Windows:

`.venv/Scripts/Activate`

- Para Linux/Mac:

`source .venv/bin/activate`

3. Depois de ativar o ambiente virtual, instale as bibliotecas através do comando:

`pip install -r requirements.txt`

4. Após instalar as bibliotecas, é necessário criar um arquivo _.env_ para salvar algumas variáveis necessárias para o projeto, que são a chave da API e as informações pra conectar no PostgreSQL. Um exemplo do que deve conter o _.env_ está a seguir:

```
CHAVE_API = "INSIRA A CHAVE DE API AQUI NESSE ESPAÇO"
HOST_DB = "Host PostgreSQL"
DATABASE_DB = "Database PostgreSQL"
PORT_DB = "Port PostgreSQL"
USERNAME_DB = "Username PostgreSQL"
PASSWORD_DB = "Password PostgreSQL"
SCHEMA_DB = "Schema PostgreSQL"
```

É necessário substituir todas as variáveis, de acordo com a sua configuração local.

4. Quando estiver pronto para executar o projeto, insira o comando:

`flask -app app.main run`

Ele vai inicializar a API, como já irá gerar a tabela para armazenar as informações necessárias.

5. Quando encerrar o uso do programa, pode desativar o ambiente com o comando:

`deactivate`

# Rotas

## Salvar as informações de vôos

`GET /get_flights`

|Parâmetros|Tipo|Opcional|Descrição|Exemplo|
|---|---|---|---|---|
|iata_code|string| |Código IATA de aeroporto|CWB|
|status|string| X |Status de vôos|scheduled|

Exemplo de Requisição

`/get_flights?iata_code=CWB&status=scheduled`

## Obter as informações de vôos no banco de dados

`GET /info_flights`