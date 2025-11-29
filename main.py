from src.gui import gui_main
import src.utils.utils as utils

def main():        
    gui_main.interface()
    
    
if __name__ == "__main__":
    area_transferencia_anterior = utils.guardar_area_transferencia() #guarda os itens copiados da aréa de transferência
    try:
        main()
    finally:
        try:
            utils.copiar_area_transferencia(area_transferencia_anterior)
        except:
            pass