# 📄 Hub de Captura de Documentos WhatsApp

Este projeto é um microserviço construído em **FastAPI** que atua em conjunto com a **Evolution API**.

Ele tem a responsabilidade de:

- Receber webhooks de mensagens do WhatsApp
- Interceptar arquivos enviados (como PDFs e Imagens)
- Baixá-los fisicamente
- Disponibilizar uma API para que outros times/sistemas possam consultar e fazer o download desses arquivos para processamento futuro

---

## 🚀 Arquitetura e Tecnologias

O ambiente é totalmente dockerizado e sobe toda a infraestrutura necessária de uma só vez:

- **FastAPI (Python 3.11):** API de captura e disponibilização de arquivos
- **Evolution API (v2.3.6):** Motor de conexão com o WhatsApp
- **PostgreSQL 15:** Banco de dados para a Evolution API
- **Redis:** Gerenciamento de cache e filas para a Evolution API

---

## ⚙️ Como Instalar e Rodar

### 1️⃣ Pré-requisitos

Você precisa ter instalado na sua máquina/servidor:

- Docker
- Docker Compose

---

### 2️⃣ Configurando o Ambiente

Clone este repositório e crie o arquivo de variáveis de ambiente a partir do exemplo:

Linux / Mac:
cp .env.example .env

Windows (PowerShell):
Copy-Item .env.example -Destination .env

Abra o arquivo `.env` gerado e preencha as variáveis de segurança:

- EVOLUTION_API_KEY
- AUTHENTICATION_API_KEY
- EVOLUTION_INSTANCE

---

### 3️⃣ Subindo a Aplicação

Execute o comando abaixo na raiz do projeto:

docker-compose up -d --build

O sistema criará automaticamente uma pasta chamada `downloads` na raiz do projeto, onde os arquivos capturados serão salvos.

Essa pasta está mapeada no Docker e os arquivos não serão perdidos se o container reiniciar.

---

## 🔌 Configurando a Evolution API

Webhook que deve ser cadastrado:

http://capturador-api:8000/webhook/evolution

Importante:
- Ative o evento messages.upsert
- Ative a opção de enviar mídia em Base64

---

## 📡 Documentação das Rotas (API)

POST /webhook/evolution  
Recebe os eventos do WhatsApp e salva arquivos detectados.

GET /arquivos/listar  
Retorna lista de arquivos disponíveis.

Exemplo de resposta:

{
  "quantidade": 1,
  "arquivos": ["20231025_11999999999_a1b2c3.pdf"],
  "mensagem": "Use a rota /arquivos/download/{nome_arquivo} para baixar"
}

GET /arquivos/download/{nome_arquivo}  
Realiza o download do documento desejado.

Swagger:
http://localhost:8000/docs
