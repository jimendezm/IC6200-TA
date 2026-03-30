# Semana 4 - Búsqueda Informada

En esta semana se implementa el algoritmo de búsqueda informada **A***, aplicado sobre una matriz que representa un entorno con obstáculos.

---

## A* Search (`astar.py`)

### Descripción

El algoritmo **A*** es una técnica de búsqueda informada que encuentra el camino más corto entre un punto inicial y un punto final.

Combina:

* **Costo real (g):** distancia recorrida desde el inicio
* **Heurística (h):** estimación de la distancia al objetivo (en este caso, distancia Manhattan)
* **Función total (f = g + h)**

El entorno está representado por una **matriz**, donde:

* `1` representa un camino válido
* `0` representa un obstáculo

El algoritmo explora los nodos más prometedores primero, logrando eficiencia en la búsqueda del camino óptimo.

Además, incluye una **visualización con Pygame**, donde se muestra:

* Nodos visitados
* Frontera (nodos por explorar)
* Nodo actual
* Camino final encontrado

---

### Instrucciones de Instalación

1. Tener instalado Python 3
2. Instalar Pygame:

```id="instastar"
pip install pygame
```

---

### Instrucciones de Ejecución

1. Ejecutar el archivo:

```id="runastar"
python astar.py
```

2. Se abrirá una ventana gráfica
3. Presionar el botón **"Iniciar"**
4. Observar cómo el algoritmo encuentra el camino desde el inicio hasta el destino
