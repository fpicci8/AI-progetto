import numpy as np

def elementi(A, i, j):
    """Trova gli elementi già inseriti in riga, colonna e quadrante"""
    elementi_riga = set(A[i, :]) - {0} # Rimuove lo 0 che rappresenta le celle vuote e restituisce solo i numeri già presenti nella riga i
    elementi_colonna = set(A[:, j]) - {0} # Rimuove lo 0 che rappresenta le celle vuote e restituisce solo i numeri già presenti nella colonna j
    elementi_quadrante = set(A[i//3*3:(i//3+1)*3, j//3*3:(j//3+1)*3].flatten()) - {0}  # Rimuove lo 0 che rappresenta le celle vuote e restituisce solo i numeri già presenti nel quadrante 3x3 a cui appartiene la cella (i, j)
    #data una cella (i,j), es 3,1 set (A[3//3*3:(3//3+1)*3, 1//3*3:(1//3+1)*3]) = set (A[3:6, 0:3]) e questo è  il quadrante 3x3 che contiene la cella (3,1).
    #il secondo indice non è compreso.
    return elementi_riga, elementi_colonna, elementi_quadrante

def dominio(A, i, j):
    """Calcola i numeri validi per la cella (i, j)"""
    riga, colonna, quadrante = elementi(A, i, j) 
    return set(range(1, 10)) - riga - colonna - quadrante # Restituisce i numeri da 1 a 9 che non sono già presenti in riga, colonna o quadrante

def mrv_degree(A):
    """Sceglie la prossima cella usando MRV e Degree come spareggio"""
    dim_min = 10 # Inizialmente più grande del massimo numero di opzioni (9)
    max_grado = -1 # Inizialmente più piccolo di qualsiasi grado possibile  .
    cella_scelta = None # Inizialmente nessuna cella scelta
    
    for i in range(9): # Scorre tutte le celle
        for j in range(9): 
            if A[i, j] == 0: # Solo per le celle vuote
                num_opzioni = len(dominio(A, i, j)) # Conta quante opzioni ha la cella (i, j)
                
                # Calcolo del GRADO: conta le celle VUOTE correlate
                grado = 0 
                for k in range(9):
                    if A[i, k] == 0 and k != j: grado += 1 # Cella vuota nella stessa riga (escludendo se stessa)
                    if A[k, j] == 0 and k != i: grado += 1 # Cella vuota nella stessa colonna (escludendo se stessa)
                for m in range(i//3*3, (i//3+1)*3):
                    for n in range(j//3*3, (j//3+1)*3):
                        if A[m, n] == 0 and (m, n) != (i, j): grado += 1 # Cella vuota nello stesso quadrante (escludendo se stessa)
                
                # Logica MRV
                if num_opzioni < dim_min: # Se questa cella ha meno opzioni, è la nuova candidata
                    dim_min = num_opzioni # Aggiorna il numero minimo di opzioni
                    max_grado = grado # Aggiorna il grado massimo per il nuovo candidato
                    cella_scelta = (i, j) # Aggiorna la cella scelta
                
                # Logica Degree (spareggio)
                elif num_opzioni == dim_min: # Se c'è un pareggio MRV, confronta i gradi
                    if grado > max_grado: 
                        max_grado = grado # Aggiorna il grado massimo se questo candidato ha più vincoli
                        cella_scelta = (i, j) # Aggiorna la cella scelta se questo candidato ha più vincoli
                        
    return cella_scelta # Restituisce la cella scelta con il minor numero di opzioni (MRV) e, in caso di pareggio, quella con il maggior numero di vincoli (Degree)


def lcv(A, i, j):
    """Ordina i valori da provare partendo da quello che crea meno vincoli"""
    possibili = dominio(A, i, j) 
    valori = []

    # Conta quanti vincoli (opzioni rimosse) questo numero imporrebbe agli altri
    for num in possibili:
        count = 0 
        for k in range(9):
            if A[i, k] == 0 and num in dominio(A, i, k): count += 1 # Cella vuota nella stessa riga che verrebbe limitata
            if A[k, j] == 0 and num in dominio(A, k, j): count += 1 # Cella vuota nella stessa colonna che verrebbe limitata
        for m in range(i//3*3, (i//3+1)*3):
            for n in range(j//3*3, (j//3+1)*3):
                if A[m, n] == 0 and num in dominio(A, m, n): count += 1 # Cella vuota nello stesso quadrante che verrebbe limitata
                
        valori.append((num, count))# Salva il numero e il conteggio dei vincoli che impone
        
    valori.sort(key=lambda x: x[1]) # Ordina i numeri in base al conteggio dei vincoli (LCV)
    return [val[0] for val in valori]# Restituisce solo i numeri ordinati per LCV, senza il conteggio dei vincoli


def backtrack(A, profondita=0, stats=None, stampa_log=True): 
    #inizializzo il dizionario 
    if stats is None:# Solo alla prima chiamata, inizializza le statistiche
        stats = {'nodi_espansi': 0, 'numero_backtrack': 0, 'percorso': []}
        
    """Funzione ricorsiva di depth-first search"""
    cella = mrv_degree(A) # sceglie la prossima cella da espandere usando MRV e Degree come spareggio
    
    # Condizione di terminazione: griglia piena
    if cella is None:# Se mrv_degree restituisce None, significa che non ci sono più celle vuote, quindi il Sudoku è risolto
        stats['profondita_soluzione'] = profondita # Salva la profondità a cui è stata trovata la soluzione
        return True # Restituisce True per indicare che la soluzione è stata trovata
        
    i, j = cella
    valori_da_provare = lcv(A, i, j)
    
    for val in valori_da_provare: 
        stats['nodi_espansi'] += 1 # Incrementa il contatore dei nodi espansi ogni volta che si prova un valore
        if stampa_log: 
            print(f"Profondità: {profondita:02d} | Espansione nodo ({i+1}, {j+1}) -> provo {val}") #02d formatta il numero con almeno 2 cifre, aggiungendo uno zero davanti se necessario
        
        A[i, j] = val  # Ipotesi
        stats['percorso'].append((i, j)) # TRACCIA: Salva la coordinata
        
        if backtrack(A, profondita + 1, stats, stampa_log): # Esplorazione in profondità (passando A)
            return True 
            #se la ricorsione restituisce True, significa che la soluzione è stata trovata lungo questo ramo, quindi si propaga il True verso l'alto senza fare backtrack
        
        # --- INIZIO BACKTRACK ---
        # Se arriviamo qui, significa che il ramo esplorato ha portato a un fallimento.
        stats['numero_backtrack'] += 1 # Incrementa il contatore dei backtrack ogni volta che si torna indietro
        if stampa_log:
            print(f"Profondità: {profondita:02d} | BACKTRACK su nodo ({i+1}, {j+1}) -> annullo {val}")
        A[i, j] = 0  # Backtrack: annulla l'ipotesi se fallisce
        stats['percorso'].pop() # TRACCIA: Rimuove l'ultima coordinata dal percorso
    return False 
    # se nessun valore ha funzionato, restituisce False per indicare che questa configurazione non porta a una soluzione valida



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
                if val in riga or val in colonna or val in quadrante: # Se il valore è già presente in riga, colonna o quadrante, c'è un conflitto
                    A[i, j] = val # Ripristiniamo
                    print(f"Errore di configurazione: Il valore {val} in posizione ({i+1}, {j+1}) viola le regole, è un duplicato.")
                    return False, (i,j)
                A[i, j] = val # Ripristiniamo
                
    # 2. Controllo celle senza opzioni 
    for i in range(9):
        for j in range(9):
            if A[i, j] == 0: # Solo per le celle vuote
                if len(dominio(A, i, j)) == 0: # Se una cella vuota non ha alcun numero valido da inserire, la configurazione è insoddisfacibile
                    print(f"Errore di configurazione: La cella vuota in ({i+1}, {j+1}) non ha alcun valore possibile.")
                    return False, (i,j)
                    
    return True, None

