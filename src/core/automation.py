import time
import pyautogui
import os
import pyperclip
import re
import pygetwindow as gw

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


def focar_arquivo(caminho):
    nome = os.path.basename(caminho)

    for _ in range(10):
        for janela in gw.getAllWindows():
            if nome.lower() in janela.title.lower():
                try:
                    janela.activate()
                    time.sleep(0.2)
                    return True
                except:
                    pass
        time.sleep(0.2)

    return False
        
#Envia arquivos (vídeo, foto, pdf, etc)
def enviar_arquivo(caminho):
    if not os.path.exists(caminho):
        return False, caminho
 
    
 
    os.startfile(caminho)
    time.sleep(2)
    
    focou = focar_arquivo(caminho)
    if not focou:
        print("Aviso: não foi possível focar a janela do arquivo")
    time.sleep(0.2)

    
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.8)
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.5)
    pyautogui.press('enter')
    time.sleep(2)
    
    return True, None

def enviar_tudo(mensagens):
    erro_encontrado = None
    for mensagem in mensagens:
        if mensagem.startswith('enviar_arquivo'):
            caminho = mensagem.split(" ", 1)[1]
            sucesso, info = enviar_arquivo(caminho)
            if not sucesso:
                erro_encontrado = info
                print('Erro: ', erro_encontrado)
        else:
            if re.search(r"[^a-zA-Z0-9\s]", mensagem):
                caracteres_especiais(mensagem)
            else:
                escrever(mensagem)
    
    if erro_encontrado:
        return False, erro_encontrado
    return True, None
