import pygame
import sys

matriz = [
    [1,1,1,1,1,1,0,1,1,1],
    [1,0,0,0,1,1,0,1,0,1],
    [1,1,1,0,1,1,1,1,0,1],
    [0,0,1,0,0,0,0,1,0,1],
    [1,1,1,1,1,1,0,1,1,1],
    [1,0,0,0,0,1,0,0,0,1],
    [1,1,1,1,0,1,1,1,0,1],
    [1,0,0,1,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,0,1],
    [0,0,0,0,0,0,0,1,1,1]
]

class Cell:
    def __init__(self, pos, g, h, parent=None):
        self.pos = pos
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

def weightForCurrentNode(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.pos)
        node = node.parent
    return path[::-1]

def a_search_step(puntoInicio, puntoFinal):

    cantFilas = len(matriz) - 1
    cantColumn = len(matriz[0]) - 1

    visited = [] 
    frontier = [] 

    inicio = Cell(puntoInicio, 0, weightForCurrentNode(puntoInicio, puntoFinal))
    frontier += [inicio]

    while(True):

        if frontier == []:
            yield visited, frontier, None, []
            return

        menor = frontier[0]
        for nodo in frontier:
            if nodo.f < menor.f:
                menor = nodo

        puntoActual = menor.pos
        g_actual = menor.g

        frontier.remove(menor)
        visited += [puntoActual]

        yield visited, frontier, menor, []

        if(puntoActual == puntoFinal):
            path = reconstruct_path(menor)
            yield visited, frontier, menor, path
            return

        distancias = []

        if(puntoActual[0]-1 >= 0):
            nueva = (puntoActual[0]-1, puntoActual[1])
            if(nueva not in visited and matriz[nueva[0]][nueva[1]] == 1):
                distancias += [Cell(nueva, g_actual+1, weightForCurrentNode(nueva, puntoFinal), menor)]

        if(puntoActual[0]+1 <= cantFilas):
            nueva = (puntoActual[0]+1, puntoActual[1])
            if(nueva not in visited and matriz[nueva[0]][nueva[1]] == 1):
                distancias += [Cell(nueva, g_actual+1, weightForCurrentNode(nueva, puntoFinal), menor)]

        if(puntoActual[1]+1 <= cantColumn):
            nueva = (puntoActual[0], puntoActual[1]+1)
            if(nueva not in visited and matriz[nueva[0]][nueva[1]] == 1):
                distancias += [Cell(nueva, g_actual+1, weightForCurrentNode(nueva, puntoFinal), menor)]

        if(puntoActual[1]-1 >= 0):
            nueva = (puntoActual[0], puntoActual[1]-1)
            if(nueva not in visited and matriz[nueva[0]][nueva[1]] == 1):
                distancias += [Cell(nueva, g_actual+1, weightForCurrentNode(nueva, puntoFinal), menor)]

        for nodo in distancias:

            existe = False
            for f in frontier:
                if f.pos == nodo.pos and f.f <= nodo.f:
                    existe = True
                    break

            if not existe:
                frontier += [nodo]

pygame.init()

WIDTH, HEIGHT = 600, 750
ROWS, COLS = len(matriz), len(matriz[0])
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Visual")

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
GRAY = (200,200,200)
YELLOW = (255,255,0)

font = pygame.font.SysFont(None, 26)

button_rect = pygame.Rect(200, 680, 200, 50)

def draw_grid(visited, frontier, current, path):
    screen.fill(WHITE)

    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if matriz[i][j] == 0:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)

            if (i,j) in visited:
                pygame.draw.rect(screen, GREEN, rect)

            for f in frontier:
                if f.pos == (i,j):
                    pygame.draw.rect(screen, BLUE, rect)

            if (i,j) in path:
                pygame.draw.rect(screen, YELLOW, rect)

            pygame.draw.rect(screen, GRAY, rect, 1)

    if current:
        x, y = current.pos[1]*CELL_SIZE + CELL_SIZE//2, current.pos[0]*CELL_SIZE + CELL_SIZE//2
        pygame.draw.circle(screen, RED, (x,y), CELL_SIZE//3)

    pygame.draw.rect(screen, GRAY, button_rect)
    text = font.render("Iniciar", True, BLACK)
    screen.blit(text, (button_rect.x+60, button_rect.y+15))

    legend_y = 620
    legends = [
        ("Visitado", GREEN),
        ("Frontera", BLUE),
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

    visited, frontier, current, path = [], [], None, []

    start = (0,0)
    end = (9,9)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    generator = a_search_step(start, end)
                    running = True
                    visited, frontier, current, path = [], [], None, []

        if running and generator:
            try:
                visited, frontier, current, path = next(generator)
                pygame.time.delay(190)
            except StopIteration:
                running = False

        draw_grid(visited, frontier, current, path)
        pygame.display.flip()
        clock.tick(120)

main()