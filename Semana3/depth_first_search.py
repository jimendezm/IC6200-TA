import pygame
import sys

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

posiciones = {
    "Arad": (100, 100), "Zerind": (80, 50), "Oradea": (150, 50),
    "Sibiu": (200, 120), "Timisoara": (80, 200), "Lugoj": (150, 250),
    "Mehadia": (150, 300), "Drobeta": (150, 350), "Craiova": (250, 350),
    "Rimnicu Vilcea": (250, 200), "Fagaras": (300, 120),
    "Pitesti": (300, 250), "Bucharest": (400, 300),
    "Giurgiu": (400, 380), "Urziceni": (480, 250),
    "Hirsova": (550, 200), "Eforie": (600, 250),
    "Vaslui": (500, 150), "Iasi": (480, 80), "Neamt": (550, 50)
}

def find_path(nodoInicial, nodoFinal, recorridos):
    path =[nodoFinal]
    while nodoFinal!=nodoInicial:
        for padreHijo in recorridos:
            if padreHijo[1]== nodoFinal:
                nodoFinal =padreHijo[0]
                path =[nodoFinal]+path
    return path

def depth_first_search_step(nodoInicial, nodoFinal): 

    pila=[nodoInicial]
    visited=[]
    recorridos=[]
    nodoActual=nodoInicial

    while(True):
        if (pila==[]):
            yield visited, pila, None, []
            return
        
        nodoActual=pila[-1]

        yield visited, pila, nodoActual, []

        if(nodoActual==nodoFinal):
            path = find_path(nodoInicial,nodoFinal,recorridos)
            yield visited, pila, nodoActual, path
            return
        
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
                    recorridos+=[(nodoActual,hijo)]
                    break
        else:
            pila=pila[:-1]

pygame.init()

WIDTH, HEIGHT = 700, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DFS Rumania")

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
YELLOW = (255,255,0)
GRAY = (200,200,200)

font = pygame.font.SysFont(None, 22)

button_rect = pygame.Rect(250, 730, 200, 50)

def draw_graph(visited, pila, current, path):
    screen.fill(WHITE)

    for ciudad in rutas:
        for vecino in rutas[ciudad]:
            pygame.draw.line(screen, GRAY, posiciones[ciudad], posiciones[vecino], 2)

    for ciudad, pos in posiciones.items():
        color = WHITE

        if ciudad in visited:
            color = GREEN
        if ciudad in pila:
            color = BLUE
        if ciudad in path:
            color = YELLOW

        pygame.draw.circle(screen, color, pos, 15)
        pygame.draw.circle(screen, BLACK, pos, 15, 2)

        texto = font.render(ciudad, True, BLACK)
        screen.blit(texto, (pos[0]-30, pos[1]-30))

    if current:
        pygame.draw.circle(screen, RED, posiciones[current], 10)

    pygame.draw.rect(screen, GRAY, button_rect)
    text = font.render("Iniciar", True, BLACK)
    screen.blit(text, (button_rect.x+60, button_rect.y+15))

    legend_y = 600
    legends = [
        ("Visitado", GREEN),
        ("Pila", BLUE),
        ("Actual", RED),
        ("Camino", YELLOW)
    ]

    for i, (txt, color) in enumerate(legends):
        pygame.draw.rect(screen, color, (20, legend_y + i*25, 20, 20))
        label = font.render(txt, True, BLACK)
        screen.blit(label, (50, legend_y + i*25))

def main():
    clock = pygame.time.Clock()

    running = False
    generator = None

    visited, pila, current, path = [], [], None, []

    start = "Arad"
    end = "Bucharest"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    generator = depth_first_search_step(start, end)
                    running = True
                    visited, pila, current, path = [], [], None, []

        if running and generator:
            try:
                visited, pila, current, path = next(generator)
                pygame.time.delay(300)
            except StopIteration:
                running = False

        draw_graph(visited, pila, current, path)
        pygame.display.flip()
        clock.tick(60)

main()
