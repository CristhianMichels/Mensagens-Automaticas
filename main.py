import funcoes
import time
import pyautogui


mensagens = []
while True:
    #Adicionar mensagens caso não tenha sido adicionado ainda
    if not mensagens:
        while True:
            nova_mensagem = funcoes.validacao('Adicionar uma mensagem?')        
            if nova_mensagem == 's':
                mensagem = input('Digite a mensagem: ')
                mensagens.append(mensagem)
            else:
                break
    print(mensagens)

    #limpar as mensagens
    apagar_mensagens = funcoes.validacao('Apagar as mensagens?')
    if apagar_mensagens == 's':
        mensagens = []  
    else:
    #enviar mensagens
        executar = funcoes.validacao('Enviar mensagens?')
        if executar == 's':
            time.sleep(3)
            for mensagem in mensagens:
                pyautogui.write(mensagem)
                time.sleep(0.5)
                pyautogui.press("enter")
        else:
            break
        
        


    
