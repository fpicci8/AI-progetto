
import matplotlib.pyplot as plt
import numpy as np
from logic import elementi






#===========================
#  PARTE GRAFICA
#===========================

# A è la matrice in ingresso, x è un flag per plottare o meno i domini possibili (1 si, 0 no)
def disegna_sudoku(A,x, errore=None):  
    """Visualizza la matrice A con matplotlib"""
    fig, ax = plt.subplots()
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(8.5, -0.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    
    
    if errore:
        ax.set_title("ERRORE DI CONFIGURAZIONE!", pad=20, color="red", weight="bold")
        i_err, j_err = errore
        # Disegna il quadrato giallo: j è l'asse X, i è l'asse Y
        ax.add_patch(plt.Rectangle((j_err - 0.5, i_err - 0.5), 1, 1, facecolor='yellow', alpha=0.5))
    else:
        if x==1:
          ax.set_title("Stato Iniziale con Domini Possibili", pad=20)
        else:
          ax.set_title("Stato Iniziale", pad=20)    

    for k in range(10):
        lw = 2.5 if k % 3 == 0 else 0.8 # linee piu grosse ogni 3 righe/colonne per evidenziare i quadranti
        ax.plot([-0.5, 8.5], [k-0.5, k-0.5], color="black", linewidth=lw) # Disegna le linee orizzontali
        ax.plot([k-0.5, k-0.5], [-0.5, 8.5], color="black", linewidth=lw) # Disegna le linee verticali

    for i in range(9):
        for j in range(9):
            if A[i, j] != 0: 
                ax.text(j, i, str(A[i, j]), ha="center", va="center", fontsize=16) 
    
    # creazione matrice B con i possibili valori e disegno numerini grigi
    if x==1 and not errore:
        B = np.empty((9,9), dtype=object) 
        for i in range(9):
            for j in range(9):
                if A[i, j] == 0:
                    elementi_riga, elementi_colonna, elementi_quadrante = elementi(A, i, j)
                    B[i, j] = set(range(1, 10)) - elementi_riga - elementi_colonna - elementi_quadrante #
                
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
    
    
def disegna_sudoku_finale(A, A_originale, flag_ordine=0, percorso=None, stats=None):
    """Visualizza il Sudoku risolto, distinguendo i numeri iniziali da quelli calcolati."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(8.5, -0.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Sudoku Risolto!", pad=20, color="green", weight="bold")

    for k in range(10):
        lw = 2.5 if k % 3 == 0 else 0.8
        ax.plot([-0.5, 8.5], [k-0.5, k-0.5], color="black", linewidth=lw)
        ax.plot([k-0.5, k-0.5], [-0.5, 8.5], color="black", linewidth=lw)

    for i in range(9):
        for j in range(9):
            if A[i, j] != 0:
                # Controlliamo la matrice originale per decidere il colore
                if A_originale[i, j] != 0:
                    colore = "black"
                    peso = "bold"  # Grassetto per i numeri di partenza
                else:
                    colore = "blue"
                    peso = "normal" # Normale per i numeri trovati
                    
                ax.text(j, i, str(A[i, j]), ha="center", va="center", 
                        fontsize=16, color=colore, weight=peso)
                
    # Disegna l'ordine di completamento se richiesto         
    if flag_ordine == 1 and percorso:
        for step, (i, j) in enumerate(percorso, start=1): #enumerate serve per numerare i passi a partire da 1
            # j-0.35 e i-0.35 posizionano il testo in alto a sinistra nella cella
            ax.text(j - 0.30, i - 0.30, str(step), ha="center", va="center", 
                    fontsize=7, color="red", weight="bold")
            
    # ==========================
    # BOX STATISTICHE 
    # ==========================
    if stats is not None:
        testo = (
            "STATISTICHE\n"
            f"Nodi totali espansi:  {stats.get('nodi_espansi', 0)}\n"
            f"Numero di backtrack:  {stats.get('numero_backtrack', 0)}\n"
            f"Profondità soluzione: {stats.get('profondita_soluzione', 0)}\n"
        )

        fig.text(
            0.5, 0.1, testo,
            ha="center", va="center",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.6", alpha=0.2,facecolor="lightgray", edgecolor="black")
        )
        plt.subplots_adjust(bottom=0.20)
            
                        
    plt.show()