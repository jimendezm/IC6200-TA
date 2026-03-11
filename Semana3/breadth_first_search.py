rutas = {
    "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
    "Bucharest": {"Fagaras": 211, "Pitesti": 101, "Giurgiu": 90, "Urziceni": 85},
    "Craiova": {"Drobeta": 120, "Rimnicu Vilcea": 146, "Pitesti": 138},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Eforie": {"Hirsova": 86},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "Giurgiu": {"Bucharest": 90},
    "Hirsova": {"Urziceni": 98, "Eforie": 86},
    "Iasi": {"Neamt": 87, "Vaslui": 92},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Neamt": {"Iasi": 87},
    "Oradea": {"Zerind": 71, "Sibiu": 151},
    "Pitesti": {"Rimnicu Vilcea": 97, "Craiova": 138, "Bucharest": 101},
    "Rimnicu Vilcea": {"Sibiu": 80, "Pitesti": 97, "Craiova": 146},
    "Sibiu": {"Arad": 140, "Oradea": 151, "Fagaras": 99, "Rimnicu Vilcea": 80},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Urziceni": {"Bucharest": 85, "Vaslui": 142, "Hirsova": 98},
    "Vaslui": {"Iasi": 92, "Urziceni": 142},
    "Zerind": {"Arad": 75, "Oradea": 71}
}


def breadth_first_search(nodoInicial, nodoFinal): # Busca todos los caminos y los recorre al mismo momento
    frontier=[nodoInicial]
    visited=[nodoInicial]
    recorridos=[]

    while(True):
        if (frontier[0]==nodoFinal): # si ya encontro a el nodoFinal
            return find_path(nodoInicial, nodoFinal, recorridos) #Este solo retorna la solucion 
        if (frontier==[]):
            return "No hay solucion"
        
        hijos=list(rutas[frontier[0]].keys())
        for hijo in hijos:
            if hijo not in visited:
                visited+=[hijo]
                frontier+=[hijo]
                recorridos+=[(frontier[0],hijo)] # Aqui registramos los caminos en tuplas (padre,hijo) para imprimir la solucion al final
        
        frontier=frontier[1:]

def find_path(nodoInicial, nodoFinal, recorridos):
    path =[nodoFinal]
    while nodoFinal!=nodoInicial:
        for padreHijo in recorridos:
            if padreHijo[1]== nodoFinal:
                nodoFinal =padreHijo[0]
                path =[nodoFinal]+path
    
    return path
    