import time
import pyautogui
import os
import pyperclip

#Valida decisão de continuar (sim ou não)
def validacao(texto):   
    while True:
        validar = input(f'{texto} (S/N) ').lower()
        if validar in ('s','n'):
            return validar
        print('Por favor, digite S ou N')

#Escreve o texto
def escrever(texto):
    pyautogui.write(texto)
    time.sleep(0.5)
    pyautogui.press("enter")
    
def caracteres_especiais(texto):
    pyperclip.copy(texto)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('enter')

        
#Envia arquivos (vídeo, foto, pdf, etc)
def enviar_arquivo(caminho):
    if not os.path.exists(caminho): #se não existir ou não encontrar função retorna
        print(f'Arquivo não encontrado {caminho}')
        return

    os.startfile(caminho)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.5)
    pyautogui.press('enter')
    time.sleep(2)



    