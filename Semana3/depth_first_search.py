def find_path(nodoInicial, nodoFinal, recorridos):
    path =[nodoFinal]
    while nodoFinal!=nodoInicial:
        for padreHijo in recorridos:
            if padreHijo[1]== nodoFinal:
                nodoFinal =padreHijo[0]
                path =[nodoFinal]+path
    
    return path
    
    
def depth_first_search(nodoInicial, nodoFinal): 
    ''' 
    Busca 1 random y luego si llega al final y si no llega al destino 
    entonces busca en el nodo hijo del anterior
    '''
    pila=[nodoInicial]
    visited=[]
    recorridos=[]
    nodoActual=nodoInicial
    while(True):
        if (pila==[]):
            return "No hay solucion"
        
        nodoActual=pila[-1]
        if(nodoActual==nodoFinal):
            return find_path(nodoInicial,nodoFinal,recorridos)
        
        if (nodoActual not in visited):
            visited+=[nodoActual]

        hijos=list(rutas[nodoActual].keys())
        hijosNoVisitados=False
        for hijo in hijos:
            if hijo not in visited:
                hijosNoVisitados=True
                break

        if (hijosNoVisitados):
            for hijo in hijos:
                if hijo not in visited:
                    pila+=[hijo]
                    recorridos+=[(nodoActual,hijo)] # Aqui registramos los caminos en tuplas (padre,hijo) para imprimir la solucion al final
                    break
        else:
            pila=pila[:-1]
        