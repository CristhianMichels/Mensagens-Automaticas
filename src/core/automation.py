import time
import pyautogui
import os
import pyperclip
import re
import pygetwindow as gw
import src.utils.utils as utils


def escrever(texto):
    """ 
    Digita um texto simples na interface ativa e envia com Enter.

    Esta função usa o `pyautogui` para escrever caracteres sem suporte
    especial (acentuação, emojis, caracteres de outra codificação etc.).
    Após escrever, envia automaticamente a tecla Enter.

    Atenção:
        - Requer que a janela correta já esteja aberta.
        - Não suporta caracteres especiais; use `caracteres_especiais()`.

    Args:
        texto (str): Texto a ser digitado.

    Returns:
        None
    """
        
    pyautogui.write(texto)
    time.sleep(0.5)
    pyautogui.press("enter")
    
    
def caracteres_especiais(texto):
    """ 
    Cola texto contendo caracteres especiais usando a área de transferência.

    A função copia o texto para a área de transferência usando `pyperclip`
    e executa o atalho Ctrl+V para colar. É útil quando `pyautogui.write()`
    não consegue reproduzir corretamente acentos, emojis ou símbolos.

    Nota:
        - Esta função utiliza a área de transferência do sistema, mas **não**
          é responsável por salvar ou restaurar o conteúdo original. Caso a
          aplicação precise manter a área de transferência intacta, essa lógica
          deve ser tratada externamente (fora desta função).

    Args:
        texto (str): Conteúdo a ser colado.

    Returns:
        None
    """
    
    pyperclip.copy(texto)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.6)
    pyautogui.press('enter')


def focar_arquivo(caminho):
    """
    Tenta ativar a janela correspondente ao arquivo ou pasta aberta.

    A função procura, por até 10 tentativas, uma janela cujo título contenha
    o nome do arquivo/pasta especificado e tenta ativá-la usando o `pygetwindow`.

    Observações:
        - Essencial para evitar que pop-ups capturem o foco.
        - A ativação pode falhar caso permissões ou o SO impeçam.
        - Funciona somente em Windows.

    Args:
        caminho (str): Caminho do arquivo ou pasta cujo foco deve ser ativado.

    Returns:
        bool: True se a janela foi ativada com sucesso; False caso contrário.
    """
    
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

def copiar_colar_arquivos():
    """
    Copia o(s) arquivo(s) selecionado(s), fecha a janela atual do Explorer
    e cola no chat, enviando-os automaticamente.

    A sequência executada é:
        1. Ctrl+C — copia os arquivos selecionados.
        2. Alt+F4 — fecha a janela do Explorer que foi aberta anteriormente.
        3. Ctrl+V — cola os arquivos no campo de envio do chat.
        4. Enter — confirma o envio.

    Observações:
        - Funciona somente no Windows.
        - O envio pode falhar se outra janela capturar o foco, porém a chance é baixa.
    """
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(3)
 

def verificar_caminho(caminho):
    """
    Verifica se o caminho existe
    caso não exista, retorna o erro.
    """
    if not os.path.exists(caminho): # Se o caminho não existe, retorna o erro
        erro = f'Caminho do arquivo "{caminho}" não encontrado'
        print(erro)
        return False, erro
    return True, None


def enviar_imagem(caminho):
    """
    Envia uma única imagem através do chat automatizando o Explorer.

    O arquivo é aberto via `os.startfile()`, a janela é focada, o arquivo
    é copiado e enviado ao chat usando `copiar_colar_arquivos()`.

    Compatibilidade:
        - Funciona somente em Windows.
        - Aceita qualquer extensão que o Explorer abra como imagem.

    Args:
        caminho (str): Caminho completo do arquivo de imagem.

    Returns:
        tuple:
            bool: True se enviado com sucesso; False se houve erro; False se o sistema operacional não for windows..
            str | None: Caminho do arquivo em caso de erro, None caso contrário.
    """
    try:
        sistema = utils.identificar_sistema_operacional()
        if sistema != 'Windows':
            return False, 'Alerta: Comandos especiais funcionam apenas para Windows'
        
        sucesso, info = verificar_caminho(caminho)
        if not sucesso:
            return False, info
    
        os.startfile(caminho)
        time.sleep(2)
        
        focou = focar_arquivo(caminho)
        if not focou:
            print("Aviso: não foi possível focar a janela do arquivo")
        time.sleep(0.2)
        
        copiar_colar_arquivos()
        
        return True, None
    
    except:
        return False, 'O envio de imagem falhou'

