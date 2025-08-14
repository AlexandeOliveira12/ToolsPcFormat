import os
import shutil
import ctypes
import psutil
from tkinter import messagebox

def tamanho_pasta(caminho):
    total = 0
    for dirpath, dirnames, filenames in os.walk(caminho, topdown=True):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total += os.path.getsize(fp)
            except:
                pass
    return total

def limpar_temporarios():
    caminhos = {
        "Arquivos Temporários": [
            os.environ.get("TEMP"),
            os.environ.get("TMP"),
            "C:\\Windows\\Temp"
        ],
        "Cache Microsoft Edge": os.path.expandvars(r"%LOCALAPPDATA%\\Microsoft\\Edge\\User Data\\Default\\Cache"),
        "Cache Google Chrome": os.path.expandvars(r"%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\Cache"),
        "Cache Mozilla Firefox": os.path.expandvars(r"%APPDATA%\\Mozilla\\Firefox\\Profiles")
    }

    removidos = 0
    erros = 0
    espaco_liberado = 0
    itens_removidos = []

    # Limpa pastas especificadas
    for nome, caminhos_lista in caminhos.items():
        if isinstance(caminhos_lista, str):
            caminhos_lista = [caminhos_lista]
        for pasta in caminhos_lista:
            if pasta and os.path.exists(pasta):
                espaco_antes = tamanho_pasta(pasta)
                try:
                    for item in os.listdir(pasta):
                        caminho_item = os.path.join(pasta, item)
                        try:
                            if os.path.isfile(caminho_item) or os.path.islink(caminho_item):
                                os.remove(caminho_item)
                                removidos += 1
                            elif os.path.isdir(caminho_item):
                                shutil.rmtree(caminho_item, ignore_errors=True)
                                removidos += 1
                        except Exception:
                            erros += 1
                    espaco_depois = tamanho_pasta(pasta)
                    liberado = espaco_antes - espaco_depois
                    if liberado > 0:
                        espaco_liberado += liberado
                        itens_removidos.append(f"{nome}: {liberado / (1024**2):.2f} MB")
                except PermissionError:
                    erros += 1

    # Esvaziar lixeira
    try:
        SHERB_NOCONFIRMATION = 0x00000001
        SHERB_NOPROGRESSUI = 0x00000002
        SHERB_NOSOUND = 0x00000004
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None,
            SHERB_NOCONFIRMATION | SHERB_NOPROGRESSUI | SHERB_NOSOUND)
        itens_removidos.append("Lixeira esvaziada")
    except Exception:
        erros += 1

    espaco_liberado_gb = round(espaco_liberado / (1024**3), 2)

    messagebox.showinfo(
        "🧹 Limpeza Concluída",
        f"✅ Itens removidos: {removidos}\n"
        f"💾 Espaço liberado: {espaco_liberado_gb} GB\n"
        f"🗑 Detalhes:\n- " + "\n- ".join(itens_removidos) +
        (f"\n⚠️ Não foi possível remover: {erros}" if erros else "")
    )