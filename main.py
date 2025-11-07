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
        botao_apagar = ctk.CTkButton(app, text='Apagar tudo')
        botao_apagar.pack(pady = 10)
        
        botao_enviar = ctk.CTkButton(app, text='Enviar')
        botao_enviar.pack(pady = 10)
        
        #entry
        campo_mensagens = ctk.CTkEntry(app,placeholder_text='Digite uma mensagem')
        campo_mensagens.pack(pady = 10)
        
        #buttons
        botao_adicionar = ctk.CTkButton(app, text='Adicionar')
        botao_adicionar.pack(pady = 10)
        
        #iniciar
        app.mainloop()
        
        
        
        #Adicionar se houver, mensagens na lista
        if os.path.exists('mensagens.txt'):
            with open('mensagens.txt', 'r') as arquivo:
                mensagens = [linha.strip() for linha in arquivo.readlines() if linha.strip()]
        
        while True:
            #Adicionar mensagens
            adicionar = funcoes.validacao('Adicionar uma nova mensagem?')
            while adicionar == 's':
                mensagem = input('Digite a mensagem:').strip()
                mensagens.append(mensagem)
                with open('mensagens.txt', 'a') as arquivo:
                    arquivo.write(str(mensagem) + '\n')
                adicionar = funcoes.validacao('Adicionar outra mensagem?')

            print(mensagens)

            #limpar as mensagens
            apagar_mensagens = funcoes.validacao('Apagar as mensagens?')
            if apagar_mensagens == 's':
                mensagens = []
                open('mensagens.txt','w').close()
            else:
            #enviar mensagens
                executar = funcoes.validacao('Enviar mensagens?')
                if executar == 's':
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
                else:
                    break
                
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        
    finally:
        # restaura o conteúdo anterior do clipboard
        try:
            pyperclip.copy(area_transferencia_anterior)
        except Exception:
            pass  # caso o clipboard esteja inacessível, não quebra o programa
        
if __name__ == "__main__":
    main()