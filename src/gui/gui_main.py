import src.core.controller as controller
import src.core.messages_repo as messages_repo
import src.gui.gui_help as gui_help
import customtkinter as ctk

def interface():
    janela_ajuda = None
    
    mensagens = messages_repo.carregar_mensagens() #inicia a lista das mensagens
    
    def limpar_alerta():
        """Limpa o texto do alerta de erros na interface."""
        label_alerta.configure(text='')
     
        
    def alerta(msg_alerta):
        label_alerta.configure(text=msg_alerta, font=ctk.CTkFont(size=14))
        
                 
    def adicionar():
        """Adiciona a mensagem digitada na lista, atualiza a Textbox e habilita botões desativados"""
        mensagem = campo_mensagens.get().strip()
        if controller.adicionar(mensagem,mensagens):
            campo_mensagens.delete(0, 'end')
        else:
            alerta('A Mensagem está vazia')
        renderizar_textbox() # Atualiza o Textbox para visualizar as mensagens
        ativar_botoes()


    def apagar():
        """Remove todas as mensagens da lista, limpa o arquivo, atualiza a Textbox e alertas da interface."""
        controller.apagar(mensagens)
        renderizar_textbox()
        ativar_botoes()     
        limpar_alerta() # Limpa o alerta de erros


    def enviar():
        """Envia todas as mensagens da lista após uma contagem regressiva."""
        segundos = 5 # Tempo em segundos antes de iniciar o envio
        desativar_botoes() # Desativa os botões para evitar interações durante o envio
        
        def atualizar_contagem():
            """Atualiza a contagem regressiva e envia as mensagens ao final."""
            nonlocal segundos
            alerta(f"Você tem {segundos} segundos para clicar na conversa...")

            if segundos >= 0:
                segundos -= 1
                app.after(1200, atualizar_contagem)
            else:
                sucesso, info = controller.enviar_tudo(mensagens) # Envia todas as mensagens
                ativar_botoes() 
                
                if sucesso:
                    limpar_alerta()
                else:
                    alerta(f'Caminho do arquivo "{info}" não encontrado')
                    label_alerta.configure(font=ctk.CTkFont(size=12))
                    # Informa qual mensagem possui caminho de arquivo inválido
                
        atualizar_contagem()

    
    def renderizar_textbox():
        """Exibe o conteúdo da lista de mensagens na Textbox."""
        bloco_texto.configure(state='normal')
        bloco_texto.delete("1.0", "end")
        for msg in mensagens:
            bloco_texto.insert("end", msg + "\n")
        bloco_texto.edit_modified(False)
        bloco_texto.configure(state='normal')


    def sincronizar_lista_com_textbox():
        """Atualiza a lista 'mensagens' com o que está na Textbox."""
        conteudo = bloco_texto.get("1.0", "end").strip()
        controller.sincronizar(conteudo, mensagens)
        campo_mensagens.delete(0, 'end')
        ativar_botoes()
    
    
    def desativar_botoes():
        """Desativa todos os botões da interface"""
        botao_atualizar.configure(state="disabled")
        botao_apagar.configure(state="disabled")
        botao_enviar.configure(state="disabled")
        botao_adicionar.configure(state="disabled")
     
        
    def ativar_botoes():
        """Ativa todos os botões da interface"""
        botao_atualizar.configure(state="normal")
        botao_apagar.configure(state="normal")
        botao_enviar.configure(state="normal")
        botao_adicionar.configure(state="normal")
       
                 
    def modificar_textbox(event=None):
        """Detecta alterações no conteúdo da Textbox e ajusta os botões da interface."""
        if bloco_texto.edit_modified():
            bloco_texto.edit_modified(False)
            desativar_botoes()
            limpar_alerta() # Limpa o alerta de erros, presumindo que o usuário corrigirá o problema
            botao_atualizar.configure(state="normal") # Força o usuário clicar no botão atualizar
    
    
    def modificar_entry(event=None):
        """Detecta alterações no campo de entrada e habilita o botão 'Adicionar'."""
        desativar_botoes()
        limpar_alerta()
        botao_adicionar.configure(state="normal")
        
    
    def abrir_ajuda():
        """Abre a Janela de ajuda/tutorial"""
        nonlocal janela_ajuda
        desativar_botoes()
        
        if janela_ajuda is not None and janela_ajuda.winfo_exists(): # Foca na janela de ajuda
            janela_ajuda.focus()
            return

        def ao_fechar():
            """Função chamada ao fechar a janela de ajuda; destrói a janela e reativa os botões."""
            nonlocal janela_ajuda
            janela_ajuda.destroy()
            janela_ajuda = None
            ativar_botoes()

        janela_ajuda = gui_help.help_interface(master=app) # Cria a janela de ajuda

        janela_ajuda.protocol("WM_DELETE_WINDOW", ao_fechar)              
     
    # ======== INTERFACE ============
    ctk.set_appearance_mode('dark')

    #Cria a janela
    app = ctk.CTk()
    app.title('Mensagens Automáticas')
    app.geometry('350x450')

    # Configurações de grid para centralização vertical
    app.grid_rowconfigure((0, 1, 2, 3), weight=1)
    app.grid_columnconfigure(0, weight=1)

    # Label (título)
    label_mensagens = ctk.CTkLabel(app, text='Mensagens Automáticas', font=ctk.CTkFont(size=15, weight="bold"))
    label_mensagens.grid(row=0, column=0, pady=(10, 3))
    
    # Botão de ajuda ao lado esquerdo
    botao_ajuda = ctk.CTkButton(
        app,
        text="?",
        width=15,
        height=20,
        corner_radius=20,
        command=abrir_ajuda
    )
    botao_ajuda.grid(row=0, column=0, padx=(17, 10), sticky="w")
    
    # ======== BLOCO DE TEXTO (Textbox) ========
    frame_texto = ctk.CTkFrame(app)
    frame_texto.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")

    bloco_texto = ctk.CTkTextbox(frame_texto, width=350, height=250, corner_radius=8)
    bloco_texto.pack(fill="both", expand=True, padx=5, pady=5)

    bloco_texto.edit_modified(False)
    bloco_texto.bind("<<Modified>>", modificar_textbox)

    # Inicializa com mensagens existentes
    renderizar_textbox()
    
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

    
    # Frame da área de alerta
    frame_alerta = ctk.CTkFrame(frame_principal, fg_color='transparent')
    frame_alerta.grid(row=2, column=0, pady=(0, 10))

    label_alerta = ctk.CTkLabel(frame_alerta, text='', font=ctk.CTkFont(size=14))
    label_alerta.pack()
    

    ativar_botoes() 
    app.mainloop() # Inicia a interface