def enviar_arquivos_pasta(caminho):
    """
    Envia todos os arquivos de uma pasta via chat.

    A função abre a pasta, ativa a janela, seleciona todos os arquivos
    com Ctrl+A e os envia usando `copiar_colar_arquivos()`.

    Compatibilidade:
        - Funciona somente em Windows.
        - Depende totalmente do Explorer e da interface gráfica.

    Args:
        caminho (str): Caminho da pasta.

    Returns:
        tuple:
            bool: True se o envio foi bem-sucedido; False caso o caminho não exista; False se o sistema operacional não for windows.
            str | None: Caminho da pasta em caso de erro; None caso contrário.
    """
    try:
        sistema = utils.identificar_sistema_operacional()
        if sistema != 'Windows':
            return False, 'Alerta: Comandos especiais funcionam apenas para Windows'
        
        sucesso, info = verificar_caminho(caminho)
        if not sucesso:
            return False, info
    
        os.startfile(caminho)
        time.sleep(2)
        
        focou = focar_arquivo(caminho)
        if not focou:
            print("Aviso: não foi possível focar a janela do arquivo")
        time.sleep(0.2)
        
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.8)
        
        copiar_colar_arquivos()
        
        return True, None
    except:
        return False, 'O envio de pasta falhou'


def  executar_comando_de_arquivo(mensagem):
    """
        Verifica se a mensagem é um comando de envio de arquivo
        (/enviar_imagem ou /enviar_pasta). 
        Se for, executa a função correspondente.

        Returns:
            - (True, None)  → comando executado com sucesso
            - (False, erro) → comando executado, mas falhou
            - (None, None)  → não é comando; deve ser tratado como texto normal
    """
    comandos = {
        "/enviar_imagem" : enviar_imagem,
        "/enviar_pasta" : enviar_arquivos_pasta
    }
    
    for comando, funcao in comandos.items():
        if mensagem.startswith(comando):
            caminho = mensagem.split(" ", 1)[1].strip()
            return funcao(caminho) # Retorna sucesso, info
    return None, None # não é comando de envio de arquivo
  
    
def enviar_tudo(mensagens):
    """
    Processa uma lista de mensagens e executa ações automáticas de envio.

    A função identifica o tipo de comando:
        - `/enviar_imagem C:\Caminho\da\imagem.png'`: envia uma imagem específica.
        - `/enviar_pasta C:\Caminho\da\pasta'`: envia todos os arquivos de uma pasta.
        - Caso contrário: envia texto, se o texto conter caracteres especiais, utiliza
        - caracteres_especiais() para copiar e colar o envio de texto

    Observações:
        - Envio de arquivos (imagem e pasta) funciona somente no Windows

    Args:
        mensagens (list[str]): Lista de comandos ou textos comuns.

    Returns:
        tuple:
            bool: True se tudo ocorreu bem; False se algum arquivo falhou.
            str | None: Caminho do arquivo/pasta com erro, se houver.
    """

    try:
        erro_encontrado = None
        for mensagem in mensagens:
            sucesso, info = executar_comando_de_arquivo(mensagem)
            if sucesso is not None:
                if not sucesso:
                    erro_encontrado = info
                continue       
            
            if re.search(r"[^a-zA-Z0-9\s]", mensagem): # Verifica se tem caractéres especiais
                caracteres_especiais(mensagem)
            else:
                escrever(mensagem)
        
        if erro_encontrado:
            return False, erro_encontrado
        return True, None
    except:
        return False, 'Erro: não foi possível enviar as mensagens'