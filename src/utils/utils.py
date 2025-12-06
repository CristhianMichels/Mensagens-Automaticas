import platform
import pyperclip


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

