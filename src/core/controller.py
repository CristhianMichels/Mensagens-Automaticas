import src.core.messages_repo as messages_repo
import src.core.automation as automation


# Funcções Mensagens:
def adicionar(msg, lista):
    """Adiciona a mensagem digitada na lista"""
    msg = msg.strip()
    
    if not msg:
        return False
    
    messages_repo.adicionar_mensagens(lista, msg)
    return True


def apagar(lista):
    """Remove todas as mensagens da lista e limpa o arquivo"""
    messages_repo.apagar_tudo(lista)


def sincronizar(conteudo, lista):
    """Sincromiza o conteúdo da lista e do arquivo"""
    novas_mensagens = [linha for linha in conteudo.split("\n") if linha.strip()]
    
    lista.clear() # Apaga a lista antiga
    lista.extend(novas_mensagens) 
    
    messages_repo.salvar_mensagens(lista)

# Funcções Automação
def enviar_tudo(lista):
    """Envia todas as mensagens da lista"""
    sucesso, info = automation.enviar_tudo(lista)
    return sucesso, info
