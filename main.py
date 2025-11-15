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
            atualizar_textbox()

        def atualizar_textbox():
            """Exibe o conteúdo da lista de mensagens no bloco de texto."""
            bloco_texto.configure(state='normal')
            bloco_texto.delete("1.0", "end")
            for msg in mensagens:
                bloco_texto.insert("end", msg + "\n")
            bloco_texto.configure(state='normal')

        def sincronizar_lista_com_textbox():
            """Atualiza a lista 'mensagens' com o que está no bloco de texto."""
            conteudo = bloco_texto.get("1.0", "end").strip()
            novas_mensagens = [linha for linha in conteudo.split("\n") if linha.strip()]
            mensagens.clear()
            mensagens.extend(novas_mensagens)
            # Reescreve o arquivo também
            open('mensagens.txt','w').close()
            for mensagem in mensagens:
                with open('mensagens.txt', 'a') as arquivo:
                    arquivo.write(str(mensagem) + '\n')
                    campo_mensagens.delete(0, 'end')

        def apagar():
            mensagens.clear()
            open('mensagens.txt','w').close()
            atualizar_textbox()

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
        
     
    # ======== INTERFACE ================
    ctk.set_appearance_mode('dark')

    app = ctk.CTk()
    app.title('Mensagens Automáticas')
    app.geometry('350x400')

    # Configurações de grid para centralização vertical
    app.grid_rowconfigure((0, 1, 2, 3), weight=1)
    app.grid_columnconfigure(0, weight=1)

    # Label (título)
    label_mensagens = ctk.CTkLabel(app, text='Mensagens Automáticas', font=ctk.CTkFont(size=15, weight="bold"))
    label_mensagens.grid(row=0, column=0, pady=(20, 5))
    
    
    # ======== BLOCO DE TEXTO (tipo bloco de notas) ========
    frame_texto = ctk.CTkFrame(app)
    frame_texto.grid(row=0, column=0, padx=15, pady=10, sticky="nsew")

    bloco_texto = ctk.CTkTextbox(frame_texto, width=350, height=250, corner_radius=8)
    bloco_texto.pack(fill="both", expand=True, padx=5, pady=5)

    # Inicializa com mensagens existentes
    atualizar_textbox()
    
    
    
    # Frame principal que agrupa os botões e o campo de entrada
    frame_principal = ctk.CTkFrame(app, fg_color='transparent')
    frame_principal.grid(row=1, column=0, sticky="n")

    # Frame dos botões principais (alinhados à esquerda)
    frame_botoes = ctk.CTkFrame(frame_principal, fg_color='transparent')
    frame_botoes.grid(row=0, column=0, pady=5, sticky="w")
    
    botao_atualizar = ctk.CTkButton(frame_botoes, text='Atualizar', command=sincronizar_lista_com_textbox, height=28, width=80)
    botao_atualizar.pack(side='left', padx=5)

    botao_apagar = ctk.CTkButton(frame_botoes, text='Apagar tudo', command=apagar, height=28, width=90)
    botao_apagar.pack(side='left', padx=5)

    botao_enviar = ctk.CTkButton(frame_botoes, text='Enviar', command=enviar, height=28, width=80)
    botao_enviar.pack(side='left', padx=5)
    

    # Frame do campo de entrada
    frame_entry = ctk.CTkFrame(frame_principal, fg_color='transparent')
    frame_entry.grid(row=1, column=0, pady=(5, 15), sticky="w")

    campo_mensagens = ctk.CTkEntry(frame_entry, placeholder_text='Digite uma mensagem', width=200, height=32)
    campo_mensagens.pack(side='left', padx=(0, 5))

    botao_adicionar = ctk.CTkButton(frame_entry, text='Adicionar', command=adicionar_mensagens, height=30, width=90)
    botao_adicionar.pack(side='left')

    app.mainloop()
    
        
if __name__ == "__main__":
    main()