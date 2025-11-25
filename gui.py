import funcoes
import mensagens_repo
import customtkinter as ctk

def interface():
    mensagens = mensagens_repo.carregar_mensagens()
    
    def limpar_alerta():
        label_alerta.configure(text='')
        
              
    def adicionar():
        mensagem = campo_mensagens.get().strip()
        if mensagens_repo.adicionar_mensagens(mensagens, mensagem):
            campo_mensagens.delete(0, 'end')
        atualizar_textbox()
        ativar_botoes()


    def apagar():
        mensagens_repo.apagar_tudo(mensagens)
        atualizar_textbox()
        ativar_botoes()
        limpar_alerta()


    def enviar():
        segundos = 5
        desativar_botoes()
        
        def atualizar_contagem():
            nonlocal segundos
            label_alerta.configure(text=f"Você tem {segundos} segundos para clicar na conversa...")

            if segundos >= 0:
                segundos -= 1
                app.after(1200, atualizar_contagem)
            else:
                sucesso, info = funcoes.enviar_tudo(mensagens)
                ativar_botoes()
                
                if sucesso:
                    limpar_alerta()
                else:
                    label_alerta.configure(text=f'Caminho do arquivo "{info}" não encontrado', font=ctk.CTkFont(size=12) )    
                
        atualizar_contagem()


    
    def atualizar_textbox():
        """Exibe o conteúdo da lista de mensagens no bloco de texto."""
        bloco_texto.configure(state='normal')
        bloco_texto.delete("1.0", "end")
        for msg in mensagens:
            bloco_texto.insert("end", msg + "\n")
        bloco_texto.edit_modified(False)
        bloco_texto.configure(state='normal')


    def sincronizar_lista_com_textbox():
        """Atualiza a lista 'mensagens' com o que está no bloco de texto."""
        conteudo = bloco_texto.get("1.0", "end").strip()
        novas_mensagens = [linha for linha in conteudo.split("\n") if linha.strip()]
        
        mensagens.clear()
        mensagens.extend(novas_mensagens)
        
        mensagens_repo.salvar_mensagens(mensagens)
        campo_mensagens.delete(0, 'end')
        
        ativar_botoes()
    
    
    def desativar_botoes():
        botao_atualizar.configure(state="disabled")
        botao_apagar.configure(state="disabled")
        botao_enviar.configure(state="disabled")
        botao_adicionar.configure(state="disabled")
     
        
    def ativar_botoes():
        botao_atualizar.configure(state="normal")
        botao_apagar.configure(state="normal")
        botao_enviar.configure(state="normal")
        botao_adicionar.configure(state="normal")
       
                 
    def modificar_textbox(event=None):
        if bloco_texto.edit_modified():
            bloco_texto.edit_modified(False)
            desativar_botoes()
            limpar_alerta()
            botao_atualizar.configure(state="normal")
    
    
    def modificar_entry(event=None):
        desativar_botoes()
        botao_adicionar.configure(state="normal")
        
                  
     
    # ======== INTERFACE ================
    ctk.set_appearance_mode('dark')

    app = ctk.CTk()
    app.title('Mensagens Automáticas')
    app.geometry('350x450')

    # Configurações de grid para centralização vertical
    app.grid_rowconfigure((0, 1, 2, 3), weight=1)
    app.grid_columnconfigure(0, weight=1)

    # Label (título)
    label_mensagens = ctk.CTkLabel(app, text='Mensagens Automáticas', font=ctk.CTkFont(size=15, weight="bold"))
    label_mensagens.grid(row=0, column=0, pady=(10, 3))
    
    
    # ======== BLOCO DE TEXTO (tipo bloco de notas) ========
    frame_texto = ctk.CTkFrame(app)
    frame_texto.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")

    bloco_texto = ctk.CTkTextbox(frame_texto, width=350, height=250, corner_radius=8)
    bloco_texto.pack(fill="both", expand=True, padx=5, pady=5)

    bloco_texto.edit_modified(False)
    bloco_texto.bind("<<Modified>>", modificar_textbox)

    # Inicializa com mensagens existentes
    atualizar_textbox()
    
    
    
    # Frame principal que agrupa os botões e o campo de entrada
    frame_principal = ctk.CTkFrame(app, fg_color='transparent')
    frame_principal.grid(row=2, column=0, sticky="n")

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
    campo_mensagens.bind("<KeyRelease>", modificar_entry)

    botao_adicionar = ctk.CTkButton(frame_entry, text='Adicionar', command=adicionar, height=30, width=90)
    botao_adicionar.pack(side='left')
    
    frame_alerta = ctk.CTkFrame(frame_principal, fg_color='transparent')
    frame_alerta.grid(row=2, column=0, pady=(0, 10))

    label_alerta = ctk.CTkLabel(frame_alerta, text='', font=ctk.CTkFont(size=14))
    label_alerta.pack()

    ativar_botoes()
    app.mainloop()