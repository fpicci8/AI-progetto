from graphic import disegna_sudoku, disegna_sudoku_finale
from logic import verifica_configurazione, backtrack
from from_file import carica_sudoku_da_file, seleziona_file
import tkinter as tk
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
            if len(lista_sudoku) == 1: # Se c'è un solo sudoku
                A_iniziale = lista_sudoku[0]
                A_originale = np.copy(A_iniziale) # Salviamo una copia dell'originale per la visualizzazione finale
                
                # 3. Verifica la validità logica prima di lanciare la ricerca
                valido, info_errore = verifica_configurazione(A_iniziale)
                
                if valido:
                    flag=tk.messagebox.askyesno("Visualizzazione Domini", "Vuoi visualizzare i domini possibili per le celle vuote?") 
                    disegna_sudoku(A_iniziale, flag)    
                    print("Ricerca in corso...")
                    tk.messagebox.showinfo("Ricerca", "Premi ok per avviare la risoluzione del Sudoku.")
                    statistiche_ricerca = {'nodi_espansi': 0, 'numero_backtrack': 0, 'percorso': []}
                        
                    # 4. Lancia l'algoritmo
                    if backtrack(A_iniziale, profondita=0, stats=statistiche_ricerca):# Se la ricerca ha successo, A_iniziale è ora risolto
                        print("\n" + "="*50)
                        print("SUDOKU RISOLTO CON SUCCESSO!")
                        print("="*50)
                        print(f"Nodi totali espansi:   {statistiche_ricerca['nodi_espansi']}")
                        print(f"Numero di backtrack:   {statistiche_ricerca['numero_backtrack']}")
                        print(f"Profondità soluzione:  {statistiche_ricerca.get('profondita_soluzione', 0)}")
                        print("="*50 + "\n")
                        
                        
                        flag_ordine=tk.messagebox.askyesno("Visualizzazione Ordine", "Vuoi mostrare l'ordine di completamento delle caselle?")
                        disegna_sudoku_finale(A_iniziale, A_originale, flag_ordine, statistiche_ricerca['percorso'],stats=statistiche_ricerca)
                    else:
                        print("\nNessuna soluzione trovata per la configurazione data.")
                        tk.messagebox.showinfo("Risoluzione Fallita", "\nNessuna soluzione trovata per la configurazione data.")
                else:
                    print("\nErrore di configurazione: La configurazione di partenza viola i vincoli del Sudoku.")
                    tk.messagebox.showinfo("Errore di Configurazione", "\nErrore: La configurazione di partenza viola i vincoli del Sudoku.")
                    disegna_sudoku(A_iniziale, 0, errore=info_errore)
            
            # ==================================================
            # CASO B: SUDOKU MULTIPLI (Modalità Batch Silenziosa)
            # ==================================================
            else:
                totale = len(lista_sudoku) # Numero totale di Sudoku trovati nel file
                print(f"\nTrovati {totale} Sudoku nel file.")
                print("Avvio Modalità Batch. Nessun grafico verrà mostrato.")
                print("Elaborazione e scrittura report in corso...\n")
                
                file_report = "report_prestazioni.txt"
                
                with open(file_report, "w") as f_out:
                    f_out.write("ID  | Nodi Espansi | Backtrack | Tempo (sec) | Esito\n")
                    f_out.write("-" * 55 + "\n")
                    
                    tempo_totale = 0
                    
                    for idx, A_iniziale in enumerate(lista_sudoku, 1):
                        valido, _ = verifica_configurazione(A_iniziale) # Verifica la configurazione prima di lanciare la ricerca
                        
                        if not valido:
                            f_out.write(f"#{idx:03d} | ---          | ---       | ---         | ERRORE INIZIALE\n")
                            continue
                            
                        stats = {'nodi_espansi': 0, 'numero_backtrack': 0, 'percorso': []} # Statistiche per questo Sudoku
                        
                        inizio = time.perf_counter() # Avvia il cronometro prima di chiamare backtrack
                        # NOTA: Richiede l'argomento stampa_log=False aggiunto prima in logic.py
                        risolto = backtrack(A_iniziale, profondita=0, stats=stats, stampa_log=False)
                        fine = time.perf_counter()# Ferma il cronometro subito dopo la chiamata a backtrack
                        
                        tempo_impiegato = fine - inizio # Calcola il tempo impiegato per risolvere questo Sudoku
                        tempo_totale += tempo_impiegato # Aggiorna il tempo totale accumulato
                        
                        esito = "RISOLTO" if risolto else "FALLITO" # Determina l'esito basato sul risultato di backtrack
                        f_out.write(f"#{idx:03d} | {stats['nodi_espansi']:<12} | {stats['numero_backtrack']:<9} | {tempo_impiegato:.4f}      | {esito}\n") # Scrive i risultati di questo Sudoku nel file report
                        
                        # Aggiorna la console sulla stessa riga
                        print(f"Risolto {idx}/{totale}...", end="\r")
                        
                    f_out.write("-" * 55 + "\n") 
                    f_out.write(f"TEMPO TOTALE ELABORAZIONE: {tempo_totale:.4f} secondi\n") # Scrive il tempo totale alla fine del report
                
                print(f"\n\nTest completato! Risultati salvati nel file '{file_report}'.")

        else:
            print("Errore: Impossibile elaborare il file selezionato.")
            
    else:
        print("Nessun file selezionato. Operazione annullata.")