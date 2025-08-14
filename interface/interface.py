import os
import tkinter as tk
from tkinter import ttk
from modulos import info_system, disco, limpeza, relatorio
from modulos import atualizacoes, inicializacao, antivirus
from modulos import instaladores  # novo módulo que vamos criar para gerenciar instaladores locais

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
    botao(frame_manut, "⚡ Programas de Inicialização", inicializacao.listar_programas_inicializacao).pack(pady=5, fill="x")

    # -------------------- Aba: Segurança --------------------
    frame_seg = ttk.Frame(notebook, padding=10)
    notebook.add(frame_seg, text="🛡 Segurança")

    botao(frame_seg, "📦 Atualizações do Windows", atualizacoes.verificar_atualizacoes).pack(pady=5, fill="x")
    botao(frame_seg, "🛡 Status do Antivírus", antivirus.verificar_status_antivirus).pack(pady=5, fill="x")

    # -------------------- Aba: Instaladores Locais --------------------
    frame_instaladores = ttk.Frame(notebook, padding=10)
    notebook.add(frame_instaladores, text="⬇️ Instaladores Locais")

    def atualizar_lista_instaladores():
        # Limpa os widgets anteriores para atualizar a lista
        for widget in frame_instaladores.winfo_children():
            widget.destroy()

        arquivos = instaladores.listar_instaladores()
        if not arquivos:
            ttk.Label(frame_instaladores, text="Nenhum instalador (.exe) encontrado na pasta 'instaladores'.").pack(pady=10)
            return

        for arquivo in arquivos:
            frame_arquivo = ttk.Frame(frame_instaladores)
            frame_arquivo.pack(fill="x", pady=5)

            label = ttk.Label(frame_arquivo, text=arquivo, font=("Segoe UI", 11))
            label.pack(side="left", padx=5)

            botao_executar = ttk.Button(frame_arquivo, text="Executar", command=lambda a=arquivo: instaladores.executar_instalador(a))
            botao_executar.pack(side="right", padx=5)

    atualizar_lista_instaladores()

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


if __name__ == "__main__":
    criar_interface()
