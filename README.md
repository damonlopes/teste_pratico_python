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
- pytest
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
CHAVE_API = "Chave API"
PG_HOST = "Host PostgreSQL"
PG_DATABASE = "Database PostgreSQL"
PG_PORT = "Port PostgreSQL"
PG_USERNAME = "Username PostgreSQL"
PG_PASSWORD = "Password PostgreSQL"
PG_SCHEMA = "Schema PostgreSQL"
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

Rota para obter os dados de vôos e salvar no banco de dados localmente

- Parâmetros

|Parâmetro|Tipo|Opcional|Descrição|Exemplo|
|---|---|---|---|---|
|iata_code|string| |Código IATA de aeroporto|CWB|
|status|string| X |Status de vôos|scheduled|

Para obter o código IATA, pode acessar o site da [IATA](https://www.iata.org/en/publications/directories/code-search/) para obter o código de algum aeroporto.
Isso foi feito pois nos testes, eram muitos vôos registrados diariamente, então optou-se por limitar a pesquisa para um aeroporto.

- Exemplo de Requisição

`GET /get_flights?iata_code=CWB&status=scheduled`

## Obter as informações de vôos no banco de dados

`GET /info_flights`

Rota para obter todos os dados salvos referentes a vôos.

- Parâmetros

|Parâmetro|Tipo|Opcional|Descrição|Exemplo|
|---|---|---|---|---|
|flight_date|date| X |Data do vôo|2024-09-01|

- Exemplo de requisição

`GET /info_flights?flight_date=2024-09-10`

# Tabela do Banco de Dados

Nome da tabela: flights
|Nome Variável|Tipo|Chave Primária|Obrigatório|Descrição|
|---|---|---|---|---|
|id|int| X | X |ID de cada entrada na tabela|
|flight_date|datetime|| X |Data de registro do vôo|
|flight_iata|string|||Código IATA do vôo|
|flight_status|string|||Status do vôo|
|airplane|string|| X |Companhia Aérea|
|dep_iata|string|| X |Código IATA de origem do vôo|
|dep_delay|int|||Tempo de atraso de partida|
|arr_iata|datetime|| X |Código IATA de destino do vôo|
|dep_delay|int|||Tempo de atraso da chegada|

# Análise de Dados

A análise de dados foi feita de acordo com os dados obtidos no período da tarde do dia 12/09/2024, referente a todos os vôos do Aeroporto Internacional Afonso Pena (CWB). 

A análise se encontra dentro da pasta _data-analysis_, onde foi utilizado a biblioteca _pandas_, dentro de um arquivo [notebook](data-analysis/analise-dados-aeroporto-cwb.ipynb). Foi salvo junto um arquivo [html](data-analysis/analise-dados-aeroporto-cwb.html) com o arquivo original da análise, e a [base de dados](data-analysis/info_flights.json) utilizada.

# Testes

Foi utilizado a biblioteca _pytest_ para poder executar os testes referentes à API.

Para poder executar os testes localizados na pasta [tests](app/tests/), é só rodar o seguinte comando (com o ambiente virtual ativado):

`python -m pytest`