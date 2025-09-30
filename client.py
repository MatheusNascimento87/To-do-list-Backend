import requests
import json

BASE = "http://localhost:8000/tarefas"

def criar_tarefa():
    titulo = input("Título da tarefa: ").strip()
    descricao = input("Descrição (opcional): ").strip()
    if not titulo:
        print("Título é obrigatório.")
        return
    payload = {"titulo": titulo, "descricao": descricao or None}
    try:
        r = requests.post(BASE, json=payload)
        if r.status_code == 201:
            print("Criada:", r.json())
        else:
            print("Erro:", r.status_code, r.text)
    except requests.RequestException as e:
        print("Erro de conexão:", e)

def listar_tarefas():
    try:
        r = requests.get(BASE)
        if r.status_code == 200:
            tarefas = r.json()
            if not tarefas:
                print("Nenhuma tarefa encontrada.")
                return
            for t in tarefas:
                print(f"[{t['id']}] {t['titulo']} - {t['status']}")
        else:
            print("Erro:", r.status_code, r.text)
    except requests.RequestException as e:
        print("Erro de conexão:", e)

def visualizar_tarefa():
    tid = input("ID da tarefa: ").strip()
    if not tid.isdigit():
        print("ID inválido")
        return
    try:
        r = requests.get(f"{BASE}/{tid}")
        if r.status_code == 200:
            print(json.dumps(r.json(), indent=2, ensure_ascii=False))
        else:
            print("Erro:", r.status_code, r.text)
    except requests.RequestException as e:
        print("Erro de conexão:", e)

def atualizar_tarefa():
    tid = input("ID da tarefa: ").strip()
    if not tid.isdigit():
        print("ID inválido")
        return
    titulo = input("Novo título (deixe em branco para manter): ").strip()
    descricao = input("Nova descrição (deixe em branco para manter): ").strip()
    status = input("Novo status (pendente/completo) (deixe em branco para manter): ").strip()
    payload = {}
    if titulo: payload['titulo'] = titulo
    if descricao: payload['descricao'] = descricao
    if status: payload['status'] = status
    try:
        r = requests.put(f"{BASE}/{tid}", json=payload)
        if r.status_code == 200:
            print("Atualizada:", r.json())
        else:
            print("Erro:", r.status_code, r.text)
    except requests.RequestException as e:
        print("Erro de conexão:", e)

def deletar_tarefa():
    tid = input("ID da tarefa: ").strip()
    if not tid.isdigit():
        print("ID inválido")
        return
    try:
        r = requests.delete(f"{BASE}/{tid}")
        if r.status_code == 200:
            print(r.json().get('message'))
        else:
            print("Erro:", r.status_code, r.text)
    except requests.RequestException as e:
        print("Erro de conexão:", e)

def menu():
    while True:
        print("\n===== MENU =====")
        print("1 - Criar tarefa")
        print("2 - Listar tarefas")
        print("3 - Visualizar tarefa por ID")
        print("4 - Atualizar tarefa")
        print("5 - Deletar tarefa")
        print("0 - Sair")
        opc = input("Opção: ").strip()
        if opc == "1":
            criar_tarefa()
        elif opc == "2":
            listar_tarefas()
        elif opc == "3":
            visualizar_tarefa()
        elif opc == "4":
            atualizar_tarefa()
        elif opc == "5":
            deletar_tarefa()
        elif opc == "0":
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    menu()
