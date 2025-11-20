import time
import pyautogui
import os
import pyperclip
import re

#Escreve o texto
def escrever(texto):
    pyautogui.write(texto)
    time.sleep(0.5)
    pyautogui.press("enter")
    
    
#Escreve o texto mas com caracteres especiais
def caracteres_especiais(texto):
    pyperclip.copy(texto)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.6)
    pyautogui.press('enter')

        
#Envia arquivos (vídeo, foto, pdf, etc)
def enviar_arquivo(caminho):
    if not os.path.exists(caminho): #se não existir ou não encontrar função retorna
        print(f'Arquivo não encontrado {caminho}') #FAZER UMA OPÇÃO DE DIGITAR NOVAMENTE O CAMINHO DO ARQUIVO CASO NAO ENCONTRADO!!!!!!
        return
    
    os.startfile(caminho)
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.8)
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.5)
    pyautogui.press('enter')
    time.sleep(2)

def enviar_tudo(mensagens):
    for mensagem in mensagens:
        if 'enviar_arquivo' in mensagem:
            caminho = mensagem.split(" ", 1)[1]
            enviar_arquivo(caminho)
        else:
            if re.search(r"[^a-zA-Z0-9\s]", mensagem):
                caracteres_especiais(mensagem)
            else:
                escrever(mensagem)
