class Cell:
    def __init__(self, pos, g, h):
        self.pos = pos
        self.g = g
        self.h = h
        self.f = g + h


def weightForCurrentNode(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_search(puntoInicio, puntoFinal):

    cantFilas = len(matriz) - 1
    cantColumn = len(matriz[0]) - 1

    visited = [] 
    frontier = [] 

    # empezamos con el nodo inicial
    inicio = Cell(puntoInicio, 0, weightForCurrentNode(puntoInicio, puntoFinal))
    frontier += [inicio]

    while(True):

        if frontier == []:
            return "No hay solucion"
        menor = frontier[0]
        for nodo in frontier:
            if nodo.f < menor.f:
                menor = nodo

        puntoActual = menor.pos
        g_actual = menor.g

        frontier.remove(menor)
        visited += [puntoActual]

        if(puntoActual == puntoFinal):
            return g_actual

        distancias = []  # ahora guardará objetos Cell

        # ARRIBA
        if(puntoActual[0]-1 >= 0):
            nueva = (puntoActual[0]-1, puntoActual[1])
            if(nueva not in visited and matriz[nueva[0]][nueva[1]] == 1):
                g = g_actual + 1
                h = weightForCurrentNode(nueva, puntoFinal)
                distancias += [Cell(nueva, g, h)]

        # ABAJO
        if(puntoActual[0]+1 <= cantFilas):
            nueva = (puntoActual[0]+1, puntoActual[1])
            if(nueva not in visited and matriz[nueva[0]][nueva[1]] == 1):
                g = g_actual + 1
                h = weightForCurrentNode(nueva, puntoFinal)
                distancias += [Cell(nueva, g, h)]

        # DERECHA
        if(puntoActual[1]+1 <= cantColumn):
            nueva = (puntoActual[0], puntoActual[1]+1)
            if(nueva not in visited and matriz[nueva[0]][nueva[1]] == 1):
                g = g_actual + 1
                h = weightForCurrentNode(nueva, puntoFinal)
                distancias += [Cell(nueva, g, h)]

        # IZQUIERDA
        if(puntoActual[1]-1 >= 0):
            nueva = (puntoActual[0], puntoActual[1]-1)
            if(nueva not in visited and matriz[nueva[0]][nueva[1]] == 1):
                g = g_actual + 1
                h = weightForCurrentNode(nueva, puntoFinal)
                distancias += [Cell(nueva, g, h)]

        # en vez de elegir uno, agregamos TODOS a frontier
        for nodo in distancias:

            existe = False
            for f in frontier:
                if f.pos == nodo.pos and f.f <= nodo.f:
                    existe = True
                    break

            if not existe:
                frontier += [nodo]