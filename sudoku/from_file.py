import numpy as np
import tkinter as tk
from tkinter import filedialog

def carica_sudoku_da_file(nome_file):
    """
    Legge un Sudoku da un file di testo.
    I numeri devono essere separati SOLO da spazi. Le celle vuote sono '0'.
    """
    try:
        valori = []
        with open(nome_file, 'r') as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue # Salta le righe vuote
                
                # Divide i numeri usando gli spazi e li converte in interi
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
        print("Errore: Il file contiene caratteri non validi. Usa solo numeri e spazi.")
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