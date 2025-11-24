import os

arquivo_mensagem = 'mensagens.txt'


def carregar_mensagens():
    if os.path.exists(arquivo_mensagem):
        with open(arquivo_mensagem, 'r') as arquivo:
            return [linha.strip() for linha in arquivo.readlines() if linha.strip()]
        
    return []


def salvar_mensagens(lista):
    with open(arquivo_mensagem, "w") as arquivo:
        for msg in lista:
            arquivo.write(msg + "\n")


def adicionar_mensagens(lista, mensagem):
    mensagem = mensagem.strip()
    if mensagem:
        lista.append(mensagem)
        with open(arquivo_mensagem, 'a') as arquivo:
            arquivo.write(str(mensagem) + '\n')
        return True
    return False


def apagar_tudo(lista):
    lista.clear()
    open(arquivo_mensagem,'w').close()