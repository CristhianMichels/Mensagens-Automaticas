import time
import pyautogui


def validacao(texto):   
    while True:
        validar = input(f'{texto} (S/N) ').lower()
        if validar in ('s','n'):
            return validar
        print('Por favor, digite S ou N')


def escrever(texto):
    pyautogui.write(texto)
    time.sleep(0.5)
    pyautogui.press("enter")