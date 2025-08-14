import subprocess
import tkinter.messagebox as messagebox
import json

def verificar_atualizacoes():
    try:
        # Verifica se o módulo PSWindowsUpdate está instalado
        check_cmd = [
            "powershell",
            "-Command",
            "Get-Module -ListAvailable PSWindowsUpdate | ConvertTo-Json"
        ]
        resultado_check = subprocess.run(check_cmd, capture_output=True, text=True)

        if not resultado_check.stdout.strip() or resultado_check.stdout.strip() == "null":
            messagebox.showwarning(
                "📦 PSWindowsUpdate não encontrado",
                "O módulo PSWindowsUpdate não está instalado.\n\n"
                "Para instalar, execute no PowerShell como administrador:\n\n"
                "Install-Module -Name PSWindowsUpdate -Force\n"
            )
            return

        # Executa a verificação de atualizações
        resultado = subprocess.run(
            ["powershell", "-Command", "Get-WindowsUpdate | ConvertTo-Json"],
            capture_output=True, text=True
        )

        try:
            updates = json.loads(resultado.stdout)
        except:
            updates = None

        if updates:
            if isinstance(updates, dict):
                updates = [updates]
            nomes = "\n".join([u.get("Title", "Atualização") for u in updates])
            messagebox.showinfo(
                "📦 Atualizações do Windows",
                f"Há atualizações disponíveis:\n\n{nomes}"
            )
        else:
            messagebox.showinfo(
                "📦 Atualizações do Windows",
                "✅ Seu Windows está atualizado."
            )

    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível verificar atualizações.\n{e}")
