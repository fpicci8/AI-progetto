from graphic import disegna_sudoku, disegna_sudoku_finale
from logic import verifica_configurazione, backtrack
from from_file import carica_sudoku_da_file, seleziona_file


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