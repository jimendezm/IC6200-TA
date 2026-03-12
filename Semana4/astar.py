
matriz=[ # Los 0 son celdas bloqueadas y 1 las que si tienen camino
    [0,0,0,0,0,1],
    [0,1,1,0,0,1],
    [0,0,1,0,0,1],
    [0,1,1,1,1,1],
    [0,1,0,1,0,0],
    [0,1,0,1,0,0],
]

class Cell:
    def __init__(self, pos, distancia):
        


def a_search(puntoInicio, puntoFinal): #formato (fila,columna)
    contador=0 # Distancia que recorrerá

    cantFilas=len(matriz)-1 #Esto para saber el limite
    cantColumn=len(matriz[0])-1

    visited=[] #Los puntos que ya fueron visitados

    frontier=[] #Estos van a ser los puntos donde tienen más de un camino, para devolverse

    puntoActual=puntoInicio
    while(True):
        visited+=[puntoActual]
        if(puntoActual==puntoFinal):
            return contador
        distancias=[] # Se guardaria en tuplas de  (fila,columna, distancia) *la distancia del destino
        #Aqui vamos a revisar los caminos disponibles del punto actual
        if(puntoActual[0]-1 >= 0): # Movimiento arriba
            if((puntoActual[0]-1,puntoActual[1]) not in visited):
                if(matriz[puntoActual[0]-1][puntoActual[1]]==1 ):
                    distancia=abs(puntoActual[0]-1 - puntoFinal[0]) + abs(puntoActual[1]-puntoFinal[1])
                    distancias+=[(puntoActual[0]-1,puntoActual[1],distancia)]
        if(puntoActual[0]+1<=cantFilas): #Movimiento abajo
            if((puntoActual[0]+1,puntoActual[1]) not in visited):
                if(matriz[puntoActual[0]+1][puntoActual[1]]==1 ):
                    distancia=abs(puntoActual[0]+1 - puntoFinal[0]) + abs(puntoActual[1]-puntoFinal[1])
                    distancias+=[(puntoActual[0]+1,puntoActual[1],distancia)]
        if(puntoActual[1]+1<=cantColumn): #Movimiento derecha
            if((puntoActual[0],puntoActual[1]+1) not in visited):
                if(matriz[puntoActual[0]][puntoActual[1]+1]==1 ):
                    distancia=abs(puntoActual[0] - puntoFinal[0]) + abs(puntoActual[1]+1-puntoFinal[1])
                    distancias+=[(puntoActual[0],puntoActual[1]+1,distancia)]
        if(puntoActual[1]-1>=0): #Movimiento izquierda
            if((puntoActual[0],puntoActual[1]-1) not in visited):
                if(matriz[puntoActual[0]][puntoActual[1]-1]==1 ):
                    distancia=abs(puntoActual[0] - puntoFinal[0]) + abs(puntoActual[1]-1-puntoFinal[1])
                    distancias+=[(puntoActual[0],puntoActual[1]-1,distancia)]
        
        if (len(distancias)>=2):
            frontier+=[(puntoActual[0],puntoActual[1],len(distancias)-1)] #Guarda coordenadas y cantidad de caminos que le quedan

        if(distancias!=[]):
            #Se toma la decision
            menor = distancias[0]

            for punto in distancias:
                if punto[2]<menor[2]:
                    menor=punto

            puntoActual=(menor[0],menor[1])
            contador+=1
        else:
            if(frontier!=[]):
                # Se regresa al punto anterior donde tiene otros caminos y busca el mejor
                puntoActual=(frontier[-1][0],frontier[-1][1])
                nuevo_punto=(frontier[-1][0],frontier[-1][1],frontier[-1][2]-1) # restaura la cantidad de caminos que tiene
                frontier=frontier[:-1]
                frontier+=[nuevo_punto]
                if(frontier[-1][2]==0):
                    frontier=frontier[:-1]
            else:
                return "No hay solucion"




        