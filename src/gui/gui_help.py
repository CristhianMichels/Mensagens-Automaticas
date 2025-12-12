import customtkinter as ctk
from src.utils.utils import aplicar_icone
import tkinter as tk



def help_interface(master = None):
    # Criar a janela
        janela_ajuda = tk.Toplevel(master)
        janela_ajuda.title("Ajuda / Tutorial")
        janela_ajuda.geometry("340x400")
        janela_ajuda.attributes("-topmost", True)
        janela_ajuda.configure(bg="#1F1F1F")
        
        janela_ajuda.after(0, lambda: aplicar_icone(janela_ajuda))

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
        cmd_text1 = texto_normal('/enviar_imagem C:\Caminho\da\imagem.png')
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
        cmd_text2 = texto_normal('/enviar_pasta C:\Caminho\da\pasta')
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
        
        return janela_ajuda