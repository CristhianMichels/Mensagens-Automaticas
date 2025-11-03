import time
import pyautogui
import pyperclip
import os

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
    
#Envia arquivos (vídeo, foto, pdf, etc)
def enviar_arquivo(caminho):
    if not os.path.exists(caminho): #se não existir ou não encontrar função retorna
        print(f'Arquivo não encontrado {caminho}')
        return
    #copia e envia o arquivo
    pyperclip.copy(caminho) #copia o caminho
    
    #cola e envia o arquivo
    pyautogui.hotkey('ctrl','v')
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(2)
    