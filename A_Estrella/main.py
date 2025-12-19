import pygame
import math
import random
from queue import PriorityQueue

# Dimensiones de la cuadrícula
M, N = 30, 30  # M = filas, N = columnas
TAMANO_CELDA = 15
ANCHO_VENTANA, ALTO_VENTANA = N * TAMANO_CELDA, M * TAMANO_CELDA
ANCHO_VENTANA += 200  # Espacio para el panel lateral (botones y métricas)

# Colores
BLANCO     = (255, 255, 255)
NEGRO      = (0, 0, 0)
ROJO       = (255, 0, 0)
VERDE      = (0, 255, 0)
AMARILLO   = (255, 255, 0)
AZUL       = (0, 0, 255)
GRIS       = (200, 200, 200)
AZUL_CLARO = (0, 255, 255)
NARANJA    = (255, 165, 0)  # Para los waypoints

# Inicializa pygame
pygame.init()

# Crear la ventana de juego
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("A*")

# Variables globales para la cuadrícula y puntos
inicio = None
objetivo = None
waypoints = []  # Lista de waypoints (puntos intermedios)
obstaculos = []
# Celdas peligrosas: diccionario con clave = (fila, columna) y valor = factor de riesgo
celdas_peligrosas = {}

# Flag para el modo de agregar waypoints
modo_waypoints = False

# Calcular la diagonal y definir el límite máximo para el factor de riesgo
DIAGONAL_CUADRICULA = math.sqrt(M**2 + N**2)
FACTOR_RIESGO_MAX = 0.1 * DIAGONAL_CUADRICULA  # 10% de la diagonal

# Función para generar obstáculos aleatorios
def generar_obstaculos():
    return [(i, j) for i in range(M) for j in range(N) if random.random() < 0.2]

# Función para generar celdas peligrosas con factores variables
def generar_celdas_peligrosas():
    celdas = {}
    for i in range(M):
        for j in range(N):
            if random.random() < 0.1:  # 10% de probabilidad
                riesgo = random.uniform(0.1, FACTOR_RIESGO_MAX)
                celdas[(i, j)] = riesgo
    return celdas

# Dibujar la cuadrícula (incluye obstáculos y celdas peligrosas con su color)
def dibujar_cuadricula():
    for fila in range(M):
        for columna in range(N):
            rect = pygame.Rect(columna * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
            if (fila, columna) in obstaculos:
                pygame.draw.rect(pantalla, ROJO, rect)
            elif (fila, columna) in celdas_peligrosas:
                pygame.draw.rect(pantalla, AZUL, rect)
            else:
                pygame.draw.rect(pantalla, BLANCO, rect)
            pygame.draw.rect(pantalla, NEGRO, rect, 1)

# Dibujar botón "Reiniciar"
def dibujar_boton_reiniciar():
    rect = pygame.Rect(ANCHO_VENTANA - 180, 20, 160, 50)
    pygame.draw.rect(pantalla, AZUL_CLARO, rect)
    font = pygame.font.Font(None, 36)
    texto = font.render("Reiniciar", True, NEGRO)
    pantalla.blit(texto, (ANCHO_VENTANA - 150, 30))

# Dibujar botón "Modo Waypoints"
def dibujar_boton_waypoints():
    rect = pygame.Rect(ANCHO_VENTANA - 180, 80, 160, 50)
    color = AZUL_CLARO if modo_waypoints else GRIS
    pygame.draw.rect(pantalla, color, rect)
    font = pygame.font.Font(None, 26)
    estado = "ON" if modo_waypoints else "OFF"
    texto = font.render("Modo Waypoints: " + estado, True, NEGRO)
    pantalla.blit(texto, (ANCHO_VENTANA - 175, 95))

# Clase Nodo para A*
class Nodo:
    def __init__(self, posicion, padre=None):
        self.posicion = posicion
        self.padre = padre
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, otro):
        return self.f < otro.f

# Función heurística: distancia euclidiana + factor de riesgo si la celda es peligrosa
def distancia_heuristica(nodo1, nodo2):
    x1, y1 = nodo1
    x2, y2 = nodo2
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    if nodo1 in celdas_peligrosas:
        distancia += celdas_peligrosas[nodo1]
    return distancia

