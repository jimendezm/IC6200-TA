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

def actions(rutaActual):
    return rutas[rutaActual]

def allpaths(rutaActual, rutaFinal, visitados=[]):
    nueva_ruta=visitados+[rutaActual]
    if rutaActual==rutaFinal:
        return [nueva_ruta]

    posiblesCaminos =[]
    vecinos=list(rutas[rutaActual])
    i = 0
    while i < len(vecinos):
        ciudad_vecina = vecinos[i]
        if ciudad_vecina not in visitados: 
            # Recursividad para seguir las mismas reglas sin repetición (visitados) pero para las demás rutas
            resultados = allpaths(ciudad_vecina, rutaFinal, nueva_ruta)
            posiblesCaminos += resultados
        
        i += 1
        
    return posiblesCaminos