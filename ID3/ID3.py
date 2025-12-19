import math
import pygame
import sys

# ============================
# Funciones para ID3
# ============================

def calcular_infor(p, n):
    """Calcula -p log2(p) - n log2(n), sustituyendo log(0) por 0"""
    term1 = -p * math.log2(p) if p > 0 else 0
    term2 = -n * math.log2(n) if n > 0 else 0
    return term1 + term2

def calcular_entropia(datos):
    total = len(datos)
    pos = 0
    neg = 0
    for ejemplo in datos:
        decision = ejemplo["Jugar"].strip().lower()
        if decision == "positivo":
            pos += 1
        else:
            neg += 1
    p = pos / total
    n = neg / total
    return calcular_infor(p, n)

def calcular_ganancia_informacion(atributo, ejemplos):
    entropia_total = calcular_entropia(ejemplos)
    valores = set(ej[atributo].strip() for ej in ejemplos)
    sub_entropia = 0
    for valor in valores:
        subset = [ej for ej in ejemplos if ej[atributo].strip() == valor]
        sub_entropia += (len(subset) / len(ejemplos)) * calcular_entropia(subset)
    return entropia_total - sub_entropia

def id3(ejemplos, atributos, nivel=0):
    decisions = [ej["Jugar"].strip() for ej in ejemplos]
    # Si todos los ejemplos tienen la misma etiqueta, retorna esa etiqueta.
    if len(set(decisions)) == 1:
        return decisions[0]
    # Si ya no quedan atributos para dividir, retorna la etiqueta mayoritaria.
    if not atributos:
        return max(set(decisions), key=decisions.count)
    # Seleccionar el mejor atributo según la ganancia de información.
    mejor_atributo = max(atributos, key=lambda attr: calcular_ganancia_informacion(attr, ejemplos))
    tree = {mejor_atributo: {}}
    valores = set(ej[mejor_atributo].strip() for ej in ejemplos)
    for valor in valores:
        subset = [ej for ej in ejemplos if ej[mejor_atributo].strip() == valor]
        nuevos_atributos = [attr for attr in atributos if attr != mejor_atributo]
        subtree = id3(subset, nuevos_atributos, nivel + 1)
        tree[mejor_atributo][valor] = subtree
    return tree