# Algoritmo A*
def algoritmo_a_estrella(inicio, objetivo):
    abierta = PriorityQueue()
    abierta.put((0, Nodo(inicio)))
    cerrada = set()
    nodos_cerrados = set(obstaculos)

    while not abierta.empty():
        _, nodo_actual = abierta.get()
        if nodo_actual.posicion == objetivo:
            camino = []
            while nodo_actual:
                camino.append(nodo_actual.posicion)
                nodo_actual = nodo_actual.padre
            return camino[::-1]
        cerrada.add(nodo_actual.posicion)
        for delta in [(0, -1), (0, 1), (-1, 0), (1, 0),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            pos_sucesor = (nodo_actual.posicion[0] + delta[0],
                            nodo_actual.posicion[1] + delta[1])
            if 0 <= pos_sucesor[0] < M and 0 <= pos_sucesor[1] < N and pos_sucesor not in nodos_cerrados:
                nodo_sucesor = Nodo(pos_sucesor, nodo_actual)
                nodo_sucesor.g = nodo_actual.g + distancia_heuristica(nodo_actual.posicion, pos_sucesor)
                nodo_sucesor.h = distancia_heuristica(pos_sucesor, objetivo)
                nodo_sucesor.f = nodo_sucesor.g + nodo_sucesor.h
                if pos_sucesor in cerrada:
                    continue
                abierta.put((nodo_sucesor.f, nodo_sucesor))
    return None

# Calcula el camino completo (desde inicio, pasando por waypoints, hasta objetivo)
def calcular_camino_completo(inicio, waypoints, objetivo):
    if inicio is None or objetivo is None:
        return None
    camino_total = []
    puntos = [inicio] + waypoints + [objetivo]
    for i in range(len(puntos) - 1):
        segmento = algoritmo_a_estrella(puntos[i], puntos[i+1])
        if segmento is None:
            return None
        # Evitar duplicar el punto de unión entre segmentos
        if i > 0:
            segmento = segmento[1:]
        camino_total.extend(segmento)
    return camino_total

# Manejar eventos (clics en la cuadrícula y en el panel lateral)
def manejar_eventos(evento):
    global inicio, objetivo, waypoints, modo_waypoints
    x, y = pygame.mouse.get_pos()

    # Si el clic se produce en el panel lateral (x >= N * TAMANO_CELDA), procesamos botones
    if x >= N * TAMANO_CELDA:
        # Botón "Reiniciar"
        if ANCHO_VENTANA - 180 <= x <= ANCHO_VENTANA - 20 and 20 <= y <= 70:
            reiniciar_juego()
        # Botón "Modo Waypoints"
        elif ANCHO_VENTANA - 180 <= x <= ANCHO_VENTANA - 20 and 80 <= y <= 130:
            modo_waypoints = not modo_waypoints
        return

    # Clic en la cuadrícula
    pos = (y // TAMANO_CELDA, x // TAMANO_CELDA)
    # Si aún no se ha definido el inicio, con clic izquierdo se asigna
    if inicio is None and evento.button == 1:
        if pos not in obstaculos:
            inicio = pos
    else:
        if modo_waypoints:
            # Mientras el modo waypoints esté activado, se agregan waypoints con clic izquierdo
            if evento.button == 1 and pos not in obstaculos and pos not in waypoints and pos != inicio:
                waypoints.append(pos)
        else:
            # Con modo waypoints desactivado, se permite asignar el nodo final (objetivo) con clic derecho
            if evento.button == 3:
                if pos not in obstaculos and pos != inicio:
                    objetivo = pos

# Reiniciar la simulación
def reiniciar_juego():
    global inicio, objetivo, waypoints, obstaculos, celdas_peligrosas, modo_waypoints
    inicio = None
    objetivo = None
    waypoints = []
    obstaculos = generar_obstaculos()
    celdas_peligrosas = generar_celdas_peligrosas()
    modo_waypoints = False

# Bucle principal
def main():
    global inicio, objetivo, waypoints, obstaculos, celdas_peligrosas, modo_waypoints
    reiniciar_juego()
    ejecutando = True
    font_info = pygame.font.Font(None, 24)
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                manejar_eventos(evento)

        pantalla.fill(NEGRO)
        # Primero se dibuja la cuadrícula (con obstáculos y celdas peligrosas)
        dibujar_cuadricula()

        # Calcular y dibujar el camino como línea (para que no tape los colores de celdas y nodos)
        camino = calcular_camino_completo(inicio, waypoints, objetivo)
        if camino and len(camino) >= 2:
            for i in range(len(camino) - 1):
                inicio_linea = (camino[i][1] * TAMANO_CELDA + TAMANO_CELDA // 2,
                                camino[i][0] * TAMANO_CELDA + TAMANO_CELDA // 2)
                fin_linea = (camino[i+1][1] * TAMANO_CELDA + TAMANO_CELDA // 2,
                             camino[i+1][0] * TAMANO_CELDA + TAMANO_CELDA // 2)
                pygame.draw.line(pantalla, VERDE, inicio_linea, fin_linea, 3)

        # Dibujar botones del panel lateral
        dibujar_boton_reiniciar()
        dibujar_boton_waypoints()

        # Dibujar waypoints (en naranja)
        for wp in waypoints:
            rect_wp = pygame.Rect(wp[1] * TAMANO_CELDA, wp[0] * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
            pygame.draw.rect(pantalla, NARANJA, rect_wp)

        # Dibujar nodo de inicio (amarillo) y nodo final (negro)
        if inicio:
            rect_inicio = pygame.Rect(inicio[1] * TAMANO_CELDA, inicio[0] * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
            pygame.draw.rect(pantalla, AMARILLO, rect_inicio)
        if objetivo:
            rect_objetivo = pygame.Rect(objetivo[1] * TAMANO_CELDA, objetivo[0] * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
            pygame.draw.rect(pantalla, NEGRO, rect_objetivo)

        # Mostrar métricas en el panel lateral
        if camino:
            total_celdas = len(camino)
            total_peligrosas = sum(1 for pos in camino if pos in celdas_peligrosas)
            total_cost = 0
            for i in range(len(camino) - 1):
                total_cost += distancia_heuristica(camino[i], camino[i+1])
            texto_total = font_info.render("Total celdas: " + str(total_celdas), True, BLANCO)
            texto_peligrosas = font_info.render("Celdas peligrosas: " + str(total_peligrosas), True, BLANCO)
            texto_costo = font_info.render("Costo total: " + str(round(total_cost, 2)), True, BLANCO)
            pantalla.blit(texto_total, (ANCHO_VENTANA - 180, 140))
            pantalla.blit(texto_peligrosas, (ANCHO_VENTANA - 180, 165))
            pantalla.blit(texto_costo, (ANCHO_VENTANA - 180, 190))
        else:
            texto_no = font_info.render("Camino no encontrado", True, BLANCO)
            pantalla.blit(texto_no, (ANCHO_VENTANA - 180, 140))

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
