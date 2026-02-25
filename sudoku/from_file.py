import numpy as np
import tkinter as tk
from tkinter import filedialog

def carica_sudoku_da_file(nome_file):
    """
    Legge un Sudoku da un file di testo.
    Supporta due formati:
    1. Griglia 9x9 con numeri separati da spazi (0 per celle vuote).
    2. Stringa di 81 caratteri (formato Norvig), dove '.' o '0' indicano celle vuote.
    """
    try:
        with open(nome_file, 'r') as f:
            # Legge tutte le righe ignorando quelle vuote
            linee = [linea.strip() for linea in f if linea.strip()]
            
        if not linee:
            print("Errore: Il file è vuoto.")
            return None

        # --- FORMATO 1: Stringa singola di 81 caratteri (Es. Peter Norvig) ---
        if len(linee) == 1 and len(linee[0]) == 81:
            # Sostituisce i punti con gli zeri per compatibilità
            contenuto = linee[0].replace('.', '0') 
            # Converte ogni carattere in intero e lo piega in una matrice 9x9
            A = np.array([int(x) for x in contenuto]).reshape(9, 9)
            return A

        # --- FORMATO 2: Griglia classica separata da spazi ---
        valori = []
        for linea in linee:
            numeri_riga = [int(x) for x in linea.split()]
            valori.append(numeri_riga)
                
        A = np.array(valori, dtype=int)
        
        # Verifica strutturale
        if A.shape != (9, 9):
            print(f"Errore: Il file non contiene una griglia 9x9. Dimensioni lette: {A.shape}")
            return None
            
        return A

    except FileNotFoundError:
        print(f"Errore: Il file '{nome_file}' non è stato trovato.")
        return None
    except ValueError:
        print("Errore: Il file contiene caratteri non validi. Usa solo numeri, spazi o punti.")
        return None



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