# Semana 3 - Algoritmos de Búsqueda

En esta semana se implementan algoritmos de búsqueda no informados utilizando como base el mapa de Rumania. Se incluyen una búsqueda básica, búsqueda en amplitud (BFS) y búsqueda en profundidad (DFS).

---

## Búsqueda Básica (`busqueda.py`)

### Descripción

Este algoritmo implementa una búsqueda recursiva que encuentra **todas las posibles rutas** entre dos ciudades sin repetir nodos visitados.

Se basa en un grafo representado como un diccionario de rutas y utiliza recursividad para explorar todos los caminos posibles.

---

### Instrucciones de Instalación

* Tener instalado Python 3
* No se requieren librerías externas

---

### Instrucciones de Ejecución

1. Abrir el archivo `busqueda.py`
2. Definir la ciudad de inicio y destino dentro del código
3. Ejecutar el archivo:

```
python busqueda.py
```

4. El programa devolverá todas las rutas posibles entre las ciudades

---

## Breadth-First Search - BFS (`breadth_first_search.py`)

### Descripción

Este algoritmo implementa la búsqueda en amplitud (BFS), explorando el grafo por niveles. Garantiza encontrar el camino más corto en grafos no ponderados.

Incluye una visualización interactiva con Pygame donde se muestra:

* Nodos visitados
* Frontera
* Nodo actual
* Camino encontrado

---

### Instrucciones de Instalación

1. Tener instalado Python 3
2. Instalar Pygame:

```
pip install pygame
```

---

### Instrucciones de Ejecución

1. Ejecutar el archivo:

```
python breadth_first_search.py
```

2. Se abrirá una ventana gráfica
3. Presionar el botón **"Iniciar"**
4. Observar la ejecución paso a paso del algoritmo

---

## Depth-First Search - DFS (`depth_first_search.py`)

### Descripción

Este algoritmo implementa la búsqueda en profundidad (DFS), explorando primero los caminos más profundos antes de retroceder (backtracking).

Incluye una visualización con Pygame mostrando:

* Nodos visitados
* Pila de ejecución
* Nodo actual
* Camino encontrado

---

### Instrucciones de Instalación

1. Tener instalado Python 3
2. Instalar Pygame:

```
pip install pygame
```

---

### Instrucciones de Ejecución

1. Ejecutar el archivo:

```
python depth_first_search.py
```

2. Se abrirá una ventana gráfica
3. Presionar el botón **"Iniciar"**
4. Observar la exploración en profundidad
