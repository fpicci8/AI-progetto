
import matplotlib.pyplot as plt
import numpy as np
from logic import elementi






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
    if x==1:
        ax.set_title("Stato Iniziale con Domini Possibili", pad=20)
    else:
        ax.set_title("Stato Iniziale", pad=20)    

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
    
    
def disegna_sudoku_finale(A, A_originale, flag_ordine=0, percorso=None):
    """Visualizza il Sudoku risolto, distinguendo i numeri iniziali da quelli calcolati."""
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
        for step, (i, j) in enumerate(percorso, start=1):
            # j-0.35 e i-0.35 posizionano il testo in alto a sinistra nella cella
            ax.text(j - 0.35, i - 0.35, str(step), ha="center", va="center", 
                    fontsize=8, color="red", weight="bold")
            
                        
    plt.show()