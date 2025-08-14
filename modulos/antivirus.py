import subprocess
import json
from tkinter import messagebox

def verificar_status_antivirus():
    try:
        comando = [
            "powershell",
            "-Command",
            "Get-MpComputerStatus | Select-Object AMServiceEnabled, AntispywareEnabled, AntivirusEnabled | ConvertTo-Json"
        ]
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        # Converte o JSON e já normaliza booleans para string
        status = json.loads(resultado.stdout)
        
        if isinstance(status, dict):
            status = [status]

        msg = "🛡 Status do Antivírus\n\n"
        for s in status:
            msg += f"Serviço Ativo: {'✅ Sim' if s.get('AMServiceEnabled', False) else '❌ Não'}\n"
            msg += f"Antispyware: {'✅ Sim' if s.get('AntispywareEnabled', False) else '❌ Não'}\n"
            msg += f"Antivírus: {'✅ Sim' if s.get('AntivirusEnabled', False) else '❌ Não'}\n"

        messagebox.showinfo("🛡 Status do Antivírus", msg)

    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao verificar o antivírus:\n{e}")
