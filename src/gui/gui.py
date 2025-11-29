import src.core.automation as automation
import src.core.mensagens_repo as mensagens_repo
import customtkinter as ctk

def interface():
    mensagens = mensagens_repo.carregar_mensagens()
    
    janela_ajuda = None
    
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
                sucesso, info = automation.enviar_tudo(mensagens)
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
        
    
    def abrir_ajuda():
        nonlocal janela_ajuda
        desativar_botoes()
        
        if janela_ajuda is not None and janela_ajuda.winfo_exists():
            janela_ajuda.focus()
            return

        # Criar a janela
        janela_ajuda = ctk.CTkToplevel()
        janela_ajuda.title("Ajuda / Tutorial")
        janela_ajuda.geometry("340x400")
        janela_ajuda.attributes("-topmost", True)

        def ao_fechar():
            nonlocal janela_ajuda
            janela_ajuda.destroy()
            janela_ajuda = None
            ativar_botoes()

        janela_ajuda.protocol("WM_DELETE_WINDOW", ao_fechar)

        # Frame com scroll
        frame = ctk.CTkScrollableFrame(janela_ajuda)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ===== Títulos =====
        def titulo(texto):
            return ctk.CTkLabel(
                frame, text=texto, font=ctk.CTkFont(size=18, weight="bold"),
                fg_color=None, justify="left"
            )

        def subtitulo(texto):
            return ctk.CTkLabel(
                frame, text=texto, font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=None, justify="left"
            )

        def texto_normal(texto):
            return ctk.CTkLabel(
                frame, text=texto, font=ctk.CTkFont(size=12),
                wraplength=295, justify="left"
            )

        # ===== Resumo =====
        titulo_resumo = titulo("Resumo do Programa")
        titulo_resumo.pack(anchor="w", pady=(0, 5))
        resumo = texto_normal(
            "Este programa automatiza mensagens de vendas localmente, sem integração com APIs.\n"
            "- Permite salvar dados.\n"
            "- Valida entradas.\n"
            "- Envia mensagens de forma simples e intuitiva."
        )
        resumo.pack(pady=(0, 15))

        # ===== Como Usar =====
        titulo_como_usar = titulo("Como Usar")
        titulo_como_usar.pack(anchor="w", pady=(0, 5))
        como_usar = texto_normal(
            "1. Digite a mensagem no campo inferior e clique em 'Adicionar'.\n"
            "2. Modifique mensagens diretamente no bloco de texto se necessário.\n"
            "3. Após editar o texto, clique em 'Atualizar' para salvar as alterações.\n"
            "4. Clique em 'Enviar' e aguarde a contagem regressiva antes de selecionar a conversa.\n"
            "5. 'Apagar tudo' limpa a lista de mensagens."
        )
        como_usar.pack(pady=(0, 15))

        # ===== Apenas para Windows =====
        titulo_windows = titulo("Apenas para Windows")
        titulo_windows.pack(anchor="w", pady=(0, 5))
        # Texto introdutório
        intro = texto_normal("Estes comandos permitem enviar arquivos automaticamente (Windows apenas):")
        intro.pack(anchor="w", pady=(0, 10))

        # ===== Comando 1 =====
        sub1 = subtitulo("1. Enviar uma imagem única")
        sub1.pack(anchor="w", pady=(5, 2))

        comando1 = subtitulo("Comando:")
        comando1.pack(anchor="w", padx=20)
        cmd_text1 = texto_normal('/enviar_imagem C:\\Caminho\\da\\imagem.png')
        cmd_text1.pack(anchor="w", padx=20, pady=(0, 5))

        descricao1 = subtitulo("Descrição:")
        descricao1.pack(anchor="w", padx=20)
        desc_text1 = texto_normal(
            "- Envia apenas um arquivo de imagem por vez.\n"
            "- Suporta formatos comuns: .png, .jpg, .jpeg, etc"
        )
        desc_text1.pack(anchor="w", padx=20, pady=(0, 10))

        # ===== Comando 2 =====
        sub2 = subtitulo("2. Enviar todos os arquivos de uma pasta")
        sub2.pack(anchor="w", pady=(5, 2))

        comando2 = subtitulo("Comando:")
        comando2.pack(anchor="w", padx=20)
        cmd_text2 = texto_normal('/enviar_pasta C:\\Caminho\\da\\pasta')
        cmd_text2.pack(anchor="w", padx=20, pady=(0, 5))

        descricao2 = subtitulo("Descrição:")
        descricao2.pack(anchor="w", padx=20)
        desc_text2 = texto_normal(
            "- Envia todos os arquivos contidos na pasta.\n"
            "- Funciona com qualquer tipo de arquivo."
        )
        desc_text2.pack(anchor="w", padx=20, pady=(0, 10))

        # ===== Dicas Rápidas =====
        titulo_dicas = titulo("Dicas Rápidas")
        titulo_dicas.pack(anchor="w", pady=(0, 5))
        dicas = texto_normal(
            "• Sempre valide os dados antes de enviar.\n"
            "• Mantenha a janela principal aberta enquanto envia mensagens.\n"
            "• Use o programa apenas para fins legais e educativos."
        )
        dicas.pack(pady=(0, 10))
                  
     
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