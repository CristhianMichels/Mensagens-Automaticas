from src.gui import gui_main
import src.utils.utils as utils

def main():        
    """Inicia a interface gráfica do aplicativo."""
    gui_main.interface()
    
    
if __name__ == "__main__":
    area_transferencia_anterior = utils.guardar_area_transferencia() # Restaura o conteúdo anterior da área de transferência
    try:
        main()
    finally:
        try:
            utils.copiar_area_transferencia(area_transferencia_anterior) # Recupera os arquivos guardados anteriormente e devolve para a área de transferência
        except:
            pass 