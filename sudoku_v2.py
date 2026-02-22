import numpy as np
from numpy import random
import matplotlib.pyplot as plt

#creazione matrice 9x9 
A=np.zeros((9, 9), dtype=int)
num_elementi =70
A[1,0]=5
A[5:,0]=[3,1,7,9]
A[0:2,1]=[6,8]
A[3,1]=9
A[5:7,1]=[5,3]
A[8,1]=4
A[1:3,2]=[1,3]
A[6:8,2]=[5,8]
A[0,3]=3
A[2:5,3]=[5,8,7]
A[7,3]=6
A[4,4]=4
A[7,4]=1
A[0:2,5]=[8,9]
A[3:6,5]=[2,5,6]
A[7:,5]=[3,7]
A[0:2,6]=[1,6]
A[4:6,6]=[9,8]
A[7:,6]=[4,3]
A[4,7]=3
A[4:6,8]=[6,4]
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
            [elementi_riga, elementi_colonna, elementi_quadrante] = elementi(i, j)
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
dim_min=10
#fig.canvas.draw_idle()


#funzione che restituisce gli elementi presenti nella riga, colonna e quadrante di una cella (i, j)
def elementi(i, j):
    global B
    global A
    elementi_riga = set(A[i, :]) - {0}
    elementi_colonna = set(A[:, j]) - {0}
    elementi_quadrante = set(A[i//3*3:(i//3+1)*3, j//3*3:(j//3+1)*3].flatten()) - {0} 
    return elementi_riga, elementi_colonna, elementi_quadrante

#minimum remaing value (MRV) heuristic
def mrv():
    global B
    global A
    for i in range(9):
        for j in range(9):
            if A[i, j] == 0:
                if len(B[i, j]) < dim_min:
                    dim_min = len(B[i, j])
                    cella = (i, j)
                    return cella
                

#degree heuristic           
def degree():
    global B
    global A
    dim_min=20
    for i in range(9):
        for j in range(9):
            if A[i, j] == 0:
                [elementi_riga, elementi_colonna, elementi_quadrante] = elementi(i, j)
                grado = len(elementi_riga) + len(elementi_colonna) + len(elementi_quadrante)
                if grado < dim_min:
                    dim_min = grado
                    cella = (i, j)
                    return cella
                
#least constraining value (LCV) heuristic
def lcv(i, j):
    global B
    global A
    valori = []
    for num in B[i, j]:
        count = 0
        for k in range(9):
            if A[i, k] == 0 and num in B[i, k]:
                count += 1
            if A[k, j] == 0 and num in B[k, j]:
                count += 1
        for m in range(i//3*3, (i//3+1)*3):
            for n in range(j//3*3, (j//3+1)*3):
                if A[m, n] == 0 and num in B[m, n]:
                    count += 1
        valori.append((num, count))
    valori.sort(key=lambda x: x[1])
    return [val[0] for val in valori]
