import numpy as np
from numpy import random
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import filedialog

def elementi(A, i, j):
    """Trova gli elementi già inseriti in riga, colonna e quadrante"""
    elementi_riga = set(A[i, :]) - {0}
    elementi_colonna = set(A[:, j]) - {0}
    elementi_quadrante = set(A[i//3*3:(i//3+1)*3, j//3*3:(j//3+1)*3].flatten()) - {0} 
    return elementi_riga, elementi_colonna, elementi_quadrante

def dominio(A, i, j):
    """Calcola i numeri validi per la cella (i, j)"""
    riga, colonna, quadrante = elementi(A, i, j)
    return set(range(1, 10)) - riga - colonna - quadrante

def mrv_degree(A):
    """Sceglie la prossima cella usando MRV e Degree come spareggio"""
    dim_min = 10
    max_grado = -1
    cella_scelta = None
    
    for i in range(9):
        for j in range(9):
            if A[i, j] == 0:
                num_opzioni = len(dominio(A, i, j))
                
                # Calcolo del GRADO: conta le celle VUOTE correlate
                grado = 0
                for k in range(9):
                    if A[i, k] == 0 and k != j: grado += 1
                    if A[k, j] == 0 and k != i: grado += 1
                for m in range(i//3*3, (i//3+1)*3):
                    for n in range(j//3*3, (j//3+1)*3):
                        if A[m, n] == 0 and (m, n) != (i, j): grado += 1
                
                # Logica MRV
                if num_opzioni < dim_min:
                    dim_min = num_opzioni
                    max_grado = grado
                    cella_scelta = (i, j)
                # Logica Degree (spareggio)
                elif num_opzioni == dim_min:
                    if grado > max_grado:
                        max_grado = grado
                        cella_scelta = (i, j)
                        
    return cella_scelta


def lcv(A, i, j):
    """Ordina i valori da provare partendo da quello che crea meno vincoli"""
    possibili = dominio(A, i, j)
    valori = []
    
    for num in possibili:
        count = 0
        for k in range(9):
            if A[i, k] == 0 and num in dominio(A, i, k): count += 1
            if A[k, j] == 0 and num in dominio(A, k, j): count += 1
        for m in range(i//3*3, (i//3+1)*3):
            for n in range(j//3*3, (j//3+1)*3):
                if A[m, n] == 0 and num in dominio(A, m, n): count += 1
                
        valori.append((num, count))
        
    valori.sort(key=lambda x: x[1])
    return [val[0] for val in valori]


def backtrack(A, profondita=0, stats=None):
    #inizializzo il dizionario 
    if stats is None:
        stats = {'nodi_espansi': 0, 'numero_backtrack': 0}
        
    """Funzione ricorsiva di depth-first search"""
    cella = mrv_degree(A)
    
    # Condizione di terminazione: griglia piena
    if cella is None:
        stats['profondita_soluzione'] = profondita
        return True 
        
    i, j = cella
    valori_da_provare = lcv(A, i, j)
    
    for val in valori_da_provare:
        stats['nodi_espansi'] += 1
        print(f"Profondità: {profondita:02d} | Espansione nodo ({i}, {j}) -> provo {val}")
        
        A[i, j] = val  # Ipotesi
        
        if backtrack(A, profondita + 1, stats): # Esplorazione in profondità (passando A)
            return True
        
        # --- INIZIO BACKTRACK ---
        # Se arriviamo qui, significa che il ramo esplorato ha portato a un fallimento.
        stats['numero_backtrack'] += 1
        print(f"Profondità: {profondita:02d} | BACKTRACK su nodo ({i}, {j}) -> annullo {val}")
        A[i, j] = 0  # Backtrack: annulla l'ipotesi se fallisce
        
    return False




def verifica_configurazione(A):
    """
    Verifica se la configurazione iniziale è formalmente valida e potenzialmente risolvibile.
    """
    # 1. Controllo conflitti (numeri duplicati)
    for i in range(9):
        for j in range(9):
            val = A[i, j]
            if val != 0:
                # Rimuoviamo temporaneamente il valore per usare la funzione elementi()
                A[i, j] = 0
                riga, colonna, quadrante = elementi(A, i, j)
                if val in riga or val in colonna or val in quadrante:
                    A[i, j] = val # Ripristiniamo
                    print(f"Errore di configurazione: Il valore {val} in posizione ({i}, {j}) viola le regole, è un duplicato.")
                    return False
                A[i, j] = val # Ripristiniamo
                
    # 2. Controllo celle senza opzioni 
    for i in range(9):
        for j in range(9):
            if A[i, j] == 0: # Solo per le celle vuote
                if len(dominio(A, i, j)) == 0: 
                    print(f"Errore di configurazione: La cella vuota in ({i}, {j}) non ha alcun valore possibile.")
                    return False
                    
    return True


# ==========================================
# FUNZIONE DI CARICAMENTO DA FILE
# ==========================================

# ==========================================
# FUNZIONE DI SELEZIONE FILE TRAMITE FINESTRA
# ==========================================
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


#===========================
#  PARTE GRAFICA
#===========================

# A è la matrice in ingresso, x è un flag per plottare o meno i domini possibili (1 si, 0 no)
def disegna_sudoku(A,x):  
    """Visualizza la matrice A con matplotlib"""
    fig, ax = plt.subplots()
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(8.5, -0.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Stato Iniziale con Domini Possibili", pad=20)

    for k in range(10):
        lw = 2.5 if k % 3 == 0 else 0.8
        ax.plot([-0.5, 8.5], [k-0.5, k-0.5], color="black", linewidth=lw)
        ax.plot([k-0.5, k-0.5], [-0.5, 8.5], color="black", linewidth=lw)

    for i in range(9):
        for j in range(9):
            if A[i, j] != 0:
                ax.text(j, i, str(A[i, j]), ha="center", va="center", fontsize=16)
    
    # creazione matrice B con i possibili valori e disegno numerini grigi
    if x==1:
        B = np.empty((9,9), dtype=object)
        for i in range(9):
            for j in range(9):
                if A[i, j] == 0:
                    elementi_riga, elementi_colonna, elementi_quadrante = elementi(A, i, j)
                    B[i, j] = set(range(1, 10)) - elementi_riga - elementi_colonna - elementi_quadrante
                
                    pos = {
                        1: (-0.30, -0.30), 2: (0.00, -0.30), 3: (0.30, -0.30),
                        4: (-0.30,  0.00), 5: (0.00,  0.00), 6: (0.30,  0.00),
                        7: (-0.30,  0.30), 8: (0.00,  0.30), 9: (0.30,  0.30),
                    }
                    for num in B[i, j]:
                        ax.text(j + pos[num][0], i + pos[num][1], str(num),
                                ha="center", va="center", fontsize=9, color="gray")
                else:
                    B[i, j] = A[i, j]            
    plt.show()
    
    
def disegna_sudoku_finale(A):
    """Visualizza il Sudoku risolto"""
    fig, ax = plt.subplots()
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(8.5, -0.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Sudoku Risolto!", pad=20)

    for k in range(10):
        lw = 2.5 if k % 3 == 0 else 0.8
        ax.plot([-0.5, 8.5], [k-0.5, k-0.5], color="black", linewidth=lw)
        ax.plot([k-0.5, k-0.5], [-0.5, 8.5], color="black", linewidth=lw)

    for i in range(9):
        for j in range(9):
            if A[i, j] != 0:
                ax.text(j, i, str(A[i, j]), ha="center", va="center", fontsize=16, color="blue") # Numeri risolti in blu
    plt.show()    
    
# ============================
# MAIN
# ============================ 
  
if __name__ == "__main__":
    
    # 1. Apre la finestra di dialogo
    nome_file = seleziona_file()
    
    # Se l'utente chiude la finestra senza scegliere nulla, nome_file sarà vuoto
    if nome_file: 
        A_iniziale = carica_sudoku_da_file(nome_file)
        
        # 2. Controlla che il file sia stato letto e convertito correttamente
        if A_iniziale is not None:    
            disegna_sudoku(A_iniziale, 0)    

            # 3. Verifica la validità logica prima di lanciare la ricerca
            if verifica_configurazione(A_iniziale) == True:
                print("Ricerca in corso...")
                statistiche_ricerca = {'nodi_espansi': 0, 'numero_backtrack': 0}
                    
                # 4. Lancia l'algoritmo
                if backtrack(A_iniziale, profondita=0, stats=statistiche_ricerca):
                    print("\n" + "="*50)
                    print("SUDOKU RISOLTO CON SUCCESSO!")
                    print("="*50)
                    print(f"Nodi totali espansi:   {statistiche_ricerca['nodi_espansi']}")
                    print(f"Numero di backtrack:   {statistiche_ricerca['numero_backtrack']}")
                    print(f"Profondità soluzione:  {statistiche_ricerca.get('profondita_soluzione', 0)}")
                    print("="*50 + "\n")
                    
                    disegna_sudoku_finale(A_iniziale)
                else:
                    print("\nNessuna soluzione trovata per la configurazione data.")
            else:
                print("\nErrore: La configurazione di partenza viola i vincoli del Sudoku.")
    else:
        print("Nessun file selezionato. Operazione annullata.")