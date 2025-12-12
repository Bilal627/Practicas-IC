# 🧠 AI Algorithms: Implementación de Algoritmos de IA

## 🌟 Resumen del Proyecto

Implementación técnica desde cero ("from scratch") de algoritmos fundamentales de Inteligencia Artificial y Machine Learning utilizando **Python**.

El proyecto se centra en la comprensión matemática y lógica de los algoritmos, evitando el uso de librerías de "caja negra" para la lógica principal. Incluye simulaciones gráficas para algoritmos de búsqueda y clasificación de datos.

---

## 🛠️ Tecnologías Utilizadas

| Categoría | Tecnología | Uso |
| :--- | :--- | :--- |
| **Lenguaje** | Python 3 | Lógica central y algoritmos |
| **Cálculo** | NumPy | Operaciones vectoriales y matrices eficientes |
| **GUI** | Pygame / Tkinter | Visualización de búsquedas y navegación de agentes |
| **Datos** | Pandas | Carga y manipulación de datasets (para ML) |

---

## 🤖 Algoritmos Implementados

### 1. Búsqueda y Navegación (Pathfinding)
* **Algoritmo A* (A-Star):**
    * Implementación de búsqueda heurística para encontrar el camino óptimo en un espacio de estados.
    * Uso de heurísticas (Distancia Manhattan y Euclídea).
    * Gestión de costes de terreno y obstáculos dinámicos.

### 2. Aprendizaje Supervisado (Clasificación)
* **Naive Bayes:**
    * Clasificador probabilístico basado en el Teorema de Bayes.
    * Implementación de suavizado de Laplace y manejo de atributos continuos/discretos.
* **ID3 (Árboles de Decisión):**
    * Construcción recursiva del árbol basada en la **Ganancia de Información**.
    * Cálculo manual de la **Entropía** del dataset para seleccionar el mejor atributo en cada nodo.

### 3. Aprendizaje No Supervisado (Clustering)
* **K-Means:**
    * Algoritmo de agrupamiento iterativo.
    * Inicialización de centroides y reasignación basada en distancia euclídea hasta la convergencia.

---

## 🚀 Guía de Instalación y Ejecución

### 1. Requisitos Previos

Asegúrate de tener Python 3.x instalado. Instala las dependencias necesarias:

```bash
pip install numpy pandas pygame matplotlib
