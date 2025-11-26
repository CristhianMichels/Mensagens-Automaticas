import pyperclip

def copiar_area_transferencia(copiar):
    return pyperclip.copy(copiar)


def guardar_area_transferencia():
    return pyperclip.paste()