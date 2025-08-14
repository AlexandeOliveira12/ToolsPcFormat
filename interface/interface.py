import os
import tkinter as tk
from tkinter import ttk
from modulos import info_system, disco, limpeza, relatorio

# -------------------- Função principal --------------------
def criar_interface():
    root = tk.Tk()
    root.title("🛠 Manutenção do PC")
    root.geometry("650x500")
    root.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Segoe UI", 10), padding=6)
    style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[10, 5])

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # -------------------- Função para criar botão --------------------
    def botao(master, texto, comando):
        return ttk.Button(master, text=texto, command=comando)

    # -------------------- Aba: Informações --------------------
    frame_info = ttk.Frame(notebook, padding=10)
    notebook.add(frame_info, text="ℹ️ Informações")

    botao(frame_info, "💻 Info do Sistema", lambda: mostrar_info(info_system.coletar_info())).pack(pady=5, fill="x")
    botao(frame_info, "💽 Saúde do Disco", disco.verificar_saude_disco).pack(pady=5, fill="x")
    botao(frame_info, "📝 Gerar Relatório", relatorio.gerar_relatorio).pack(pady=5, fill="x")

    # -------------------- Aba: Manutenção --------------------
    frame_manut = ttk.Frame(notebook, padding=10)
    notebook.add(frame_manut, text="🧹 Manutenção")

    botao(frame_manut, "🧹 Limpar Arquivos Temporários", limpeza.limpar_temporarios).pack(pady=5, fill="x")

    root.mainloop()


# -------------------- Exibir informações do sistema --------------------
def mostrar_info(info):
    win = tk.Toplevel()
    win.title("ℹ️ Informações do Sistema")
    win.geometry("500x400")
    win.resizable(False, False)

    text = tk.Text(win, wrap="word", font=("Segoe UI", 10))
    text.pack(expand=True, fill="both")
    for chave, valor in info.items():
        text.insert("end", f"{chave}: {valor}\n")
    text.config(state="disabled")
