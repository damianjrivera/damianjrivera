#PROYECTO EN PROCESO
import tkinter as tk
from tkinter import ttk
import random
from collections import deque
import time

class MazeSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador de Laberintos - BFS/DFS")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f4f8')
        
        # Configuración del laberinto
        self.maze_size = 20
        self.cell_size = 25
        self.maze = []
        self.is_running = False
        
        self.EMPTY = 0
        self.WALL = 1
        self.START = 2
        self.END = 3
        self.PATH = 4
        self.VISITED = 5
        self.CURRENT = 6
        
        self.colors = {
            self.EMPTY: 'white',
            self.WALL: '#2d3748',
            self.START: '#48bb78',
            self.END: '#f56565',
            self.PATH: '#fbbf24',
            self.VISITED: '#93c5fd',
            self.CURRENT: '#a78bfa'
        }
        
        # Estadísticas
        self.visited_count = 0
        self.path_length = 0
        
        self.create_widgets()
        self.generate_maze()
        self.draw_maze()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg='#f0f4f8')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        title_label = tk.Label(main_frame, text="Solucionador de Laberintos", 
                               font=('Arial', 24, 'bold'), bg='#f0f4f8', fg='#1a202c')
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(main_frame, text="BFS (Anchura) vs DFS (Profundidad)", 
                                 font=('Arial', 12), bg='#f0f4f8', fg='#4a5568')
        subtitle_label.pack(pady=(0, 20))
    
        content_frame = tk.Frame(main_frame, bg='#f0f4f8')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        #  controles
        left_panel = tk.Frame(content_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.config(width=250)
        
        controls_label = tk.Label(left_panel, text="Controles", 
                                 font=('Arial', 16, 'bold'), bg='white', fg='#1a202c')
        controls_label.pack(pady=20, padx=20, anchor='w')
        
        algo_frame = tk.Frame(left_panel, bg='white')
        algo_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(algo_frame, text="Algoritmo:", font=('Arial', 10, 'bold'), 
                bg='white', fg='#4a5568').pack(anchor='w')
        
        self.algorithm_var = tk.StringVar(value='bfs')
        algo_combo = ttk.Combobox(algo_frame, textvariable=self.algorithm_var, 
                                  values=['bfs', 'dfs'], state='readonly', width=25)
        algo_combo.pack(pady=5, fill=tk.X)
        
        speed_frame = tk.Frame(left_panel, bg='white')
        speed_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(speed_frame, text="Velocidad (ms):", font=('Arial', 10, 'bold'), 
                bg='white', fg='#4a5568').pack(anchor='w')
        
        self.speed_var = tk.IntVar(value=50)
        self.speed_label = tk.Label(speed_frame, text="50", font=('Arial', 9), 
                                    bg='white', fg='#4a5568')
        self.speed_label.pack(anchor='w')
        
        speed_scale = tk.Scale(speed_frame, from_=1, to=200, orient=tk.HORIZONTAL,
                              variable=self.speed_var, command=self.update_speed_label,
                              bg='white', highlightthickness=0)
        speed_scale.pack(fill=tk.X)
        
        btn_frame = tk.Frame(left_panel, bg='white')
        btn_frame.pack(pady=20, padx=20, fill=tk.X)
        
        self.start_btn = tk.Button(btn_frame, text="▶ Iniciar", command=self.run_algorithm,
                                   bg='#3b82f6', fg='white', font=('Arial', 11, 'bold'),
                                   relief=tk.FLAT, cursor='hand2', padx=20, pady=10)
        self.start_btn.pack(fill=tk.X, pady=5)
        
        self.reset_btn = tk.Button(btn_frame, text="↻ Nuevo Laberinto", command=self.reset_maze,
                                   bg='#6b7280', fg='white', font=('Arial', 11, 'bold'),
                                   relief=tk.FLAT, cursor='hand2', padx=20, pady=10)
        self.reset_btn.pack(fill=tk.X, pady=5)
        
        # Estadísticas
        stats_frame = tk.Frame(left_panel, bg='#f9fafb', relief=tk.SOLID, borderwidth=1)
        stats_frame.pack(pady=20, padx=20, fill=tk.X)
        
        tk.Label(stats_frame, text="Estadísticas", font=('Arial', 12, 'bold'),
                bg='#f9fafb', fg='#1a202c').pack(pady=10)
        
        self.visited_label = tk.Label(stats_frame, text="Celdas visitadas: 0",
                                      font=('Arial', 10), bg='#f9fafb', fg='#4a5568')
        self.visited_label.pack(pady=5, padx=10, anchor='w')
        
        self.path_label = tk.Label(stats_frame, text="Longitud camino: -",
                                   font=('Arial', 10), bg='#f9fafb', fg='#4a5568')
        self.path_label.pack(pady=5, padx=10, anchor='w')
        
        self.status_label = tk.Label(stats_frame, text="Estado: En espera",
                                     font=('Arial', 10, 'bold'), bg='#f9fafb', fg='#4a5568')
        self.status_label.pack(pady=5, padx=10, anchor='w')
        
        legend_frame = tk.Frame(left_panel, bg='white')
        legend_frame.pack(pady=20, padx=20, fill=tk.X)
        
        tk.Label(legend_frame, text="Leyenda", font=('Arial', 12, 'bold'),
                bg='white', fg='#1a202c').pack(pady=10, anchor='w')
        
        legend_items = [
            ("Inicio", self.colors[self.START]),
            ("Fin", self.colors[self.END]),
            ("Pared", self.colors[self.WALL]),
            ("Actual", self.colors[self.CURRENT]),
            ("Visitado", self.colors[self.VISITED]),
            ("Camino", self.colors[self.PATH])
        ]
        
        for text, color in legend_items:
            item_frame = tk.Frame(legend_frame, bg='white')
            item_frame.pack(fill=tk.X, pady=2)
            
            color_box = tk.Label(item_frame, bg=color, width=3, relief=tk.SOLID, borderwidth=1)
            color_box.pack(side=tk.LEFT, padx=(0, 10))
            
            tk.Label(item_frame, text=text, font=('Arial', 9), bg='white', 
                    fg='#4a5568').pack(side=tk.LEFT)
        
        right_panel = tk.Frame(content_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        canvas_label = tk.Label(right_panel, text="Laberinto", 
                               font=('Arial', 16, 'bold'), bg='white', fg='#1a202c')
        canvas_label.pack(pady=10)
        canvas_frame = tk.Frame(right_panel, bg='white')
        canvas_frame.pack(pady=10, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, 
                               width=self.maze_size * self.cell_size + 2,
                               height=self.maze_size * self.cell_size + 2,
                               bg='white', highlightthickness=2, 
                               highlightbackground='#2d3748')
        self.canvas.pack()
        
        self.desc_label = tk.Label(right_panel, text="", font=('Arial', 10),
                                   bg='#eff6ff', fg='#1e40af', wraplength=450,
                                   justify=tk.LEFT, padx=20, pady=15)
        self.desc_label.pack(pady=10, padx=20, fill=tk.X)
        self.update_algorithm_description()
    
    def update_speed_label(self, value):
        self.speed_label.config(text=str(int(float(value))))
    
    def update_algorithm_description(self):
        if self.algorithm_var.get() == 'bfs':
            desc = "BFS (Búsqueda en Anchura): Explora nivel por nivel, garantizando encontrar el camino más corto. Usa una cola (FIFO)."
        else:
            desc = "DFS (Búsqueda en Profundidad): Explora tan profundo como sea posible antes de retroceder. Usa una pila (LIFO)."
        self.desc_label.config(text=desc)
    
    def generate_maze(self):
        self.maze = [[self.EMPTY for _ in range(self.maze_size)] 
                     for _ in range(self.maze_size)]
        
        for i in range(self.maze_size):
            for j in range(self.maze_size):
                if random.random() < 0.25:
                    self.maze[i][j] = self.WALL
        
        self.start = (1, 1)
        self.end = (self.maze_size - 2, self.maze_size - 2)
        
        self.maze[self.start[0]][self.start[1]] = self.START
        self.maze[self.end[0]][self.end[1]] = self.END
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = self.start[0] + dr, self.start[1] + dc
            if 0 <= nr < self.maze_size and 0 <= nc < self.maze_size:
                if self.maze[nr][nc] == self.WALL:
                    self.maze[nr][nc] = self.EMPTY
    
    def draw_maze(self):
        self.canvas.delete("all")
        
        for i in range(self.maze_size):
            for j in range(self.maze_size):
                x1 = j * self.cell_size + 1
                y1 = i * self.cell_size + 1
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                color = self.colors[self.maze[i][j]]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, 
                                            outline='#e5e7eb', width=1)
    
    def get_neighbors(self, row, col):
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.maze_size and 0 <= nc < self.maze_size:
                neighbors.append((nr, nc))
        return neighbors
    
    def bfs(self):
        queue = deque([(self.start[0], self.start[1], [])])
        visited = {(self.start[0], self.start[1])}
        self.visited_count = 0
        
        while queue:
            row, col, path = queue.popleft()
            
            # Verificar si llegamos al final
            if (row, col) == self.end:
                # Dibujar camino final
                for r, c in path:
                    if self.maze[r][c] not in [self.START, self.END]:
                        self.maze[r][c] = self.PATH
                self.draw_maze()
                self.path_length = len(path) + 1
                self.update_stats(found=True)
                return True
            
            # Marcar como actual
            if self.maze[row][col] not in [self.START, self.END]:
                self.maze[row][col] = self.CURRENT
            self.draw_maze()
            self.root.update()
            time.sleep(self.speed_var.get() / 1000.0)
            
            # Marcar como visitado
            if self.maze[row][col] not in [self.START, self.END]:
                self.maze[row][col] = self.VISITED
                self.visited_count += 1
            
            # Explorar vecinos
            for nr, nc in self.get_neighbors(row, col):
                if (nr, nc) not in visited and self.maze[nr][nc] != self.WALL:
                    visited.add((nr, nc))
                    queue.append((nr, nc, path + [(row, col)]))
            
            self.update_stats()
        
        return False
    
    def dfs(self):
        stack = [(self.start[0], self.start[1], [])]
        visited = {(self.start[0], self.start[1])}
        self.visited_count = 0
        
        while stack:
            row, col, path = stack.pop()
            
            # Verificar si llegamos al final
            if (row, col) == self.end:
                for r, c in path:
                    if self.maze[r][c] not in [self.START, self.END]:
                        self.maze[r][c] = self.PATH
                self.draw_maze()
                self.path_length = len(path) + 1
                self.update_stats(found=True)
                return True
    
            if self.maze[row][col] not in [self.START, self.END]:
                self.maze[row][col] = self.CURRENT
            self.draw_maze()
            self.root.update()
            time.sleep(self.speed_var.get() / 1000.0)
            
            if self.maze[row][col] not in [self.START, self.END]:
                self.maze[row][col] = self.VISITED
                self.visited_count += 1
            
            for nr, nc in self.get_neighbors(row, col):
                if (nr, nc) not in visited and self.maze[nr][nc] != self.WALL:
                    visited.add((nr, nc))
                    stack.append((nr, nc, path + [(row, col)]))
            
            self.update_stats()
        
        return False
    
    def update_stats(self, found=False):
        self.visited_label.config(text=f"Celdas visitadas: {self.visited_count}")
        
        if found:
            self.path_label.config(text=f"Longitud camino: {self.path_length}")
            self.status_label.config(text="Estado: ¡Encontrado!", fg='#16a34a')
        else:
            self.status_label.config(text="Estado: Buscando...", fg='#2563eb')
    
    def run_algorithm(self):
        if self.is_running:
            return
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED, bg='#9ca3af')
        self.reset_btn.config(state=tk.DISABLED, bg='#9ca3af')
        
        # Resetear laberinto
        for i in range(self.maze_size):
            for j in range(self.maze_size):
                if self.maze[i][j] in [self.PATH, self.VISITED, self.CURRENT]:
                    self.maze[i][j] = self.EMPTY
        
        self.maze[self.start[0]][self.start[1]] = self.START
        self.maze[self.end[0]][self.end[1]] = self.END
        self.draw_maze()
        
        self.visited_count = 0
        self.path_length = 0
        self.update_stats()
        self.update_algorithm_description()
        
        # Ejecutar algoritmo
        if self.algorithm_var.get() == 'bfs':
            found = self.bfs()
        else:
            found = self.dfs()
        
        if not found:
            self.status_label.config(text="Estado: No hay camino", fg='#dc2626')
        
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL, bg='#3b82f6')
        self.reset_btn.config(state=tk.NORMAL, bg='#6b7280')
    
    def reset_maze(self):
        if self.is_running:
            return
        
        self.generate_maze()
        self.draw_maze()
        self.visited_count = 0
        self.path_length = 0
        self.visited_label.config(text="Celdas visitadas: 0")
        self.path_label.config(text="Longitud camino: -")
        self.status_label.config(text="Estado: En espera", fg='#4a5568')

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeSolver(root)
    root.mainloop()