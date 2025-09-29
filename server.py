import http.server
import socketserver
import json
import sqlite3
import os
from urllib.parse import urlparse

PORT = 8000
DB_FILE = os.path.join(os.path.dirname(__file__), "tarefas.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT DEFAULT 'pendente',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def send_json(handler, data, status=200):
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.end_headers()
    handler.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

def read_json(handler):
    length = int(handler.headers.get("Content-Length", 0))
    if length == 0:
        return None
    return json.loads(handler.rfile.read(length).decode("utf-8"))

class TarefaHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        if path == "/tarefas":
            rows = cur.execute("SELECT * FROM tarefas ORDER BY id").fetchall()
            tarefas = [dict(r) for r in rows]
            send_json(self, tarefas)

        elif path.startswith("/tarefas/"):
            try:
                tarefa_id = int(path.split("/")[-1])
            except:
                send_json(self, {"error": "ID inválido"}, 400)
                conn.close()
                return
            row = cur.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
            if row:
                send_json(self, dict(row))
            else:
                send_json(self, {"error": "Tarefa não encontrada"}, 404)
        else:
            send_json(self, {"error": "Rota não encontrada"}, 404)

        conn.close()

    def do_POST(self):
        if self.path != "/tarefas":
            send_json(self, {"error": "Rota não encontrada"}, 404)
            return
        data = read_json(self)
        if not data or not data.get("titulo"):
            send_json(self, {"error": "Campo 'titulo' obrigatório"}, 400)
            return

        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tarefas (titulo, descricao, status) VALUES (?, ?, ?)",
            (data["titulo"], data.get("descricao"), data.get("status", "pendente"))
        )
        conn.commit()
        tarefa_id = cur.lastrowid
        row = cur.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
        conn.close()
        send_json(self, dict(row), 201)

    def do_PUT(self):
        if not self.path.startswith("/tarefas/"):
            send_json(self, {"error": "Rota não encontrada"}, 404)
            return
        try:
            tarefa_id = int(self.path.split("/")[-1])
        except:
            send_json(self, {"error": "ID inválido"}, 400)
            return
        data = read_json(self)
        if not data:
            send_json(self, {"error": "JSON inválido"}, 400)
            return

        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        row = cur.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
        if not row:
            conn.close()
            send_json(self, {"error": "Tarefa não encontrada"}, 404)
            return

        titulo = data.get("titulo", row["titulo"])
        descricao = data.get("descricao", row["descricao"])
        status = data.get("status", row["status"])

        cur.execute(
            "UPDATE tarefas SET titulo = ?, descricao = ?, status = ? WHERE id = ?",
            (titulo, descricao, status, tarefa_id)
        )
        conn.commit()
        row = cur.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
        conn.close()
        send_json(self, dict(row))

    def do_DELETE(self):
        if not self.path.startswith("/tarefas/"):
            send_json(self, {"error": "Rota não encontrada"}, 404)
            return
        try:
            tarefa_id = int(self.path.split("/")[-1])
        except:
            send_json(self, {"error": "ID inválido"}, 400)
            return

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
        deleted = cur.rowcount
        conn.commit()
        conn.close()

        if deleted:
            send_json(self, {"message": "Tarefa removida"})
        else:
            send_json(self, {"error": "Tarefa não encontrada"}, 404)

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    init_db()
    with socketserver.TCPServer(("", PORT), TarefaHandler) as httpd:
        print(f"Servidor iniciado na porta {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor finalizado")
