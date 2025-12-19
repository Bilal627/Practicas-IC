# 🤖 Proyectos de Inteligencia Artificial (IA)

Este repositorio contiene tres implementaciones fundamentales desarrolladas en **Python** para la asignatura de Ingeniería del Conocimiento. Los proyectos abarcan algoritmos de búsqueda, aprendizaje supervisado y técnicas de clustering.

## 🛠️ Tecnologías y Herramientas
* **Lenguaje:** Python 3.x
* **Librerías:** 
    * **NumPy:** Procesamiento numérico y matricial.
    * **Pygame:** Desarrollo de interfaces gráficas y simulaciones.
    * **Tkinter:** Visualización de resultados y métricas.

---

## 🚀 Proyectos Incluidos

### 1. Búsqueda de Rutas con Algoritmo A*
Simulación visual que encuentra rutas óptimas en una cuadrícula con obstáculos y zonas de riesgo.
* **Algoritmo:** Implementación de **A*** utilizando una cola de prioridad para gestionar la frontera de expansión.
* **Heurística:** Combina la distancia euclidiana con factores de riesgo variables que aumentan el costo de las celdas peligrosas.
* **Funcionalidades:** Soporte para **Waypoints** (puntos intermedios) y visualización en tiempo real del costo total del camino.

### 2. Árbol de Decisión ID3
Sistema de clasificación supervisada basado en el algoritmo ID3.
* **Lógica:** Cálculo de **Entropía de Shannon** y **Ganancia de Información** para la selección del mejor atributo en cada nodo.
* **Recursividad:** Construcción completa del árbol hasta cumplir las condiciones de parada de pureza de clase.
* **Interfaz:** Renderizado gráfico del árbol con diferenciación de colores para nodos internos y hojas de decisión.

### 3. Métodos de Clasificación
Implementación de tres algoritmos para la categorización de datos sobre el dataset Iris.
* **Bayes:** Clasificación probabilística mediante el cálculo de medias y matrices de covarianza por clase.
* **Fuzzy K-Means:** Agrupamiento borroso con cálculo de probabilidades de pertenencia y actualización de centroides.
* **Algoritmo de Lloyd:** Método competitivo para la asignación de puntos al centroide más cercano.

---

## 📂 Estructura del Proyecto
* `A_Estrella/`: Simulación visual del algoritmo A*.
* `ID3/`: Lógica del árbol de decisión y archivos de entrenamiento.
* `Clasificadores/`: Script con Bayes, Lloyd y Fuzzy K-Means junto al dataset Iris.

---
_Autor: **Bilal El Mourabit El Mourabiti**_
