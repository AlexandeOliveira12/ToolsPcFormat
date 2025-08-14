import psutil
from tkinter import messagebox

def verificar_saude_disco():
    try:
        particoes = psutil.disk_partitions()
        status_disco = []
        
        for part in particoes:
            try:
                uso = psutil.disk_usage(part.mountpoint)
                livre_gb = uso.free / (1024 ** 3)  # GB
                livre_percent = 100 - uso.percent  # %
                
                if livre_percent > 20:
                    status = "✅ OK"
                else:
                    status = "⚠️ Pouco espaço livre"

                status_disco.append(
                    f"{part.device} - Livre: {livre_percent:.1f}% ({livre_gb:.2f} GB) - {status}"
                )
            except PermissionError:
                pass

        messagebox.showinfo(
            "📀 Saúde do Disco",
            "\n".join(status_disco) if status_disco else "Nenhuma partição disponível."
        )
    except Exception as e:
        messagebox.showerror("Erro", f"❌ Não foi possível verificar a saúde do disco.\n{e}")
