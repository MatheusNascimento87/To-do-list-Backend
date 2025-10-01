# 📝 Gerenciador de Tarefas (Python + SQLite3 + HTTPServer)

Este projeto implementa um **servidor backend em Python** que expõe uma API REST para gerenciar tarefas, utilizando **SQLite3** como banco de dados, além de um **cliente em Python** para consumir essa API via linha de comando.

---

## 🚀 Funcionalidades

- Criar uma nova tarefa (`POST /tarefas`)
- Listar todas as tarefas (`GET /tarefas`)
- Buscar uma tarefa pelo ID (`GET /tarefas/{id}`)
- Atualizar uma tarefa existente (`PUT /tarefas/{id}`)
- Deletar uma tarefa (`DELETE /tarefas/{id}`)

---

## 🏗 Estrutura do Projeto

```
📂 projeto-tarefas
 ┣ 📜 server.py   # Servidor backend (API REST em Python)
 ┣ 📜 client.py   # Cliente em Python (menu interativo)
 ┣ 📜 tarefas.db  # Banco SQLite3 (gerado automaticamente)
 ┗ 📜 README.md   # Este arquivo
```

---

## ⚙️ Como funciona o servidor (`server.py`)

- Utiliza **http.server** e **socketserver** para rodar um servidor HTTP simples.
- Armazena as tarefas em um banco **SQLite3**.
- Implementa rotas RESTful (`GET`, `POST`, `PUT`, `DELETE`).
- Cada rota retorna dados no formato **JSON**.
- Exemplo de estrutura da tabela:

```sql
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT,
    status TEXT DEFAULT 'pendente',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🖥️ Como funciona o cliente (`client.py`)

- Programa de linha de comando que usa a biblioteca `requests` para consumir a API.
- Oferece um **menu interativo** com as opções:
  1 - Criar tarefa  
  2 - Listar tarefas  
  3 - Visualizar tarefa por ID  
  4 - Atualizar tarefa  
  5 - Deletar tarefa  
  0 - Sair  

---

## ▶️ Executando o projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/MatheusNascimento87/To-do-list-Backend.git
cd projeto-tarefas
```

### 2. Criar ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Instalar dependências
O servidor só usa bibliotecas padrão do Python.  
O cliente precisa da biblioteca `requests`:
```bash
pip install requests
```

### 4. Iniciar o servidor
```bash
python server.py
```
O servidor rodará em:
```
http://localhost:8000
```

### 5. Executar o cliente
Em outro terminal:
```bash
python client.py
```

---

## 📡 Exemplos de uso da API (via `curl`)

Criar uma tarefa:
```bash
curl -X POST http://localhost:8000/tarefas      -H "Content-Type: application/json"      -d '{"titulo": "Estudar Python", "descricao": "Finalizar projeto"}'
```

Listar todas as tarefas:
```bash
curl http://localhost:8000/tarefas
```

Buscar tarefa por ID:
```bash
curl http://localhost:8000/tarefas/1
```

Atualizar tarefa:
```bash
curl -X PUT http://localhost:8000/tarefas/1      -H "Content-Type: application/json"      -d '{"status": "completo"}'
```

Deletar tarefa:
```bash
curl -X DELETE http://localhost:8000/tarefas/1
```

---

## 🛠 Tecnologias utilizadas

- Python 3
- http.server + socketserver (servidor HTTP)
- SQLite3 (banco de dados)
- Requests (cliente HTTP)

---

## 📌 Observações

- O banco `tarefas.db` é criado automaticamente ao rodar o servidor.  
- Todas as respostas da API são em **JSON**.  
- Os métodos retornam **status codes HTTP** adequados:
  - `200 OK` → Sucesso
  - `201 Created` → Registro criado
  - `400 Bad Request` → Erro no formato ou parâmetros
  - `404 Not Found` → Recurso não encontrado

---

## 📄 Licença
Este projeto é livre para uso acadêmico e educacional. 🚀
