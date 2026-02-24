
import matplotlib.pyplot as plt
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
    