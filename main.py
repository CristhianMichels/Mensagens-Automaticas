import funcoes
import time
import pyautogui


mensagens = []
while True:
    if not mensagens:
        while True:
            nova_mensagem = funcoes.validacao('Adicionar uma mensagem?')        
            if nova_mensagem == 's':
                mensagem = input('Digite a mensagem: ')
                mensagens.append(mensagem)
            else:
                break
    print(mensagens)

    apagar_mensagens = funcoes.validacao('Apagar as mensagens?')
    if apagar_mensagens == 's':
        mensagens = []
    else:
        executar = funcoes.validacao('Enviar mensagens?')
        if executar == 'n':
            break
        
        


    
