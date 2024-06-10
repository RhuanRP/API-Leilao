Auction API
Descrição
Auction API é um sistema de leilão desenvolvido com FastAPI e SQLAlchemy, utilizando um banco de dados PostgreSQL. Esta API permite a criação e gerenciamento de itens de leilão, compradores e lances.

Tecnologias Utilizadas
FastAPI: Framework web moderno e rápido para construir APIs com Python.
SQLAlchemy: Biblioteca de ORM (Object-Relational Mapping) para interagir com o banco de dados.
PostgreSQL: Sistema de gerenciamento de banco de dados relacional.
Uvicorn: Servidor ASGI para executar a aplicação FastAPI.
Pydantic: Biblioteca para validação de dados.
Funcionalidades
Itens de Leilão:
Listar todos os itens.
Criar novos itens.
Compradores:
Listar todos os compradores.
Criar novos compradores.
Lances:
Listar todos os lances.
Fazer um novo lance em um item.
Endpoints
Itens de Leilão
GET /items: Retorna uma lista de todos os itens disponíveis no leilão.
POST /items: Cria um novo item de leilão.
Compradores
GET /buyers: Retorna uma lista de todos os compradores.
POST /buyers: Cria um novo comprador.
Lances
GET /bids: Retorna uma lista de todos os lances.
POST /bids: Faz um novo lance em um item de leilão.
Estrutura do Projeto
bash
Copiar código
.
├── main.py
├── models.py
├── requirements.txt
└── README.md
Arquivo main.py
Este é o arquivo principal que contém a definição da API e seus endpoints. Inclui a configuração de middleware, inicialização do banco de dados e definição dos modelos de dados e validação de esquemas.

Arquivo models.py
Este arquivo contém a definição dos modelos do SQLAlchemy para os itens, compradores e lances, bem como a configuração da sessão do banco de dados.

Como Executar
Pré-requisitos
Python 3.7 ou superior
PostgreSQL
Passos para Execução
Clone o repositório:

bash
Copiar código
git clone https://github.com/seu-usuario/auction-api.git
cd auction-api
Crie um ambiente virtual e instale as dependências:

bash
Copiar código
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configure a URL do banco de dados no arquivo main.py:

python
Copiar código
DATABASE_URL = "sua_url_do_banco_de_dados"
Execute a aplicação:

bash
Copiar código
uvicorn main:app --host 0.0.0.0 --port 5000
Acesse a documentação da API no navegador:

arduino
Copiar código
http://127.0.0.1:5000/docs
Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.
