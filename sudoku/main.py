from graphic import disegna_sudoku, disegna_sudoku_finale
from logic import verifica_configurazione, backtrack
from from_file import carica_sudoku_da_file, seleziona_file

import numpy as np
import time  # Aggiunto per il cronometro dei test batch

if __name__ == "__main__":
    
    # 1. Apre la finestra di dialogo
    nome_file = seleziona_file()
    
    # Se l'utente chiude la finestra senza scegliere nulla, nome_file sarà vuoto
    if nome_file: 
        # Attenzione: ora questa funzione restituisce una LISTA di matrici
        lista_sudoku = carica_sudoku_da_file(nome_file)
        
        # 2. Controlla che il file sia stato letto e convertito correttamente
        if lista_sudoku:
            
            # ==================================================
            # CASO A: UN SOLO SUDOKU (Modalità Grafica Interattiva)
            # ==================================================
            if len(lista_sudoku) == 1:
                A_iniziale = lista_sudoku[0]
                A_originale = np.copy(A_iniziale) # Salviamo una copia dell'originale per la visualizzazione finale
                
                # 3. Verifica la validità logica prima di lanciare la ricerca
                valido, info_errore = verifica_configurazione(A_iniziale)
                
                if valido:
                    scelta = input("Vuoi visualizzare i domini possibili per le celle vuote? (s/n): ").strip().lower()
                    # Imposta il flag a 1 se l'utente risponde con 's', 'si', 'y', altrimenti 0
                    flag = 1 if scelta in ['s', 'si', 'y', 'yes'] else 0    
                    disegna_sudoku(A_iniziale, flag)    
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
                    disegna_sudoku(A_iniziale, 0, errore=info_errore)
            
            # ==================================================
            # CASO B: SUDOKU MULTIPLI (Modalità Batch Silenziosa)
            # ==================================================
            else:
                totale = len(lista_sudoku)
                print(f"\nTrovati {totale} Sudoku nel file.")
                print("Avvio Modalità Batch. Nessun grafico verrà mostrato.")
                print("Elaborazione e scrittura report in corso...\n")
                
                file_report = "report_prestazioni.txt"
                
                with open(file_report, "w") as f_out:
                    f_out.write("ID  | Nodi Espansi | Backtrack | Tempo (sec) | Esito\n")
                    f_out.write("-" * 55 + "\n")
                    
                    tempo_totale = 0
                    
                    for idx, A_iniziale in enumerate(lista_sudoku, 1):
                        valido, _ = verifica_configurazione(A_iniziale)
                        
                        if not valido:
                            f_out.write(f"#{idx:03d} | ---          | ---       | ---         | ERRORE INIZIALE\n")
                            continue
                            
                        stats = {'nodi_espansi': 0, 'numero_backtrack': 0, 'percorso': []}
                        
                        inizio = time.perf_counter()
                        # NOTA: Richiede l'argomento stampa_log=False aggiunto prima in logic.py
                        risolto = backtrack(A_iniziale, profondita=0, stats=stats, stampa_log=False)
                        fine = time.perf_counter()
                        
                        tempo_impiegato = fine - inizio
                        tempo_totale += tempo_impiegato
                        
                        esito = "RISOLTO" if risolto else "FALLITO"
                        f_out.write(f"#{idx:03d} | {stats['nodi_espansi']:<12} | {stats['numero_backtrack']:<9} | {tempo_impiegato:.4f}      | {esito}\n")
                        
                        # Aggiorna la console sulla stessa riga
                        print(f"Risolto {idx}/{totale}...", end="\r")
                        
                    f_out.write("-" * 55 + "\n")
                    f_out.write(f"TEMPO TOTALE ELABORAZIONE: {tempo_totale:.4f} secondi\n")
                
                print(f"\n\nTest completato! Risultati salvati nel file '{file_report}'.")

        else:
            print("Errore: Impossibile elaborare il file selezionato.")
            
    else:
        print("Nessun file selezionato. Operazione annullata.")