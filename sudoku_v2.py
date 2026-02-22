import numpy as np
from numpy import random
import matplotlib.pyplot as plt

#creazione matrice 9x9 
A=np.zeros((9, 9), dtype=int)
num_elementi =70
A[:,0]=[1,3,5,8,6,2,4,9,7]
A[1:7,1]=[9,7,5,1,3,6]
A[8,1]=8
A[0:3,2]=[8,6,2,7]
A[5:8,2]=[4,1,5,3]
A[:,3]=[2,4,3,6,8,9,5,7,1]
A[0,4]=7
A[2:5,4]=[9,2,3,5]
A[7,4]=6
A[0:2,5]=[5,8,6]
A[4:8,5]=[7,1,2,3,9]
A[1:8,6]=[7,1,3,5,8,9,4,2]
A[0:6,7]=[9,5,4,1,2,7,3]
A[8,7]=6
A[0:4,8]=[3,2,8,9,4]
A[6:8,8]=[7,1,5]
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
plt.show()
#fig.canvas.draw_idle()