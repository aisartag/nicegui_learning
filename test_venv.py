from colorama import Fore

def stampa_colorata(testo: str, colore: str) -> None:
    print(f"{colore}{testo}{Fore.RESET}")

stampa_colorata("Ciao!", Fore.GREEN)
stampa_colorata("Ciao!", Fore.RED)
stampa_colorata("Ciao!", Fore.YELLOW)
stampa_colorata("Ciao!", Fore.BLUE) 


import sys
import os

print(os.path.dirname(__file__))

# Aggiunge la cartella corrente al path di ricerca
sys.path.append(os.path.dirname(__file__))