import numpy as np
from numpy import random
import matplotlib.pyplot as plt

#creazione matrice 9x9 con 70 elementi casuali tra 1 e 10, il resto 0
A=np.zeros((9, 9), dtype=int)
num_elementi = 20
posizioni = random.choice(9*9, num_elementi, replace=False)
righe, colonne = np.unravel_index(posizioni, (9, 9))
valori = random.randint(1,10, size=num_elementi)
A[righe, colonne] = valori



#rimozione di eventuali duplicati nelle righe, colonne e quadranti
for i in range(9):
    for j in range(9):
        if A[i, j] != 0:
            elementi_riga = set(A[i, :]) - {0}
            elementi_colonna = set(A[:, j]) - {0}
            elementi_quadrante = set(A[i//3*3:(i//3+1)*3, j//3*3:(j//3+1)*3].flatten()) - {0}
            if elementi_riga:
                esclusi =elementi_riga
            if elementi_colonna:
                esclusi = esclusi.union(elementi_colonna)
            if elementi_quadrante:
                esclusi = esclusi.union(elementi_quadrante)
            esclusi=set(esclusi)
            if A[i, j] in esclusi:
                possibili = list(set(range(1,10)) - esclusi)
                if possibili:
                    A[i, j] = random.choice(possibili)
                else:
                    A[i, j] = 0

#CREAZIONE DELLA FIGURA
fig, ax = plt.subplots()

# area della griglia
ax.set_xlim(-0.5, 8.5)
ax.set_ylim(8.5, -0.5)
ax.set_aspect("equal")

# rimuove numeri sugli assi
ax.set_xticks([])
ax.set_yticks([])

# disegno linee della griglia
for k in range(10):
    # linee spesse ogni 3 (quadrati sudoku)
    lw = 2.5 if k % 3 == 0 else 0.8

    ax.plot([-0.5, 8.5], [k-0.5, k-0.5], color="black", linewidth=lw)
    ax.plot([k-0.5, k-0.5], [-0.5, 8.5], color="black", linewidth=lw)

# inserimento numeri
for i in range(9):
    for j in range(9):
        if A[i, j] != 0:
            ax.text(j, i, str(A[i, j]),
                    ha="center", va="center",
                    fontsize=16)



#creazione matrice B con i possibili valori per ogni cella vuota di A
B = np.empty((9,9), dtype=object)
for i in range(9):
    for j in range(9):
        if A[i, j] == 0:
            elementi_riga = set(A[i, :]) - {0}
            elementi_colonna = set(A[:, j]) - {0}
            elementi_quadrante = set(A[i//3*3:(i//3+1)*3, j//3*3:(j//3+1)*3].flatten()) - {0} 
            B[i, j] = set(range(1, 10)) - elementi_riga - elementi_colonna - elementi_quadrante
            # offset dentro la cella (1..9) in una griglia 3x3
            pos = {
                    1: (-0.30, -0.30), 2: (0.00, -0.30), 3: (0.30, -0.30),
                    4: (-0.30,  0.00), 5: (0.00,  0.00), 6: (0.30,  0.00),
                    7: (-0.30,  0.30), 8: (0.00,  0.30), 9: (0.30,  0.30),
                }
            for num in B[i, j]:
                ax.text(j + pos[num][0], i + pos[num][1], str(num),
                        ha="center", va="center",
                        fontsize=9, color="gray")

        else:
            B[i, j] = A[i, j]
plt.show(block=False)
fig.canvas.draw_idle()