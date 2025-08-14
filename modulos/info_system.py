import platform
import socket
import psutil
import datetime
import wmi

def coletar_info():
    c = wmi.WMI()  # Inicializa o WMI antes de usar
    
    data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    sistema = f"{platform.system()} {platform.release()} {platform.architecture()[0]}"
    nome_pc = platform.node()
    ip = socket.gethostbyname(socket.gethostname())
    processador = c.Win32_Processor()[0].Name.strip()
    memoria_total = round(psutil.virtual_memory().total / (1024**3), 2)

    # Placa de vídeo
    placa_video = "N/A"
    try:
        for gpu in c.Win32_VideoController():
            if "Microsoft" not in gpu.Name:  # Ignora drivers genéricos
                placa_video = gpu.Name
                break
    except:
        pass

    # Discos
    discos = []
    for disk in c.Win32_DiskDrive():
        nome = disk.Model
        try:
            tipo = "SSD" if "SSD" in nome.upper() else "HDD"
        except:
            tipo = "Desconhecido"
    
        for part in psutil.disk_partitions():
            try:
                uso = psutil.disk_usage(part.mountpoint)
                total_gb = uso.total / (1024**3)
                livre_gb = uso.free / (1024**3)
                status = "✅ OK" if livre_gb / total_gb > 0.2 else "⚠️ Atenção"

                discos.append(
                    f"{nome} - {tipo} | Total: {total_gb:.2f} GB | Livre: {livre_gb:.2f} GB - {status}"
                )
            except PermissionError:
                pass


    return {
        "📅 Data": data,
        "💻 Sistema": sistema,
        "🖥 Nome do Computador": nome_pc,
        "🌐 Endereço IP": ip,
        "⚙️ Processador": processador,
        "🎮 Placa de Vídeo": placa_video,
        "💾 Memória Total": f"{memoria_total} GB",
        "📀 Discos": "\n".join(discos)
    }
