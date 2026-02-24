from graphic import disegna_sudoku, disegna_sudoku_finale
from logic import verifica_configurazione, backtrack
from from_file import carica_sudoku_da_file, seleziona_file

import numpy as np


if __name__ == "__main__":
    
    # 1. Apre la finestra di dialogo
    nome_file = seleziona_file()
    
    # Se l'utente chiude la finestra senza scegliere nulla, nome_file sarà vuoto
    if nome_file: 
        A_iniziale = carica_sudoku_da_file(nome_file)
        
        # 2. Controlla che il file sia stato letto e convertito correttamente
        if A_iniziale is not None:
            
            A_originale = np.copy(A_iniziale) # Salviamo una copia dell'originale per la visualizzazione finale
            scelta = input("Vuoi visualizzare i domini possibili per le celle vuote? (s/n): ").strip().lower()
            # Imposta il flag a 1 se l'utente risponde con 's', 'si', 'y', altrimenti 0
            flag = 1 if scelta in ['s', 'si', 'y', 'yes'] else 0    
            disegna_sudoku(A_iniziale, flag)    

            # 3. Verifica la validità logica prima di lanciare la ricerca
            if verifica_configurazione(A_iniziale) == True:
                print("Ricerca in corso...")
                statistiche_ricerca = {'nodi_espansi': 0, 'numero_backtrack': 0, 'percorso': []}
                    
                # 4. Lancia l'algoritmo
                if backtrack(A_iniziale, profondita=0, stats=statistiche_ricerca):
                    print("\n" + "="*50)
                    print("SUDOKU RISOLTO CON SUCCESSO!")
                    print("="*50)
                    print(f"Nodi totali espansi:   {statistiche_ricerca['nodi_espansi']}")
                    print(f"Numero di backtrack:   {statistiche_ricerca['numero_backtrack']}")
                    print(f"Profondità soluzione:  {statistiche_ricerca.get('profondita_soluzione', 0)}")
                    print("="*50 + "\n")
                    
                    
                    scelta_ordine = input("Vuoi mostrare l'ordine di completamento delle caselle? (s/n): ").strip().lower()
                    flag_ordine = 1 if scelta_ordine in ['s', 'si', 'y', 'yes'] else 0
                    
                    
                    disegna_sudoku_finale(A_iniziale, A_originale, flag_ordine, statistiche_ricerca['percorso'])
                else:
                    print("\nNessuna soluzione trovata per la configurazione data.")
            else:
                print("\nErrore: La configurazione di partenza viola i vincoli del Sudoku.")
    else:
        print("Nessun file selezionato. Operazione annullata.")