import os
import sys
import tkinter as tk
import platform
import pyperclip


def caminho_icone(relativo):
    """
    Retorna o caminho correto do arquivo tanto no Python normal
    quanto no executável do PyInstaller.
    """
    # Quando rodando pelo PyInstaller
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "src", relativo)

    # Rodando normal (VSCode)
    base = os.path.dirname(os.path.abspath(__file__))  # src/utils
    base = os.path.abspath(os.path.join(base, ".."))   # src/
    return os.path.join(base, relativo)


def aplicar_icone(janela):
    """Aplica ícone universal em qualquer janela Tkinter/CTkToplevel"""
    if identificar_sistema_operacional() == 'Windows':
        janela.iconbitmap(caminho_icone("core/icon/icon32.ico"))
    else:
        icone = tk.PhotoImage(file=caminho_icone("core/icon/icon64.png"))
        janela.iconphoto(True, icone)

def identificar_sistema_operacional():
    """Identifica qual sistema operacional está sendo utilizado"""
    so = platform.system()
    print(so)  # 'Windows', 'Linux' ou 'Darwin' (macOS)
    return so

def copiar_area_transferencia(copiar):
    """Copia para a área de transferência"""
    return pyperclip.copy(copiar)


def guardar_area_transferencia():
    """Lê o conteúdo da área de transferência"""
    return pyperclip.paste()

