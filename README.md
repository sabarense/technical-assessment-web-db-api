# Projeto de Análise de Dados ANS

Este projeto integra extração, transformação e análise de dados da Agência Nacional de Saúde Suplementar (ANS), disponibilizando-os através de uma API REST e interface web.

## Estrutura do Projeto

technical-assessment-web-db-api/
├── data/
│ ├── downloads/ # Arquivos baixados via web scraping
│ └── processed/ # Dados transformados e processados
├── backend/
│ ├── api/ # Servidor Python e API REST
│ ├── database/ # Scripts SQL e conexões
│ ├── scraping/ # Scripts de web scraping
│ └── transformation/ # Scripts de transformação de PDFs
├── frontend/ # Interface Vue.js
├── postman/ # Coleção para testes da API
└── pipeline.py # Script orquestrador de todo o processo


## Requisitos

### Backend
- Python 3.8+
- Bibliotecas: requests, BeautifulSoup4, pandas, pdfplumber, Flask/FastAPI
- PostgreSQL 10+ ou MySQL 8+

### Frontend
- Node.js 14+
- Vue.js 3
- Axios

## Instalação

### Backend

1. Configure o ambiente Python: <br>
python -m venv venv <br>
source venv/bin/activate # Linux/macOS <br>
venv\Scripts\activate # Windows <br>
pip install -r requirements.txt<br>
2. Configure o banco de dados: <br>
Execute os scripts em backend/database/scrips/


### Frontend
cd frontend <br>
npm install

## Funcionalidades

### 1. Web Scraping
Extração automatizada de dados do portal da ANS:
- Download de anexos PDF do site de atualização do Rol de Procedimentos.
- Compactação de anexos em formato ZIP.

### 2. Transformação de Dados
- Processamento de tabelas em PDFs usando pdfplumber.
- Estruturação e limpeza dos dados.
- Substituição de abreviações por descrições completas (OD → Seg. Odontológico, AMB → Seg. Ambulatorial).
- Exportação para formato CSV e compactação.

### 3. Banco de Dados
- Estruturação de dados das demonstrações contábeis e cadastros de operadoras.
- Queries analíticas para identificar operadoras com maiores despesas.
- Importação inteligente com tratamento de encoding.

### 4. API e Interface Web
- Servidor Python com rotas para busca textual no cadastro de operadoras.
- Interface Vue.js para interação com a API.

## Execução

### Pipeline Completo
Para executar todo o processo automatizado: <br>
python pipeline.py

### Componentes Individuais

**Web Scraping:**
python backend/scraping/web_scraping.py

**Transformação de Dados:**
python backend/transformation/data_transformation.py

**Servidor API:** <br>
cd backend/api<br>
python server.py

**Frontend:** <br>
cd frontend <br>
npm run serve

## Endpoints da API

### GET /api/operadoras/busca

Realiza busca textual nas operadoras de saúde.

**Parâmetros:**
- `query`: Texto para busca (obrigatório).
- `limit`: Limite de resultados (opcional, padrão: 10).

**Resposta:**
(a fazer)

## Licença

Este projeto está licenciado sob a licença MIT.

