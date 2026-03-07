import numpy as np
import tkinter as tk
from tkinter import filedialog

def carica_sudoku_da_file(nome_file):
    """
    Legge i Sudoku da un file di testo e restituisce una LISTA di matrici NumPy 9x9.
    Supporta due formati:
    1. Griglia classica 9x9: Numeri separati da spazi (0 per le celle vuote).
    2. Formato Batch (es. Norvig): Una o più righe da 81 caratteri ('.' o '0' per le celle vuote).
    """
    try:
        with open(nome_file, 'r') as f:
            # Legge tutte le righe, rimuove gli spazi extra e salta automaticamente le righe vuote
            linee = [linea.strip() for linea in f if linea.strip()]
            
        if not linee:
            print("Errore: Il file è vuoto.")
            return []

        sudokus = []

        # ==================================================
        # FORMATO 1: BATCH (Stringhe singole da 81 caratteri)
        # ==================================================
        # Se la prima riga ha esattamente 81 caratteri, gestiamo come file a riga singola/multipla
        if len(linee[0].replace('.', '0')) == 81:
            for linea in linee:
                # Sostituisce eventuali punti con zeri per compatibilità con il formato Norvig
                contenuto = linea.replace('.', '0')
                # Converte ogni carattere in intero e "piega" l'array in una matrice 9x9
                A = np.array([int(x) for x in contenuto]).reshape(9, 9)
                sudokus.append(A)
            return sudokus

        # ==================================================
        # FORMATO 2: SINGOLO (Griglia classica 9x9 con spazi)
        # ==================================================
        # Se il file ha esattamente 9 righe di testo, lo trattiamo come una griglia classica
        if len(linee) == 9:
            valori = []
            for linea in linee:
                # Divide i numeri usando gli spazi e li converte in interi
                numeri_riga = [int(x) for x in linea.split()]
                valori.append(numeri_riga)
                
            A = np.array(valori, dtype=int)
            
            # Verifica strutturale rapida
            if A.shape == (9, 9):
                sudokus.append(A)
            else:
                print(f"Errore: Dimensioni errate per la griglia. Trovata {A.shape}")
            return sudokus

        # Se non ricade in nessuno dei due casi
        print("Errore: Formato file non riconosciuto. Assicurati che sia una singola griglia 9x9 o righe da 81 caratteri.")
        return []

    except FileNotFoundError:
        print(f"Errore: Il file '{nome_file}' non è stato trovato.")
        return []
    except ValueError:
        print("Errore: Il file contiene caratteri non validi. Usa solo numeri, spazi o punti.")
        return []
    except Exception as e:
        print(f"Errore inaspettato durante la lettura del file: {e}")
        return []
    
    

def seleziona_file():
    """Apre una finestra di dialogo nativa per far scegliere il file all'utente."""
    # Crea un'istanza nascosta di tkinter (per non mostrare finestre vuote in background)
    root = tk.Tk()
    root.withdraw()
    
    # Apre la finestra di dialogo
    percorso_file = filedialog.askopenfilename(
        title="Seleziona il file di testo del Sudoku",
        filetypes=[("File di testo", "*.txt"), ("Tutti i file", "*.*")]
    )
    
    return percorso_file