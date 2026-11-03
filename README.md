# 📈 Consulta de Ações — B3

Projeto desenvolvido em Python para consultar informações de empresas negociadas na Bolsa de Valores brasileira (B3), utilizando a API da [brapi](https://brapi.dev/).

A aplicação permite buscar cotações, visualizar informações de negociação e acompanhar o histórico de preços das ações.

## 🎯 Objetivo

Desenvolver uma aplicação capaz de consumir dados de uma API externa, utilizando requisições HTTP, manipulação de dados JSON e desenvolvimento de interfaces.

## 🛠️ Tecnologias utilizadas

- **Python:** linguagem utilizada no desenvolvimento.
- **Requests:** biblioteca responsável pelas requisições HTTP.
- **Pandas:** organização e manipulação dos dados.
- **Streamlit:** criação da interface visual.
- **Python-dotenv:** gerenciamento de variáveis de ambiente.
- **brapi:** API responsável por fornecer os dados financeiros.

## 📋 Funcionalidades

- Consulta de ações pelo código de negociação (ticker).
- Obtenção de cotações e variações de preços.
- Visualização de máximas e mínimas do dia.
- Consulta de volume negociado.
- Visualização do histórico de preços.
- Gráficos para acompanhar a evolução das cotações.
- Exportação dos dados recebidos em formato JSON.

## 📁 Estrutura do projeto

```text
teste_api/
│
├── .venv/                  # Ambiente virtual
├── .env                    # Variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
│
├── main.py                 # Consulta pelo terminal
├── app.py                  # Interface Streamlit
│
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação
```

## ⚙️ Instalação e configuração

### 1. Baixar o projeto

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

### 2. Entrar na pasta do projeto

No terminal, acesse a pasta onde o projeto foi baixado. Utilize o nome ou caminho correspondente à sua pasta:

```bash
cd caminho/da/sua/pasta
```

### 3. Criar o ambiente virtual

```bash
python -m venv .venv
```

### 4. Ativar o ambiente virtual

No Windows:

```bash
.venv\Scripts\activate
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Configurar a API

Crie um arquivo `.env` na raiz do projeto e adicione seu token:

```env
token_api=SEU_TOKEN
```

Substitua `SEU_TOKEN` pela chave de acesso obtida na plataforma da brapi.

**Importante:** não compartilhe o arquivo `.env` nem publique seu token no GitHub.

## ▶️ Como executar

O projeto possui duas formas de utilização.

### Aplicação pelo terminal

```bash
python main.py
```

### Interface visual com Streamlit

```bash
streamlit run app.py
```

O Streamlit abrirá a aplicação no navegador.

## 🔌 Integração com a API

A aplicação utiliza a API da brapi para obter informações sobre ações da B3.

As requisições são realizadas utilizando a biblioteca `requests`, e as respostas são recebidas em formato JSON.

Documentação oficial: https://brapi.dev/docs

## ⚠️ Limitações

A disponibilidade de informações depende dos recursos oferecidos pelo plano de acesso da API.

A aplicação foi estruturada para utilizar funcionalidades básicas de consulta, respeitando os limites do plano gratuito utilizado no desenvolvimento.

---

**Projeto de estudos — Python e integração com APIs.**