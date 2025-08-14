import os
import subprocess
from tkinter import messagebox

PASTA_INSTALADORES = os.path.join(os.getcwd(), "instaladores")

def listar_instaladores():
    if not os.path.exists(PASTA_INSTALADORES):
        os.makedirs(PASTA_INSTALADORES)
    # Agora pegamos arquivos .exe e .msi
    arquivos = [f for f in os.listdir(PASTA_INSTALADORES) if f.lower().endswith((".exe", ".msi"))]
    return arquivos

def executar_instalador(nome_arquivo):
    caminho = os.path.join(PASTA_INSTALADORES, nome_arquivo)
    if not os.path.exists(caminho):
        messagebox.showerror("Erro", f"Arquivo {nome_arquivo} não encontrado.")
        return
    try:
        # Para executar .msi, usamos msiexec
        if nome_arquivo.lower().endswith(".msi"):
            subprocess.Popen(["msiexec", "/i", caminho])
        else:
            subprocess.Popen([caminho])
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao executar {nome_arquivo}:\n{e}")
