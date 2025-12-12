import os
import sys

def caminho_base():
    """Retorna a pasta onde o EXE está rodando, ou a pasta do script."""
    if hasattr(sys, "_MEIPASS"):
        # Estamos rodando via PyInstaller → usar a pasta onde o EXE está
        return os.path.dirname(sys.executable)
    else:
        # Rodando pelo Python normal → usar o diretório do projeto
        return os.path.dirname(os.path.abspath(__file__))


# Criar a pasta 'data' ao lado do executável se não existir
pasta_data = os.path.join(caminho_base(), "data")
os.makedirs(pasta_data, exist_ok=True)

# Caminho completo do arquivo REAL
arquivo_mensagem = os.path.join(pasta_data, "messages.txt")


def carregar_mensagens():
    """Carrega as mensagens antigas, caso existam """
    if os.path.exists(arquivo_mensagem):
        with open(arquivo_mensagem, 'r') as arquivo:
            return [linha.strip() for linha in arquivo.readlines() if linha.strip()]
        
    return []


def salvar_mensagens(lista):
    """Salva as mudanças/novas edições"""
    with open(arquivo_mensagem, "w") as arquivo:
        for msg in lista:
            arquivo.write(msg + "\n")


def adicionar_mensagens(lista, mensagem):
    """Adiciona uma nova mensagem à lista e ao arquivo."""
    mensagem = mensagem.strip()
    if mensagem:
        lista.append(mensagem)
        with open(arquivo_mensagem, 'a') as arquivo:
            arquivo.write(str(mensagem) + '\n')
        return True
    return False


def apagar_tudo(lista):
    """Apaga todas as mensagens da lista e limpa o arquivo."""
    lista.clear()
    open(arquivo_mensagem,'w').close()