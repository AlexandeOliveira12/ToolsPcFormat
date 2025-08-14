import subprocess
from tkinter import messagebox
import json

def listar_programas_inicializacao():
    try:
        comando = [
            "powershell",
            "-Command",
            "Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, Location | ConvertTo-Json"
        ]
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        programas = json.loads(resultado.stdout)
        if isinstance(programas, dict):
            programas = [programas]

        habilitados = []
        desabilitados = []

        # Verifica no Registro se está habilitado ou não
        for p in programas:
            nome = p.get("Name", "(Desconhecido)")
            comando_exec = p.get("Command", "(Sem comando)")

            # Consulta status no Registro
            check_status_cmd = [
                "powershell",
                "-Command",
                f"Get-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run' | Select-Object -Property * | ConvertTo-Json"
            ]
            reg_status = subprocess.run(check_status_cmd, capture_output=True, text=True)
            status_data = reg_status.stdout.lower()

            if nome.lower() in status_data:
                habilitados.append(f"{nome}\n{comando_exec}")
            else:
                desabilitados.append(f"{nome}\n{comando_exec}")

        msg = "⚡ Programas de Inicialização\n\n"
        msg += "✅ Habilitados:\n" + ("\n\n".join(habilitados) if habilitados else "(Nenhum)") + "\n\n"
        msg += "❌ Desabilitados:\n" + ("\n\n".join(desabilitados) if desabilitados else "(Nenhum)")

        messagebox.showinfo("⚡ Programas de Inicialização", msg)

    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao listar programas de inicialização:\n{e}")
