import os
import subprocess
from tkinter import messagebox
from modulos import info_system

def gerar_relatorio():
    try:
        info = info_system.coletar_info()
        pasta_saida = os.path.join(os.getcwd(), "saida")
        os.makedirs(pasta_saida, exist_ok=True)

        caminho = os.path.join(pasta_saida, "relatorio_pc.txt")
        with open(caminho, "w", encoding="utf-8") as arquivo:
            for chave, valor in info.items():
                arquivo.write(f"{chave}: {valor}\n")

        messagebox.showinfo(
            "✅ Relatório Gerado",
            f"O relatório foi salvo com sucesso!\n\n📂 Local do arquivo:\n{caminho}"
        )

        abrir = messagebox.askyesno("📄 Abrir Relatório", "Deseja abrir o relatório agora?")
        if abrir:
            subprocess.Popen(["notepad.exe", caminho])

    except Exception as e:
        messagebox.showerror("❌ Erro", f"Não foi possível gerar o relatório.\n{e}")
