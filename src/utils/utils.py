import pyperclip


def copiar_area_transferencia(copiar):
    """Copia para a área de transferência"""
    return pyperclip.copy(copiar)


def guardar_area_transferencia():
    """Lê o conteúdo da área de transferência"""
    return pyperclip.paste()