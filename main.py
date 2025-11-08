import funcoes
import time
import re
import pyperclip
import os
import customtkinter as ctk

def main():
    try:
        area_transferencia_anterior = pyperclip.paste() #guarda os itens copiados da aréa de transferência
            
        mensagens = []
            
        #Adicionar se houver, mensagens na lista
        if os.path.exists('mensagens.txt'):
            with open('mensagens.txt', 'r') as arquivo:
                mensagens = [linha.strip() for linha in arquivo.readlines() if linha.strip()]
            
        def adicionar_mensagens():
            mensagem = campo_mensagens.get().strip()
            if mensagem:
                mensagens.append(mensagem)
                with open('mensagens.txt', 'a') as arquivo:
                    arquivo.write(str(mensagem) + '\n')
                campo_mensagens.delete(0, 'end')


        def apagar():
            mensagens.clear()
            open('mensagens.txt','w').close()

        def enviar():
            print('Você tem 5 segundos para clicar na conversa...')
            time.sleep(5)
            for mensagem in mensagens:
                if 'enviar_arquivo' in mensagem:
                    caminho = mensagem.split(" ", 1)[1]
                    funcoes.enviar_arquivo(caminho)
                else:
                    if re.search(r"[^a-zA-Z0-9\s]", mensagem):
                        funcoes.caracteres_especiais(mensagem)
                    else:
                        funcoes.escrever(mensagem)
            
        
    finally:
        try:
            pyperclip.copy(area_transferencia_anterior)
        except Exception:
            pass  # caso o clipboard esteja inacessível, não quebra o programa
        
        
    #modo
    ctk.set_appearance_mode('dark')
    #criação
    app = ctk.CTk()
    app.title('Mensagens Automáticas')
    app.geometry('350x400')
            
    #campos
    #label
    label_mensagens = ctk.CTkLabel(app, text='Mensagens Automáticas')
    label_mensagens.pack(pady = 5)
            
    #buttons
    botao_apagar = ctk.CTkButton(app, text='Apagar tudo', command=apagar)
    botao_apagar.pack(pady = 10)
            
    botao_enviar = ctk.CTkButton(app, text='Enviar', command=enviar)
    botao_enviar.pack(pady = 10)
            
    #entry
    campo_mensagens = ctk.CTkEntry(app,placeholder_text='Digite uma mensagem')
    campo_mensagens.pack(pady = 10)
            
    #buttons
    botao_adicionar = ctk.CTkButton(app, text='Adicionar', command=adicionar_mensagens)
    botao_adicionar.pack(pady = 10)
            
    #iniciar
    app.mainloop()
    
        
if __name__ == "__main__":
    main()