def leer_datos():
    with open('AtributosJuego.txt', 'r') as f:
        line = f.readline().strip()
        atributos = [attr.strip() for attr in line.split(',')]
    ejemplos = []
    with open('Juego.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == len(atributos):
                ejemplo = {}
                for i, attr in enumerate(atributos):
                    ejemplo[attr] = parts[i].strip()
                ejemplos.append(ejemplo)
            else:
                print("Línea mal formateada ignorada:", line)
    return atributos, ejemplos

# ============================
# Visualización con Pygame
# ============================

def compute_layout_with_labels(tree, depth=0, positions=None, edges=None, labels=None, x_counter=None):
    if positions is None:
        positions = {}
    if edges is None:
        edges = []
    if labels is None:
        labels = {}
    if x_counter is None:
        x_counter = [0]
    # Si el nodo es una hoja (no es diccionario), asignamos posición basada en el contador.
    if not isinstance(tree, dict):
        node_id = f"leaf_{x_counter[0]}"
        positions[node_id] = (x_counter[0], depth)
        labels[node_id] = str(tree)
        x_counter[0] += 1
        return positions[node_id], node_id, labels, edges
    else:
        attribute = list(tree.keys())[0]
        node_id = f"node_{attribute}_{depth}_{x_counter[0]}"
        child_positions = []
        for branch_label, subtree in tree[attribute].items():
            child_pos, child_id, labels, edges = compute_layout_with_labels(
                subtree, depth + 1, positions, edges, labels, x_counter)
            edges.append((node_id, child_id, branch_label))
            child_positions.append(child_pos)
        avg_x = sum(pos[0] for pos in child_positions) / len(child_positions) if child_positions else x_counter[0]
        positions[node_id] = (avg_x, depth)
        labels[node_id] = attribute
        return positions[node_id], node_id, labels, edges

def draw_gradient_background(screen, width, height, start_color, end_color):
    """Dibuja un degradado vertical en el fondo."""
    for y in range(height):
        ratio = y / height
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

def visualize_tree_pygame(tree):
    pygame.init()
    width, height = 1200, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Árbol de Decisión")
    clock = pygame.time.Clock()

    # Calcular layout del árbol.
    positions = {}
    edges = []
    labels = {}
    x_counter = [0]
    _, root_id, labels, edges = compute_layout_with_labels(tree, positions=positions, edges=edges, labels=labels, x_counter=x_counter)

    max_depth = max(y for (_, y) in positions.values())
    max_x = max(x for (x, y) in positions.values())
    margin = 70
    x_spacing = (width - 2 * margin) / (max_x + 1) if max_x > 0 else 100
    y_spacing = (height - 2 * margin) / (max_depth + 1) if max_depth > 0 else 100

    def to_screen(pos):
        x, y = pos
        return int(margin + x * x_spacing), int(margin + y * y_spacing)

    font = pygame.font.SysFont("Arial", 16, bold=True)
    title_font = pygame.font.SysFont("Arial", 28, bold=True)

    bg_start = (240, 240, 255)
    bg_end = (200, 220, 255)
    internal_color = (30, 144, 255)  # Azul Dodger
    leaf_color = (50, 205, 50)       # Verde Lime
    line_color = (80, 80, 80)
    hover_color = (255, 215, 0)      # Dorado para resaltar

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fondo degradado.
        draw_gradient_background(screen, width, height, bg_start, bg_end)

        # Dibujar título.
        title_text = title_font.render("Árbol de Decisión", True, (10, 10, 10))
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 10))

        # Dibujar conexiones (edges).
        for parent_id, child_id, branch_label in edges:
            parent_pos = to_screen(positions[parent_id])
            child_pos = to_screen(positions[child_id])
            pygame.draw.aaline(screen, line_color, parent_pos, child_pos, 2)
            mid_x = (parent_pos[0] + child_pos[0]) // 2
            mid_y = (parent_pos[1] + child_pos[1]) // 2
            edge_text = font.render(str(branch_label), True, (200, 0, 0))
            screen.blit(edge_text, (mid_x, mid_y))

        # Dibujar nodos.
        for node_id, pos in positions.items():
            screen_pos = to_screen(pos)
            # Resaltar si el mouse está cerca.
            dist = math.hypot(screen_pos[0] - mouse_pos[0], screen_pos[1] - mouse_pos[1])
            highlight = dist < 25
            if node_id.startswith("leaf"):
                fill_color = leaf_color
            else:
                fill_color = internal_color

            # Dibujar sombra con alfa.
            shadow_surface = pygame.Surface((44, 44), pygame.SRCALPHA)
            pygame.draw.circle(shadow_surface, (0, 0, 0, 100), (22, 22), 22)
            screen.blit(shadow_surface, (screen_pos[0] - 22 + 3, screen_pos[1] - 22 + 3))
            # Dibujar el nodo.
            pygame.draw.circle(screen, fill_color, screen_pos, 20)
            border_color = hover_color if highlight else (0, 0, 0)
            pygame.draw.circle(screen, border_color, screen_pos, 20, 3)
            # Dibujar etiqueta con sombra.
            label_text = font.render(labels[node_id], True, (255, 255, 255))
            shadow_text = font.render(labels[node_id], True, (0, 0, 0))
            text_rect = label_text.get_rect(center=screen_pos)
            screen.blit(shadow_text, (text_rect.x+1, text_rect.y+1))
            screen.blit(label_text, text_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

# ============================
# Código Principal
# ============================

if __name__ == '__main__':
    atributos, ejemplos = leer_datos()
    # Excluir el atributo de clase "Jugar" para construir el árbol.
    atributos_sin_clase = [attr for attr in atributos if attr != "Jugar"]
    tree = id3(ejemplos, atributos_sin_clase, nivel=0)  # Árbol completo
    print("Árbol de decisión:")
    print(tree)
    visualize_tree_pygame(tree)
