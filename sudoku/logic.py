import numpy as np

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
        stats = {'nodi_espansi': 0, 'numero_backtrack': 0, 'percorso': []}
        
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
        print(f"Profondità: {profondita:02d} | Espansione nodo ({i+1}, {j+1}) -> provo {val}")
        
        A[i, j] = val  # Ipotesi
        stats['percorso'].append((i, j)) # TRACCIA: Salva la coordinata
        
        if backtrack(A, profondita + 1, stats): # Esplorazione in profondità (passando A)
            return True
        
        # --- INIZIO BACKTRACK ---
        # Se arriviamo qui, significa che il ramo esplorato ha portato a un fallimento.
        stats['numero_backtrack'] += 1
        print(f"Profondità: {profondita:02d} | BACKTRACK su nodo ({i+1}, {j+1}) -> annullo {val}")
        A[i, j] = 0  # Backtrack: annulla l'ipotesi se fallisce
        stats['percorso'].pop() # TRACCIA: Rimuove l'ultima coordinata dal percorso
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

