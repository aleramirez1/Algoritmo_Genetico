import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from algoritmo_genetico import AlgoritmoGenetico
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os

class AplicacionEscritorio:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Asignacion de Vigilantes - Algoritmo Genetico")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        self.ag = None
        self.ejecutando = False
        self.datos_vigilantes = []
        self.datos_restricciones = []
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        titulo = tk.Label(main_frame, text="SISTEMA DE ASIGNACION DE VIGILANTES", 
                         font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        titulo.pack(pady=10)
        
        contenedor = tk.Frame(main_frame, bg='#f0f0f0')
        contenedor.pack(fill=tk.BOTH, expand=True)
        
        panel_izq = tk.Frame(contenedor, bg='white', relief=tk.RAISED, borderwidth=2, width=520)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        panel_izq.pack_propagate(False)
        
        panel_der = tk.Frame(contenedor, bg='white', relief=tk.RAISED, borderwidth=2)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.crear_panel_configuracion(panel_izq)
        self.crear_panel_resultados(panel_der)
    
    def crear_panel_configuracion(self, parent):
        tk.Label(parent, text="CONFIGURACION", font=('Arial', 14, 'bold'), 
                bg='white', fg='#34495e').pack(pady=10)
        
        # Frame principal con una sola columna
        frame_principal = tk.Frame(parent, bg='white')
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # DOS COLUMNAS: Inputs de configuración
        frame_config = tk.Frame(frame_principal, bg='white')
        frame_config.pack(fill=tk.X)
        
        # Columna izquierda
        frame_col_izq = tk.Frame(frame_config, bg='white')
        frame_col_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Columna derecha
        frame_col_der = tk.Frame(frame_config, bg='white')
        frame_col_der.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        configs = [
            ("Numero de Dias:", "num_dias", 7),
            ("Numero de Turnos:", "num_turnos", 2),
            ("Numero de Puestos:", "num_puestos", 3),
            ("Tamaño Poblacion:", "tam_poblacion", 20),
            ("Probabilidad Cruza:", "prob_cruza", 0.85),
            ("Probabilidad Mutacion:", "prob_mutacion", 0.20),
            ("Max Generaciones:", "max_generaciones", 100),
            ("Horas Maximas:", "horas_max", 60.0),
            ("Max Turnos Nocturnos:", "max_turnos_nocturnos", 3)
        ]
        
        self.entries = {}
        
        # Dividir configs en dos columnas
        mitad = (len(configs) + 1) // 2
        
        for i, (label, key, default) in enumerate(configs):
            # Determinar en qué columna va
            if i < mitad:
                parent_frame = frame_col_izq
            else:
                parent_frame = frame_col_der
            
            frame_row = tk.Frame(parent_frame, bg='white')
            frame_row.pack(fill=tk.X, pady=5, anchor='w')
            
            tk.Label(frame_row, text=label, font=('Arial', 10), 
                    bg='white', width=18, anchor='w').pack(side=tk.LEFT)
            
            entry = tk.Entry(frame_row, font=('Arial', 10), width=10)
            entry.insert(0, str(default))
            
            if key == 'num_dias':
                entry.config(state='readonly', bg='#e0e0e0')
            
            entry.pack(side=tk.LEFT, padx=2)
            
            self.entries[key] = entry
        
        # Campo oculto para num_vigilantes (se actualiza automáticamente desde el CSV)
        self.entries['num_vigilantes'] = tk.Entry(frame_config)
        self.entries['num_vigilantes'].insert(0, "4")
        # No se hace pack() para que no se muestre
        
        # CONFIGURACION DE COSTOS
        frame_costos = tk.Frame(frame_principal, bg='#e8f5e9', relief=tk.RAISED, borderwidth=2)
        frame_costos.pack(fill=tk.X, pady=(10, 5))
        
        tk.Label(frame_costos, text="CONFIGURACION DE COSTOS:", font=('Arial', 9, 'bold'), 
                bg='#e8f5e9', fg='#2c3e50').pack(pady=5)
        
        # Pago por turno (Lun-Sab)
        frame_pago1 = tk.Frame(frame_costos, bg='#e8f5e9')
        frame_pago1.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(frame_pago1, text="Pago turno (Lun-Sab):", bg='#e8f5e9', 
                font=('Arial', 9), width=20, anchor='w').pack(side=tk.LEFT)
        self.entry_pago_dia = tk.Entry(frame_pago1, width=10, font=('Arial', 9))
        self.entry_pago_dia.insert(0, "316")
        self.entry_pago_dia.pack(side=tk.LEFT, padx=5)
        tk.Label(frame_pago1, text="MXN", bg='#e8f5e9', font=('Arial', 9)).pack(side=tk.LEFT)
        
        # Pago turno Domingo
        frame_pago2 = tk.Frame(frame_costos, bg='#e8f5e9')
        frame_pago2.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(frame_pago2, text="Pago turno Domingo:", bg='#e8f5e9', 
                font=('Arial', 9), width=20, anchor='w').pack(side=tk.LEFT)
        self.entry_pago_domingo = tk.Entry(frame_pago2, width=10, font=('Arial', 9))
        self.entry_pago_domingo.insert(0, "632")
        self.entry_pago_domingo.pack(side=tk.LEFT, padx=5)
        tk.Label(frame_pago2, text="MXN", bg='#e8f5e9', font=('Arial', 9)).pack(side=tk.LEFT)
        
        # Pago turno extra
        frame_pago3 = tk.Frame(frame_costos, bg='#e8f5e9')
        frame_pago3.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(frame_pago3, text="Pago 2do turno/día:", bg='#e8f5e9', 
                font=('Arial', 9), width=20, anchor='w').pack(side=tk.LEFT)
        self.entry_pago_dia_extra = tk.Entry(frame_pago3, width=10, font=('Arial', 9))
        self.entry_pago_dia_extra.insert(0, "632")
        self.entry_pago_dia_extra.pack(side=tk.LEFT, padx=3)
        tk.Label(frame_pago3, text="MXN", bg='#e8f5e9', font=('Arial', 8)).pack(side=tk.LEFT)
        
        tk.Label(frame_costos, text="", bg='#e8f5e9').pack(pady=2)
        
        # SECCION DE CARGA DE ARCHIVOS - BASE DE CONOCIMIENTO
        frame_archivos = tk.Frame(frame_principal, bg='#e3f2fd', relief=tk.RAISED, borderwidth=2)
        frame_archivos.pack(fill=tk.X, pady=(5, 10))
        
        tk.Label(frame_archivos, text="BASE DE CONOCIMIENTO:", font=('Arial', 9, 'bold'), 
                bg='#e3f2fd', fg='#2c3e50').pack(pady=5)
        
        # Input para archivo de vigilantes
        frame_vigilantes = tk.Frame(frame_archivos, bg='#e3f2fd')
        frame_vigilantes.pack(fill=tk.X, padx=10, pady=2)
        
        tk.Label(frame_vigilantes, text="Vigilantes:", bg='#e3f2fd', 
                font=('Arial', 9), width=18, anchor='w').pack(side=tk.LEFT)
        
        self.entry_archivo_vigilantes = tk.Entry(frame_vigilantes, font=('Arial', 8), width=35)
        self.entry_archivo_vigilantes.insert(0, "base_conocimientos/vigilantes.csv")
        self.entry_archivo_vigilantes.pack(side=tk.LEFT, padx=3)
        
        tk.Button(frame_vigilantes, text="📁", command=self.seleccionar_archivo_vigilantes,
                 font=('Arial', 8), bg='#90caf9', fg='white', cursor='hand2', width=3).pack(side=tk.LEFT)
        
        # Input para archivo de turnos
        frame_turnos = tk.Frame(frame_archivos, bg='#e3f2fd')
        frame_turnos.pack(fill=tk.X, padx=10, pady=2)
        
        tk.Label(frame_turnos, text="Turnos:", bg='#e3f2fd', 
                font=('Arial', 9), width=18, anchor='w').pack(side=tk.LEFT)
        
        self.entry_archivo_turnos = tk.Entry(frame_turnos, font=('Arial', 8), width=35)
        self.entry_archivo_turnos.insert(0, "base_conocimientos/turnos.csv")
        self.entry_archivo_turnos.pack(side=tk.LEFT, padx=3)
        
        tk.Button(frame_turnos, text="📁", command=self.seleccionar_archivo_turnos,
                 font=('Arial', 8), bg='#90caf9', fg='white', cursor='hand2', width=3).pack(side=tk.LEFT)
        
        # Input para archivo de puestos
        frame_puestos = tk.Frame(frame_archivos, bg='#e3f2fd')
        frame_puestos.pack(fill=tk.X, padx=10, pady=2)
        
        tk.Label(frame_puestos, text="Puestos:", bg='#e3f2fd', 
                font=('Arial', 9), width=18, anchor='w').pack(side=tk.LEFT)
        
        self.entry_archivo_puestos = tk.Entry(frame_puestos, font=('Arial', 8), width=35)
        self.entry_archivo_puestos.insert(0, "base_conocimientos/puestos.csv")
        self.entry_archivo_puestos.pack(side=tk.LEFT, padx=3)
        
        tk.Button(frame_puestos, text="📁", command=self.seleccionar_archivo_puestos,
                 font=('Arial', 8), bg='#90caf9', fg='white', cursor='hand2', width=3).pack(side=tk.LEFT)
        
        # Input para archivo de políticas
        frame_politicas = tk.Frame(frame_archivos, bg='#e3f2fd')
        frame_politicas.pack(fill=tk.X, padx=10, pady=2)
        
        tk.Label(frame_politicas, text="Políticas Empresa:", bg='#e3f2fd', 
                font=('Arial', 9), width=18, anchor='w').pack(side=tk.LEFT)
        
        self.entry_archivo_politicas = tk.Entry(frame_politicas, font=('Arial', 8), width=35)
        self.entry_archivo_politicas.insert(0, "base_conocimientos/politicas_empresa.csv")
        self.entry_archivo_politicas.pack(side=tk.LEFT, padx=3)
        
        tk.Button(frame_politicas, text="📁", command=self.seleccionar_archivo_politicas,
                 font=('Arial', 8), bg='#90caf9', fg='white', cursor='hand2', width=3).pack(side=tk.LEFT)
        
        # Input para archivo de normativas
        frame_normativas = tk.Frame(frame_archivos, bg='#e3f2fd')
        frame_normativas.pack(fill=tk.X, padx=10, pady=2)
        
        tk.Label(frame_normativas, text="Normativas Laborales:", bg='#e3f2fd', 
                font=('Arial', 9), width=18, anchor='w').pack(side=tk.LEFT)
        
        self.entry_archivo_normativas = tk.Entry(frame_normativas, font=('Arial', 8), width=35)
        self.entry_archivo_normativas.insert(0, "base_conocimientos/normativas_laborales.csv")
        self.entry_archivo_normativas.pack(side=tk.LEFT, padx=3)
        
        tk.Button(frame_normativas, text="📁", command=self.seleccionar_archivo_normativas,
                 font=('Arial', 8), bg='#90caf9', fg='white', cursor='hand2', width=3).pack(side=tk.LEFT)
        
        # Input para archivo de restricciones
        frame_restricciones_file = tk.Frame(frame_archivos, bg='#e3f2fd')
        frame_restricciones_file.pack(fill=tk.X, padx=10, pady=2)
        
        tk.Label(frame_restricciones_file, text="Restricciones:", bg='#e3f2fd', 
                font=('Arial', 9), width=18, anchor='w').pack(side=tk.LEFT)
        
        self.entry_archivo_restricciones = tk.Entry(frame_restricciones_file, font=('Arial', 8), width=35)
        self.entry_archivo_restricciones.insert(0, "base_conocimientos/restricciones.csv")
        self.entry_archivo_restricciones.pack(side=tk.LEFT, padx=3)
        
        tk.Button(frame_restricciones_file, text="📁", command=self.seleccionar_archivo_restricciones,
                 font=('Arial', 8), bg='#90caf9', fg='white', cursor='hand2', width=3).pack(side=tk.LEFT)
        
        # Input para archivo de entradas del sistema
        frame_entradas = tk.Frame(frame_archivos, bg='#e3f2fd')
        frame_entradas.pack(fill=tk.X, padx=10, pady=2)
        
        tk.Label(frame_entradas, text="Entradas Sistema:", bg='#e3f2fd', 
                font=('Arial', 9), width=18, anchor='w').pack(side=tk.LEFT)
        
        self.entry_archivo_entradas = tk.Entry(frame_entradas, font=('Arial', 8), width=35)
        self.entry_archivo_entradas.insert(0, "base_conocimientos/entradas_sistema.csv")
        self.entry_archivo_entradas.pack(side=tk.LEFT, padx=3)
        
        tk.Button(frame_entradas, text="📁", command=self.seleccionar_archivo_entradas,
                 font=('Arial', 8), bg='#90caf9', fg='white', cursor='hand2', width=3).pack(side=tk.LEFT)
        
        tk.Label(frame_archivos, text="", bg='#e3f2fd').pack(pady=3)
        
        # Boton para cargar y ejecutar
        self.btn_ejecutar_todo = tk.Button(frame_archivos, text="CARGAR Y EJECUTAR", 
                                           command=self.cargar_y_ejecutar,
                                           font=('Arial', 11, 'bold'), bg='#27ae60', fg='white',
                                           padx=30, pady=10, cursor='hand2')
        self.btn_ejecutar_todo.pack(pady=5)
        
        tk.Label(frame_archivos, text="", bg='#e3f2fd').pack(pady=2)
        
        # Progress bar
        self.progress = ttk.Progressbar(parent, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=20, pady=10)
        
        # Consola invisible (para que no haya errores en self.log)
        self.consola = scrolledtext.ScrolledText(parent, height=0, font=('Consolas', 9))
        # No se hace pack() para que no se muestre
    
    def crear_panel_resultados(self, parent):
        tk.Label(parent, text="RESULTADOS", font=('Arial', 14, 'bold'), 
                bg='white', fg='#34495e').pack(pady=10)
        
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tab_metricas = tk.Frame(notebook, bg='white')
        tab_grafica = tk.Frame(notebook, bg='white')
        tab_horario = tk.Frame(notebook, bg='white')
        
        notebook.add(tab_metricas, text='Metricas')
        notebook.add(tab_grafica, text='Grafica Evolucion')
        notebook.add(tab_horario, text='Horarios')
        
        self.crear_tab_metricas(tab_metricas)
        self.crear_tab_grafica(tab_grafica)
        self.crear_tab_horario(tab_horario)
    
    def crear_tab_restricciones(self, parent):
        tk.Label(parent, text="RESTRICCIONES Y LEYES DEL SISTEMA", 
                font=('Arial', 14, 'bold'), bg='white', fg='#2c3e50').pack(pady=20)
        
        frame_botones = tk.Frame(parent, bg='white')
        frame_botones.pack(fill=tk.X, padx=40, pady=10)
        
        frame_botones_row = tk.Frame(frame_botones, bg='white')
        frame_botones_row.pack()
        
        btn_cargar = tk.Button(frame_botones_row, text="Cargar Restricciones desde CSV", 
                              command=self.actualizar_restricciones_desde_csv,
                              font=('Arial', 10, 'bold'), bg='#e67e22', fg='white',
                              padx=20, pady=8, cursor='hand2')
        btn_cargar.pack(side=tk.LEFT, padx=5)
        
        btn_exportar = tk.Button(frame_botones_row, text="Exportar a Excel", 
                                command=self.exportar_excel,
                                font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
                                padx=20, pady=8, cursor='hand2')
        btn_exportar.pack(side=tk.LEFT, padx=5)
        
        frame_contenido = tk.Frame(parent, bg='white')
        frame_contenido.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        self.text_restricciones_tab = scrolledtext.ScrolledText(frame_contenido, 
                                                       font=('Consolas', 10), 
                                                       bg='#ecf0f1', fg='#2c3e50',
                                                       wrap=tk.WORD)
        self.text_restricciones_tab.pack(fill=tk.BOTH, expand=True)
        
        self.mostrar_restricciones_default()
    
    def mostrar_restricciones_default(self):
        restricciones_texto = """
================================================================================
                        RESTRICCIONES DEL SISTEMA
================================================================================

Para cargar restricciones personalizadas, haz clic en el boton
"Cargar Restricciones desde CSV" y selecciona el archivo restricciones.csv

Restricciones por defecto:

HORARIOS:
- Turno Dia: 08:00 - 20:00 (10.5 hrs efectivas)
- Turno Noche: 20:00 - 08:00 (10.5 hrs efectivas)

RESTRICCIONES LEGALES:
- Maximo 2 turnos por dia por vigilante (2do turno cobra extra)
- Horas legales: 48 hrs/semana
- Maximo 3 turnos nocturnos por semana
- Cobertura 100% requerida

SUELDOS:
- Pago por turno (Lun-Sab): $316 MXN
- Pago turno Domingo: $632 MXN (doble)
- Pago 2do turno mismo dia: $632 MXN (extra)
- Sueldo minimo semanal: $2,396 MXN por vigilante

PENALIZACIONES FITNESS:
- Cobertura: Peso 1.0 (Critica)
- Horas Extra: Peso 0.3 (Media)
- Balance: Peso 0.2 (Baja)
- Violaciones: Peso 0.5 (Alta - mas de 2 turnos/dia)

================================================================================
"""
        self.text_restricciones_tab.delete(1.0, tk.END)
        self.text_restricciones_tab.insert(1.0, restricciones_texto)
    
    def actualizar_restricciones_desde_csv(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de restricciones",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir="base_conocimientos",
            initialfile="restricciones.csv"
        )
        
        if not archivo:
            return
        
        try:
            import csv
            
            with open(archivo, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                filas = list(reader)
            
            self.text_restricciones_tab.delete(1.0, tk.END)
            self.text_restricciones_tab.insert(tk.END, "="*80 + "\n")
            self.text_restricciones_tab.insert(tk.END, "RESTRICCIONES CARGADAS DESDE CSV\n")
            self.text_restricciones_tab.insert(tk.END, "="*80 + "\n\n")
            
            categorias = {}
            for i, fila in enumerate(filas):
                if i == 0:
                    continue
                if len(fila) >= 3:
                    tipo = fila[0]
                    if tipo not in categorias:
                        categorias[tipo] = []
                    categorias[tipo].append(fila)
            
            for tipo in ['HORARIOS', 'RESTRICCION', 'PENALIZACION', 'SUELDO', 'CONFIGURACION', 'CALIDAD']:
                if tipo in categorias:
                    self.text_restricciones_tab.insert(tk.END, f"\n{tipo}:\n")
                    self.text_restricciones_tab.insert(tk.END, "-"*80 + "\n")
                    for fila in categorias[tipo]:
                        desc = fila[1] if len(fila) > 1 else ""
                        valor = fila[2] if len(fila) > 2 else ""
                        unidad = fila[3] if len(fila) > 3 else ""
                        penalizacion = fila[4] if len(fila) > 4 else ""
                        
                        linea = f"  {desc}: {valor} {unidad}"
                        if penalizacion and penalizacion != "N/A":
                            linea += f" (Penalizacion: {penalizacion})"
                        self.text_restricciones_tab.insert(tk.END, linea + "\n")
            
            self.text_restricciones_tab.insert(tk.END, "\n" + "="*80 + "\n")
            self.text_restricciones_tab.insert(tk.END, f"Total restricciones cargadas: {len(filas)-1}\n")
            self.text_restricciones_tab.insert(tk.END, "="*80 + "\n")
            
            messagebox.showinfo("Exito", f"Restricciones cargadas correctamente\nTotal: {len(filas)-1} restricciones")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar restricciones:\n{str(e)}")
    
    def crear_tab_metricas(self, parent):
        frame_metricas = tk.Frame(parent, bg='white')
        frame_metricas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.labels_metricas = {}
        
        metricas = [
            ("Mejor Fitness:", "fitness", "#27ae60"),
            ("Cobertura:", "cobertura", "#3498db"),
            ("Horas Extra:", "horas_extra", "#e74c3c"),
            ("Balance Carga:", "balance", "#f39c12"),
            ("Violaciones:", "violaciones", "#e74c3c")
        ]
        
        for i, (label, key, color) in enumerate(metricas):
            frame = tk.Frame(frame_metricas, bg=color, relief=tk.RAISED, borderwidth=3)
            frame.pack(fill=tk.X, pady=10)
            
            tk.Label(frame, text=label, font=('Arial', 12, 'bold'), 
                    bg=color, fg='white').pack(pady=5)
            
            valor_label = tk.Label(frame, text="--", font=('Arial', 24, 'bold'), 
                                  bg=color, fg='white')
            valor_label.pack(pady=10)
            
            self.labels_metricas[key] = valor_label
    
    def crear_tab_grafica(self, parent):
        frame_info = tk.Frame(parent, bg='#ecf0f1', height=80)
        frame_info.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame_info, text="EVOLUCION DEL FITNESS - COMO SE GENERA LA GRAFICA", 
                font=('Arial', 10, 'bold'), bg='#ecf0f1', fg='#2c3e50').pack(pady=5)
        
        info_texto = ("Esta grafica muestra como evoluciona el MEJOR fitness en cada generacion.\n"
                     "Cada punto representa el mejor individuo de esa generacion.\n"
                     "Si la linea sube = el algoritmo esta mejorando. Si se aplana = ya encontro una buena solucion.")
        
        tk.Label(frame_info, text=info_texto, font=('Arial', 8), 
                bg='#ecf0f1', fg='#34495e', wraplength=1200, justify=tk.LEFT).pack(padx=20, pady=5)
        
        frame_controles = tk.Frame(parent, bg='white', height=40)
        frame_controles.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame_controles, text="Controles:", font=('Arial', 9, 'bold'), 
                bg='white').pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_controles, text="🖱️ Scroll: Zoom | Arrastrar: Mover grafica", 
                font=('Arial', 8), bg='white', fg='#7f8c8d').pack(side=tk.LEFT, padx=10)
        
        btn_zoom_in = tk.Button(frame_controles, text="🔍 Zoom In", 
                               command=self.zoom_in_grafica,
                               font=('Arial', 8), bg='#3498db', fg='white',
                               padx=10, pady=3, cursor='hand2')
        btn_zoom_in.pack(side=tk.LEFT, padx=2)
        
        btn_zoom_out = tk.Button(frame_controles, text="🔍 Zoom Out", 
                                command=self.zoom_out_grafica,
                                font=('Arial', 8), bg='#3498db', fg='white',
                                padx=10, pady=3, cursor='hand2')
        btn_zoom_out.pack(side=tk.LEFT, padx=2)
        
        btn_reset = tk.Button(frame_controles, text="🏠 Reset", 
                             command=self.reset_grafica,
                             font=('Arial', 8), bg='#95a5a6', fg='white',
                             padx=10, pady=3, cursor='hand2')
        btn_reset.pack(side=tk.LEFT, padx=2)
        
        btn_guardar = tk.Button(frame_controles, text="💾 Guardar", 
                               command=self.guardar_grafica,
                               font=('Arial', 8), bg='#27ae60', fg='white',
                               padx=10, pady=3, cursor='hand2')
        btn_guardar.pack(side=tk.LEFT, padx=2)
        
        self.fig = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Evolucion del Fitness', fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Generacion', fontsize=12)
        self.ax.set_ylabel('Fitness', fontsize=12)
        self.ax.grid(True, alpha=0.3)
        
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.xlim_original = None
        self.ylim_original = None
        self.press = None
        
        self.canvas.mpl_connect('scroll_event', self.on_scroll_zoom)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
    
    def zoom_in_grafica(self):
        if self.xlim_original is None:
            self.xlim_original = self.ax.get_xlim()
            self.ylim_original = self.ax.get_ylim()
        
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        
        x_range = (xlim[1] - xlim[0]) * 0.7
        y_range = (ylim[1] - ylim[0]) * 0.7
        
        self.ax.set_xlim(x_center - x_range/2, x_center + x_range/2)
        self.ax.set_ylim(y_center - y_range/2, y_center + y_range/2)
        self.canvas.draw()
    
    def zoom_out_grafica(self):
        if self.xlim_original is None:
            return
        
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        
        x_range = (xlim[1] - xlim[0]) * 1.3
        y_range = (ylim[1] - ylim[0]) * 1.3
        
        self.ax.set_xlim(x_center - x_range/2, x_center + x_range/2)
        self.ax.set_ylim(y_center - y_range/2, y_center + y_range/2)
        self.canvas.draw()
    
    def reset_grafica(self):
        if self.xlim_original is not None:
            self.ax.set_xlim(self.xlim_original)
            self.ax.set_ylim(self.ylim_original)
            self.canvas.draw()
    
    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        self.press = event.xdata, event.ydata
    
    def on_release(self, event):
        self.press = None
        self.canvas.draw()
    
    def on_motion(self, event):
        if self.press is None or event.inaxes != self.ax:
            return
        
        if self.xlim_original is None:
            self.xlim_original = self.ax.get_xlim()
            self.ylim_original = self.ax.get_ylim()
        
        xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        self.ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
        self.ax.set_ylim(ylim[0] - dy, ylim[1] - dy)
        
        self.canvas.draw()
    
    def on_scroll_zoom(self, event):
        if self.xlim_original is None:
            self.xlim_original = self.ax.get_xlim()
            self.ylim_original = self.ax.get_ylim()
        
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        xdata = event.xdata
        ydata = event.ydata
        
        if xdata is None or ydata is None:
            return
        
        if event.button == 'up':
            scale_factor = 0.9
        elif event.button == 'down':
            scale_factor = 1.1
        else:
            return
        
        new_width = (xlim[1] - xlim[0]) * scale_factor
        new_height = (ylim[1] - ylim[0]) * scale_factor
        
        relx = (xlim[1] - xdata) / (xlim[1] - xlim[0])
        rely = (ylim[1] - ydata) / (ylim[1] - ylim[0])
        
        self.ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
        self.ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
        self.canvas.draw()
    
    def guardar_grafica(self):
        if self.ag is None:
            messagebox.showwarning("Advertencia", "Primero debes ejecutar el algoritmo")
            return
        
        archivo = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), ("SVG", "*.svg"), ("All files", "*.*")],
            initialfile="grafica_fitness.png"
        )
        
        if archivo:
            self.fig.savefig(archivo, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Exito", f"Grafica guardada en:\n{archivo}")
    
    def crear_tab_costos(self, parent):
        tk.Label(parent, text="COSTOS Y SUELDOS", 
                font=('Arial', 12, 'bold'), bg='white', fg='#34495e').pack(pady=10)
        
        frame_boton = tk.Frame(parent, bg='white')
        frame_boton.pack(pady=10)
        
        btn_calcular = tk.Button(frame_boton, text="Calcular Costos", 
                                command=self.calcular_costos,
                                font=('Arial', 11, 'bold'), bg='#3498db', fg='white',
                                padx=20, pady=10, cursor='hand2')
        btn_calcular.pack()
        
        tk.Label(parent, text="Los valores de pago se configuran en el panel izquierdo", 
                font=('Arial', 9, 'italic'), bg='white', fg='#7f8c8d').pack(pady=5)
        
        frame_resultados = tk.Frame(parent, bg='white')
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.text_costos = scrolledtext.ScrolledText(frame_resultados, height=20, 
                                                     font=('Consolas', 9), bg='#ecf0f1')
        self.text_costos.pack(fill=tk.BOTH, expand=True)
    
    def crear_tab_horario(self, parent):
        self.notebook_horarios = ttk.Notebook(parent)
        self.notebook_horarios.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tabs_horarios = {}
        for nombre in ['Top 1', 'Top 2', 'Top 3', 'Peor']:
            tab = tk.Frame(self.notebook_horarios, bg='white')
            self.notebook_horarios.add(tab, text=nombre)
            
            frame_info = tk.Frame(tab, bg='#3498db', height=60)
            frame_info.pack(fill=tk.X)
            frame_info.pack_propagate(False)
            
            fitness_label = tk.Label(frame_info, text="Fitness: --", 
                                    font=('Arial', 14, 'bold'), bg='#3498db', fg='white')
            fitness_label.pack(pady=5)
            
            calidad_label = tk.Label(frame_info, text="", 
                                    font=('Arial', 12), bg='#3498db', fg='white')
            calidad_label.pack(pady=5)
            
            frame_scroll_container = tk.Frame(tab, bg='white')
            frame_scroll_container.pack(fill=tk.BOTH, expand=True)
            
            scrollbar_y = tk.Scrollbar(frame_scroll_container, orient=tk.VERTICAL)
            scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
            
            scrollbar_x = tk.Scrollbar(frame_scroll_container, orient=tk.HORIZONTAL)
            scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            
            canvas_horario = tk.Canvas(frame_scroll_container, bg='white', 
                                      yscrollcommand=scrollbar_y.set,
                                      xscrollcommand=scrollbar_x.set)
            canvas_horario.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            scrollbar_y.config(command=canvas_horario.yview)
            scrollbar_x.config(command=canvas_horario.xview)
            
            frame_horario = tk.Frame(canvas_horario, bg='white')
            canvas_window = canvas_horario.create_window((0, 0), window=frame_horario, anchor='nw')
            
            def configure_scroll(event, canvas=canvas_horario):
                canvas.configure(scrollregion=canvas.bbox('all'))
            
            frame_horario.bind('<Configure>', configure_scroll)
            
            self.tabs_horarios[nombre] = {
                'frame': frame_horario,
                'canvas': canvas_horario,
                'fitness_label': fitness_label,
                'calidad_label': calidad_label
            }
    
    def log(self, mensaje):
        self.consola.insert(tk.END, mensaje + '\n')
        self.consola.see(tk.END)
        self.root.update()
    
    def ejecutar_algoritmo(self):
        if self.ejecutando:
            messagebox.showwarning("Advertencia", "El algoritmo ya esta ejecutandose")
            return
        
        try:
            num_vigilantes = int(self.entries['num_vigilantes'].get())
            num_dias = int(self.entries['num_dias'].get())
            num_turnos = int(self.entries['num_turnos'].get())
            num_puestos = int(self.entries['num_puestos'].get())
            tam_poblacion = int(self.entries['tam_poblacion'].get())
            
            if num_dias != 7:
                messagebox.showerror("Error", "Numero de dias debe ser exactamente 7 (Lunes a Domingo)")
                return
            
            if num_vigilantes < 1:
                messagebox.showerror("Error", "Numero de vigilantes debe ser al menos 1")
                return
            
            if num_turnos < 1:
                messagebox.showerror("Error", "Numero de turnos debe ser al menos 1")
                return
            
            if num_puestos < 1:
                messagebox.showerror("Error", "Numero de puestos debe ser al menos 1")
                return
            
            if tam_poblacion < 10:
                messagebox.showerror("Error", "Tamaño de poblacion debe ser al menos 10")
                return
            
            if num_vigilantes < num_puestos:
                respuesta = messagebox.askyesno("Advertencia", 
                    f"Tienes {num_vigilantes} vigilantes pero necesitas al menos {num_puestos} para cubrir los puestos.\n\n"
                    f"Esto resultara en baja cobertura.\n\n¿Continuar de todos modos?")
                if not respuesta:
                    return
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numericos validos")
            return
        
        self.ejecutando = True
        self.btn_ejecutar_todo.config(state=tk.DISABLED)
        self.progress.start()
        
        thread = threading.Thread(target=self.ejecutar_ag_thread)
        thread.daemon = True
        thread.start()
    
    def ejecutar_ag_thread(self):
        try:
            self.consola.delete(1.0, tk.END)
            self.log("="*60)
            self.log("INICIANDO ALGORITMO GENETICO")
            self.log("="*60)
            
            self.log("\n[1/10] Leyendo parametros...")
            num_vigilantes = int(self.entries['num_vigilantes'].get())
            num_dias = int(self.entries['num_dias'].get())
            num_turnos = int(self.entries['num_turnos'].get())
            num_puestos = int(self.entries['num_puestos'].get())
            tam_poblacion = int(self.entries['tam_poblacion'].get())
            prob_cruza = float(self.entries['prob_cruza'].get())
            prob_mutacion = float(self.entries['prob_mutacion'].get())
            max_generaciones = int(self.entries['max_generaciones'].get())
            horas_max = float(self.entries['horas_max'].get())
            max_turnos_nocturnos = int(self.entries['max_turnos_nocturnos'].get())
            
            self.log(f"  Vigilantes: {num_vigilantes}")
            self.log(f"  Dias: {num_dias}")
            self.log(f"  Turnos: {num_turnos}")
            self.log(f"  Puestos: {num_puestos}")
            self.log(f"  Poblacion: {tam_poblacion}")
            self.log(f"  Generaciones: {max_generaciones}")
            
            self.log("\n[2/10] Creando instancia del algoritmo genetico...")
            
            if self.datos_vigilantes:
                self.log(f"  Usando datos de {len(self.datos_vigilantes)} vigilantes del CSV")
            
            self.ag = AlgoritmoGenetico(
                num_vigilantes=num_vigilantes,
                num_dias=num_dias,
                num_turnos=num_turnos,
                num_puestos=num_puestos,
                tam_poblacion=tam_poblacion,
                prob_cruza=prob_cruza,
                prob_mutacion_individuo=prob_mutacion,
                prob_mutacion_gen=0.25,
                max_generaciones=max_generaciones,
                horas_max=horas_max,
                max_turnos_nocturnos=max_turnos_nocturnos,
                datos_vigilantes=self.datos_vigilantes if self.datos_vigilantes else None
            )
            
            self.log("  Algoritmo creado correctamente")
            self.log(f"  Longitud cromosoma: {self.ag.longitud_cromosoma} genes")
            
            self.log("\n[3/10] Ejecutando algoritmo genetico...")
            self.log("  (Esto puede tomar varios minutos...)")
            
            (top_1_global, top_1_fitness, 
             top_2_global, top_2_fitness, 
             top_3_global, top_3_fitness, 
             peor_global, peor_fitness, 
             historial, poblacion_final, aptitudes_finales) = self.ag.ejecutar()
            
            self.log("\n[4/10] Algoritmo finalizado")
            self.log(f"  Top 1 Global: {top_1_fitness:.4f}")
            self.log(f"  Top 2 Global: {top_2_fitness:.4f}")
            self.log(f"  Top 3 Global: {top_3_fitness:.4f}")
            self.log(f"  Peor Global: {peor_fitness:.4f}")
            
            self.log("\n[5/10] Calculando metricas...")
            CT = self.ag.calcular_cobertura_turnos(top_1_global)
            HE = self.ag.calcular_horas_extra(top_1_global)
            BCL = self.ag.calcular_balance_carga_laboral(top_1_global)
            VL, _ = self.ag.calcular_violaciones(top_1_global)
            
            self.log(f"  Cobertura: {CT:.2%}")
            self.log(f"  Horas extra: {HE:.1f}")
            self.log(f"  Balance: {BCL:.1f}")
            self.log(f"  Violaciones: {int(VL)}")
            
            self.log("\n[6/10] Actualizando interfaz...")
            self.root.after(0, self.mostrar_resultados, 
                          top_1_global, top_1_fitness,
                          top_2_global, top_2_fitness,
                          top_3_global, top_3_fitness,
                          peor_global, peor_fitness,
                          historial, poblacion_final, aptitudes_finales)
            
            self.log("\n" + "="*60)
            self.log("PROCESO COMPLETADO EXITOSAMENTE")
            self.log("="*60)
            
        except Exception as e:
            import traceback
            error_completo = traceback.format_exc()
            self.log(f"\n\nERROR DETALLADO:")
            self.log("="*60)
            self.log(error_completo)
            self.log("="*60)
            messagebox.showerror("Error", f"Error al ejecutar el algoritmo:\n\n{str(e)}\n\nRevisa la consola para mas detalles")
        finally:
            self.ejecutando = False
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.btn_ejecutar_todo.config(state=tk.NORMAL))
    
    def mostrar_resultados(self, top_1_global, top_1_fitness, 
                          top_2_global, top_2_fitness,
                          top_3_global, top_3_fitness,
                          peor_global, peor_fitness,
                          historial, poblacion_final, aptitudes_finales):
        try:
            self.log("\n[7/10] Calculando metricas del MEJOR GLOBAL...")
            
            # CORRECCION: Usar el Top 1 GLOBAL (de todas las generaciones)
            CT = self.ag.calcular_cobertura_turnos(top_1_global)
            HE = self.ag.calcular_horas_extra(top_1_global)
            BCL = self.ag.calcular_balance_carga_laboral(top_1_global)
            VL, _ = self.ag.calcular_violaciones(top_1_global)
            
            self.log(f"  Mejor fitness GLOBAL: {top_1_fitness:.4f}")
            
            self.log("\n[8/10] Actualizando metricas en interfaz...")
            self.labels_metricas['fitness'].config(text=f"{top_1_fitness:.4f}")
            self.labels_metricas['cobertura'].config(text=f"{CT:.2%}")
            self.labels_metricas['horas_extra'].config(text=f"{HE:.1f} hrs")
            self.labels_metricas['balance'].config(text=f"{BCL:.1f} hrs")
            self.labels_metricas['violaciones'].config(text=f"{int(VL)}")
            
            self.log("\n[9/10] Generando grafica de evolucion...")
            self.ax.clear()
            
            # Crear lista de generaciones como enteros (0, 1, 2, 3, ...)
            generaciones = list(range(len(historial)))
            
            self.ax.plot(generaciones, historial, linewidth=2, color='#2E86AB', marker='o', markersize=4)
            self.ax.set_title('Evolucion del Fitness (Mejor por Generacion)', fontsize=14, fontweight='bold')
            self.ax.set_xlabel('Generacion', fontsize=12)
            self.ax.set_ylabel('Fitness', fontsize=12)
            self.ax.set_ylim([0, 1.05])
            self.ax.grid(True, alpha=0.3, linestyle='--')
            
            # CORRECCION: Forzar que el eje X muestre solo enteros
            from matplotlib.ticker import MaxNLocator
            self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            
            # Guardar limites originales para zoom
            self.xlim_original = self.ax.get_xlim()
            self.ylim_original = self.ax.get_ylim()
            
            self.canvas.draw()
            
            self.log(f"\n[10/10] Seleccionando los 4 mejores GLOBALES...")
            
            # CORRECCION: TODOS son GLOBALES (guardados durante la ejecucion)
            soluciones = [
                ('Top 1', top_1_global, top_1_fitness),
                ('Top 2', top_2_global, top_2_fitness),
                ('Top 3', top_3_global, top_3_fitness),
                ('Peor', peor_global, peor_fitness)
            ]
            
            self.log(f"  Top 1 (GLOBAL): {top_1_fitness:.4f}")
            self.log(f"  Top 2 (GLOBAL): {top_2_fitness:.4f}")
            self.log(f"  Top 3 (GLOBAL): {top_3_fitness:.4f}")
            self.log(f"  Peor (GLOBAL): {peor_fitness:.4f}")
            
            self.log(f"  Generando horarios detallados...")
            for nombre, cromosoma, fitness in soluciones:
                tab_info = self.tabs_horarios[nombre]
                
                if fitness >= 0.9:
                    calidad = "EXCELENTE"
                    color_calidad = '#27ae60'
                elif fitness >= 0.7:
                    calidad = "BUENA"
                    color_calidad = '#f39c12'
                else:
                    calidad = "MEJORABLE"
                    color_calidad = '#e74c3c'
                
                tab_info['fitness_label'].config(text=f"Fitness: {fitness:.4f}")
                tab_info['calidad_label'].config(text=f"Calidad: {calidad}", fg=color_calidad)
                
                self.generar_horario_texto(cromosoma, tab_info['frame'], fitness, nombre)
            
            self.log("\nResultados actualizados correctamente en todas las pestañas")
            
        except Exception as e:
            import traceback
            error_completo = traceback.format_exc()
            self.log(f"\n\nERROR EN MOSTRAR_RESULTADOS:")
            self.log("="*60)
            self.log(error_completo)
            self.log("="*60)
            raise
    
    def generar_horario_texto(self, cromosoma, frame_horario, fitness, nombre_tab=""):
        for widget in frame_horario.winfo_children():
            widget.destroy()
        
        style = ttk.Style()
        style.theme_use('clam')  # Usar tema clam para mejor control de colores
        style.configure("Horario.Treeview", 
                       rowheight=30, 
                       font=('Arial', 9, 'bold'),
                       foreground='#000000',
                       background='white',
                       fieldbackground='white',
                       borderwidth=0)
        style.configure("Horario.Treeview.Heading", 
                       font=('Arial', 10, 'bold'),
                       background='#e8e8e8',
                       foreground='#000000',
                       borderwidth=0,
                       relief='flat')
        
        style.map('Horario.Treeview',
                 foreground=[('selected', '#000000'), ('!selected', '#000000')],
                 background=[('selected', '#e8e8e8')])
        
        nombres_puestos_completos = []
        for i in range(self.ag.num_puestos):
            if i < len(self.ag.nombres_puestos):
                nombres_puestos_completos.append(self.ag.nombres_puestos[i])
            else:
                nombres_puestos_completos.append(f"Puesto {i+1}")
        
        columnas = ['Dia', 'Turno', 'Horario'] + nombres_puestos_completos
        
        tree = ttk.Treeview(frame_horario, columns=columnas, show='headings', 
                           style="Horario.Treeview", height=14)
        
        tree.heading('Dia', text='Día')
        tree.column('Dia', width=90, anchor='center', minwidth=80, stretch=True)
        
        tree.heading('Turno', text='Turno')
        tree.column('Turno', width=80, anchor='center', minwidth=70, stretch=True)
        
        tree.heading('Horario', text='Horario')
        tree.column('Horario', width=110, anchor='center', minwidth=100, stretch=True)
        
        # Calcular ancho para cada puesto - distribuir el espacio restante equitativamente
        ancho_puesto = max(140, int(600 / len(nombres_puestos_completos)))
        
        for puesto in nombres_puestos_completos:
            tree.heading(puesto, text=puesto)
            tree.column(puesto, width=ancho_puesto, anchor='center', minwidth=120, stretch=True)
        
        scrollbar_y = ttk.Scrollbar(frame_horario, orient=tk.VERTICAL, command=tree.yview)
        scrollbar_x = ttk.Scrollbar(frame_horario, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for dia in range(self.ag.num_dias):
            nombre_dia = self.ag.nombres_dias[dia]
            
            for turno in range(self.ag.num_turnos):
                turno_nombre = "Día" if turno == 0 else "Noche"
                horario = "08:00 - 20:00" if turno == 0 else "20:00 - 08:00"
                
                valores = [nombre_dia, turno_nombre, horario]
                
                for puesto in range(self.ag.num_puestos):
                    idx = dia * (self.ag.num_turnos * self.ag.num_puestos) + \
                          turno * self.ag.num_puestos + puesto
                    vigilante = cromosoma[idx]
                    nombre_vigilante = self.ag.obtener_nombre_vigilante(vigilante)
                    valores.append(nombre_vigilante)
                
                tag = 'dia' if turno == 0 else 'noche'
                tree.insert('', 'end', values=valores, tags=(tag,))
        
        tree.tag_configure('dia', background='#FFF8DC', foreground='#000000')
        tree.tag_configure('noche', background='#D3D3D3', foreground='#000000')
        
        # CALCULAR DATOS PARA EL RESUMEN
        horas = self.ag.calcular_horas_trabajadas(cromosoma)
        nocturnos = self.ag.calcular_turnos_nocturnos(cromosoma)
        HE = self.ag.calcular_horas_extra(cromosoma)
        BCL = self.ag.calcular_balance_carga_laboral(cromosoma)
        VL, _ = self.ag.calcular_violaciones(cromosoma)
        CT = self.ag.calcular_cobertura_turnos(cromosoma)
        
        # Calcular turnos y pagos por vigilante para el resumen
        try:
            pago_por_turno = float(self.entry_pago_dia.get())
            pago_domingo = float(self.entry_pago_domingo.get())
            pago_turno_extra = float(self.entry_pago_dia_extra.get())
        except:
            pago_por_turno = 316
            pago_domingo = 632
            pago_turno_extra = 632
        
        turnos_por_vigilante_por_dia = {}
        turnos_dia_total = 0
        turnos_noche_total = 0
        vigilantes_usados = set()
        
        for dia in range(self.ag.num_dias):
            for turno in range(self.ag.num_turnos):
                for puesto in range(self.ag.num_puestos):
                    idx = dia * (self.ag.num_turnos * self.ag.num_puestos) + turno * self.ag.num_puestos + puesto
                    vigilante = cromosoma[idx]
                    vigilantes_usados.add(vigilante)
                    
                    if vigilante not in turnos_por_vigilante_por_dia:
                        turnos_por_vigilante_por_dia[vigilante] = {}
                    
                    if dia not in turnos_por_vigilante_por_dia[vigilante]:
                        turnos_por_vigilante_por_dia[vigilante][dia] = 0
                    
                    turnos_por_vigilante_por_dia[vigilante][dia] += 1
                    
                    if turno == 0:
                        turnos_dia_total += 1
                    else:
                        turnos_noche_total += 1
        
        # Calcular pagos por vigilante
        # Calcular datos adicionales para el resumen
        turnos_por_vigilante_dia = {}
        turnos_por_vigilante_noche = {}
        dias_trabajados_por_vigilante = {}
        turnos_domingo_por_vigilante = {}
        
        for vigilante in vigilantes_usados:
            turnos_por_vigilante_dia[vigilante] = 0
            turnos_por_vigilante_noche[vigilante] = 0
            dias_trabajados_por_vigilante[vigilante] = set()
            turnos_domingo_por_vigilante[vigilante] = 0
        
        for dia in range(self.ag.num_dias):
            for turno in range(self.ag.num_turnos):
                for puesto in range(self.ag.num_puestos):
                    idx = dia * (self.ag.num_turnos * self.ag.num_puestos) + turno * self.ag.num_puestos + puesto
                    vigilante = cromosoma[idx]
                    
                    dias_trabajados_por_vigilante[vigilante].add(dia)
                    
                    if turno == 0:
                        turnos_por_vigilante_dia[vigilante] += 1
                    else:
                        turnos_por_vigilante_noche[vigilante] += 1
                    
                    if dia == 6:  # Domingo
                        turnos_domingo_por_vigilante[vigilante] += 1
        
        # Calcular pagos
        pagos_por_vigilante = {}
        for vigilante in vigilantes_usados:
            pago_normal = 0
            pago_dom = 0
            pago_extra = 0
            
            for dia, num_turnos in turnos_por_vigilante_por_dia[vigilante].items():
                if dia == 6:  # Domingo
                    pago_dom += num_turnos * pago_domingo
                else:
                    pago_normal += min(1, num_turnos) * pago_por_turno
                    if num_turnos > 1:
                        pago_extra += (num_turnos - 1) * pago_turno_extra
            
            pago_total = pago_normal + pago_dom + pago_extra
            nombre = self.ag.obtener_nombre_vigilante(vigilante)
            pagos_por_vigilante[nombre] = pago_total
        
        # RESUMEN GENERAL DEBAJO DE LA TABLA - Con ancho máximo
        frame_resumen_container = tk.Frame(frame_horario, bg='white')
        frame_resumen_container.pack(fill=tk.X, padx=5, pady=5)
        
        frame_resumen = tk.Frame(frame_resumen_container, bg='#f0f0f0', relief=tk.RAISED, borderwidth=2)
        frame_resumen.pack(fill=tk.X, padx=0, pady=0)
        
        # El resumen ahora ocupa todo el ancho disponible
        
        tk.Label(frame_resumen, text="RESUMEN DETALLADO DEL HORARIO", 
                font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='black').pack(pady=5)
        
        # Frame para los totales generales - Layout en 3 columnas
        frame_totales_generales = tk.Frame(frame_resumen, bg='#f0f0f0')
        frame_totales_generales.pack(fill=tk.X, padx=8, pady=3)
        
        # Calcular promedios
        promedio_turnos = (turnos_dia_total + turnos_noche_total) / len(vigilantes_usados) if vigilantes_usados else 0
        promedio_dias = sum(len(dias) for dias in dias_trabajados_por_vigilante.values()) / len(vigilantes_usados) if vigilantes_usados else 0
        
        info_general = [
            ("Turnos día:", f"{turnos_dia_total}"),
            ("Turnos noche:", f"{turnos_noche_total}"),
            ("Total turnos:", f"{turnos_dia_total + turnos_noche_total}"),
            ("Vigilantes:", f"{len(vigilantes_usados)}"),
            ("Promedio turnos/vigilante:", f"{promedio_turnos:.1f}"),
            ("Promedio días/vigilante:", f"{promedio_dias:.1f}")
        ]
        
        # Crear 3 columnas para los totales
        frame_col1 = tk.Frame(frame_totales_generales, bg='#f0f0f0')
        frame_col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        
        frame_col2 = tk.Frame(frame_totales_generales, bg='#f0f0f0')
        frame_col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        
        frame_col3 = tk.Frame(frame_totales_generales, bg='#f0f0f0')
        frame_col3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        
        for i, (etiqueta, valor) in enumerate(info_general):
            if i < 2:
                parent_frame = frame_col1
            elif i < 4:
                parent_frame = frame_col2
            else:
                parent_frame = frame_col3
            
            frame_fila = tk.Frame(parent_frame, bg='white', relief=tk.FLAT, borderwidth=1)
            frame_fila.pack(fill=tk.X, pady=1)
            
            tk.Label(frame_fila, text=f"{etiqueta} {valor}", font=('Arial', 8), 
                    bg='white', fg='black', anchor='w').pack(padx=5, pady=2)
        
        # Separador
        tk.Label(frame_resumen, text="", bg='#f0f0f0').pack(pady=2)
        
        # Pagos por vigilante - Layout más compacto con más detalles
        tk.Label(frame_resumen, text="DETALLE POR VIGILANTE", 
                font=('Arial', 9, 'bold'), bg='#f0f0f0', fg='black').pack(pady=3)
        
        frame_pagos = tk.Frame(frame_resumen, bg='#f0f0f0')
        frame_pagos.pack(fill=tk.X, padx=8, pady=3)
        
        # Crear 2 columnas para los pagos
        frame_pago_col1 = tk.Frame(frame_pagos, bg='#f0f0f0')
        frame_pago_col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        
        frame_pago_col2 = tk.Frame(frame_pagos, bg='#f0f0f0')
        frame_pago_col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        
        total_general = 0
        vigilantes_lista = sorted(pagos_por_vigilante.keys())
        
        for i, nombre in enumerate(vigilantes_lista):
            pago = pagos_por_vigilante[nombre]
            total_general += pago
            
            # Buscar el vigilante ID por nombre
            vigilante_id = None
            for v_id in vigilantes_usados:
                if self.ag.obtener_nombre_vigilante(v_id) == nombre:
                    vigilante_id = v_id
                    break
            
            if vigilante_id is not None:
                t_dia = turnos_por_vigilante_dia[vigilante_id]
                t_noche = turnos_por_vigilante_noche[vigilante_id]
                dias_trab = len(dias_trabajados_por_vigilante[vigilante_id])
                t_domingo = turnos_domingo_por_vigilante[vigilante_id]
            else:
                t_dia = t_noche = dias_trab = t_domingo = 0
            
            parent_frame = frame_pago_col1 if i % 2 == 0 else frame_pago_col2
            
            frame_fila_pago = tk.Frame(parent_frame, bg='white', relief=tk.SOLID, borderwidth=1)
            frame_fila_pago.pack(fill=tk.X, pady=2)
            
            tk.Label(frame_fila_pago, text=nombre, font=('Arial', 8, 'bold'), 
                    bg='white', fg='black', anchor='w').pack(padx=5, pady=1)
            
            detalles = f"  Día: {t_dia} | Noche: {t_noche} | Días: {dias_trab}"
            if t_domingo > 0:
                detalles += f" | Dom: {t_domingo}"
            
            tk.Label(frame_fila_pago, text=detalles, font=('Arial', 7), 
                    bg='white', fg='#555', anchor='w').pack(padx=5, pady=0)
            
            tk.Label(frame_fila_pago, text=f"Pago: ${pago:,.0f}", font=('Arial', 8, 'bold'), 
                    bg='white', fg='#1565c0', anchor='w').pack(padx=5, pady=1)
        
        # Total general
        frame_total_final = tk.Frame(frame_resumen, bg='#1565c0', relief=tk.RAISED, borderwidth=2)
        frame_total_final.pack(fill=tk.X, padx=8, pady=5)
        
        tk.Label(frame_total_final, text=f"TOTAL: ${total_general:,.0f}", 
                font=('Arial', 9, 'bold'), bg='#1565c0', fg='white').pack(pady=4)
    
    def calcular_costos(self):
        if self.ag is None:
            messagebox.showwarning("Advertencia", "Primero debes ejecutar el algoritmo")
            return
        
        try:
            pago_por_turno = float(self.entry_pago_dia.get())
            pago_domingo = float(self.entry_pago_domingo.get())
            pago_turno_extra = float(self.entry_pago_dia_extra.get())
            
            mejores_indices = self.ag.seleccionar_mejores(self.ag.poblacion_final, self.ag.aptitudes_finales, 1)
            mejor_cromosoma = self.ag.poblacion_final[mejores_indices[0]]
            
            horas = self.ag.calcular_horas_trabajadas(mejor_cromosoma)
            
            turnos_por_vigilante_por_dia = {}
            turnos_dia_por_vigilante = {}
            turnos_noche_por_vigilante = {}
            turnos_domingo_por_vigilante = {}
            dias_trabajados_por_vigilante = {}
            
            for dia in range(self.ag.num_dias):
                for turno in range(self.ag.num_turnos):
                    for puesto in range(self.ag.num_puestos):
                        idx = dia * (self.ag.num_turnos * self.ag.num_puestos) + turno * self.ag.num_puestos + puesto
                        vigilante = mejor_cromosoma[idx]
                        
                        if vigilante not in turnos_por_vigilante_por_dia:
                            turnos_por_vigilante_por_dia[vigilante] = {}
                            turnos_dia_por_vigilante[vigilante] = 0
                            turnos_noche_por_vigilante[vigilante] = 0
                            turnos_domingo_por_vigilante[vigilante] = 0
                            dias_trabajados_por_vigilante[vigilante] = set()
                        
                        if dia not in turnos_por_vigilante_por_dia[vigilante]:
                            turnos_por_vigilante_por_dia[vigilante][dia] = 0
                        
                        turnos_por_vigilante_por_dia[vigilante][dia] += 1
                        dias_trabajados_por_vigilante[vigilante].add(self.ag.nombres_dias[dia])
                        
                        if dia == 6:
                            turnos_domingo_por_vigilante[vigilante] += 1
                        
                        if turno == 0:
                            turnos_dia_por_vigilante[vigilante] += 1
                        else:
                            turnos_noche_por_vigilante[vigilante] += 1
            
            self.text_costos.delete(1.0, tk.END)
            self.text_costos.insert(tk.END, "="*120 + "\n")
            self.text_costos.insert(tk.END, "CALCULO DE COSTOS Y SUELDOS - MEJOR SOLUCION\n")
            self.text_costos.insert(tk.END, "="*120 + "\n\n")
            
            self.text_costos.insert(tk.END, "REGLAS DE PAGO:\n")
            self.text_costos.insert(tk.END, f"  - Pago por turno (Lun-Sab): ${pago_por_turno:.2f} MXN\n")
            self.text_costos.insert(tk.END, f"  - Pago turno Domingo: ${pago_domingo:.2f} MXN (doble)\n")
            self.text_costos.insert(tk.END, f"  - Pago 2do turno mismo dia: ${pago_turno_extra:.2f} MXN (extra)\n")
            self.text_costos.insert(tk.END, f"  - Semanal normal: 1 turno/dia x 7 dias = 7 turnos\n\n")
            
            self.text_costos.insert(tk.END, "-"*120 + "\n")
            self.text_costos.insert(tk.END, f"{'Vigilante':<20} {'Hrs':>6} {'Dia':>4} {'Noc':>4} {'Dom':>4} {'Tot':>4} {'$Normal':>10} {'$Dom':>10} {'$Extra':>10} {'Total':>10} {'Estado':>12}\n")
            self.text_costos.insert(tk.END, "-"*120 + "\n")
            
            total_turnos = 0
            total_turnos_dia = 0
            total_turnos_noche = 0
            total_turnos_domingo = 0
            total_costo_normal = 0
            total_costo_domingo = 0
            total_costo_extra = 0
            sueldo_minimo_semanal = 2396.0
            vigilantes_bajo_minimo = []
            
            for i in range(1, self.ag.num_vigilantes + 1):
                hrs_trabajadas = horas[i-1] if i-1 < len(horas) else 0
                turnos_dia = turnos_dia_por_vigilante.get(i, 0)
                turnos_noche = turnos_noche_por_vigilante.get(i, 0)
                turnos_domingo = turnos_domingo_por_vigilante.get(i, 0)
                turnos_totales = turnos_dia + turnos_noche
                
                turnos_por_dia_dict = turnos_por_vigilante_por_dia.get(i, {})
                
                costo_normal = 0
                costo_domingo_pago = 0
                costo_extra = 0
                
                for dia, num_turnos_dia in turnos_por_dia_dict.items():
                    if dia == 6:
                        costo_domingo_pago += num_turnos_dia * pago_domingo
                    else:
                        if num_turnos_dia == 1:
                            costo_normal += pago_por_turno
                        elif num_turnos_dia > 1:
                            costo_normal += pago_por_turno
                            costo_extra += (num_turnos_dia - 1) * pago_turno_extra
                
                costo_total = costo_normal + costo_domingo_pago + costo_extra
                
                total_turnos += turnos_totales
                total_turnos_dia += turnos_dia
                total_turnos_noche += turnos_noche
                total_turnos_domingo += turnos_domingo
                total_costo_normal += costo_normal
                total_costo_domingo += costo_domingo_pago
                total_costo_extra += costo_extra
                
                nombre_vigilante = self.ag.obtener_nombre_vigilante(i)
                
                estado = "OK"
                if costo_total < sueldo_minimo_semanal:
                    estado = "BAJO MINIMO"
                    vigilantes_bajo_minimo.append((nombre_vigilante, costo_total))
                
                self.text_costos.insert(tk.END, 
                    f"{nombre_vigilante:<20} {hrs_trabajadas:6.1f} {turnos_dia:4d} {turnos_noche:4d} {turnos_domingo:4d} {turnos_totales:4d} "
                    f"${costo_normal:9.2f} ${costo_domingo_pago:9.2f} ${costo_extra:9.2f} ${costo_total:9.2f} {estado:>12}\n")
                
                dias_trabajados = dias_trabajados_por_vigilante.get(i, set())
                if dias_trabajados:
                    dias_str = ", ".join(sorted(dias_trabajados, key=lambda x: self.ag.nombres_dias.index(x)))
                    self.text_costos.insert(tk.END, f"  Dias: {dias_str}\n")
                
                turnos_multiples = [f"{self.ag.nombres_dias[d]}({n})" for d, n in turnos_por_dia_dict.items() if n > 1]
                if turnos_multiples:
                    self.text_costos.insert(tk.END, f"  Turnos multiples: {', '.join(turnos_multiples)}\n")
            
            self.text_costos.insert(tk.END, "="*120 + "\n")
            self.text_costos.insert(tk.END, 
                f"{'TOTAL':<20} {'':>6} {total_turnos_dia:4d} {total_turnos_noche:4d} {total_turnos_domingo:4d} {total_turnos:4d} "
                f"${total_costo_normal:9.2f} ${total_costo_domingo:9.2f} ${total_costo_extra:9.2f} ${total_costo_normal+total_costo_domingo+total_costo_extra:9.2f}\n")
            self.text_costos.insert(tk.END, "="*120 + "\n\n")
            
            self.text_costos.insert(tk.END, "RESUMEN:\n")
            self.text_costos.insert(tk.END, f"  Total vigilantes:       {self.ag.num_vigilantes}\n")
            self.text_costos.insert(tk.END, f"  Total turnos dia:       {total_turnos_dia}\n")
            self.text_costos.insert(tk.END, f"  Total turnos noche:     {total_turnos_noche}\n")
            self.text_costos.insert(tk.END, f"  Total turnos domingo:   {total_turnos_domingo}\n")
            self.text_costos.insert(tk.END, f"  Total turnos:           {total_turnos}\n")
            self.text_costos.insert(tk.END, f"  Costo turnos normales:  ${total_costo_normal:,.2f} MXN (Lun-Sab)\n")
            self.text_costos.insert(tk.END, f"  Costo turnos domingo:   ${total_costo_domingo:,.2f} MXN (doble)\n")
            self.text_costos.insert(tk.END, f"  Costo turnos extras:    ${total_costo_extra:,.2f} MXN (2do turno/dia)\n")
            self.text_costos.insert(tk.END, f"  Costo total semanal:    ${total_costo_normal+total_costo_domingo+total_costo_extra:,.2f} MXN\n")
            self.text_costos.insert(tk.END, f"  Costo mensual (x4):     ${(total_costo_normal+total_costo_domingo+total_costo_extra)*4:,.2f} MXN\n\n")
            
            self.text_costos.insert(tk.END, "VALIDACION SUELDO MINIMO:\n")
            self.text_costos.insert(tk.END, f"  Sueldo minimo semanal:  ${sueldo_minimo_semanal:,.2f} MXN\n")
            if vigilantes_bajo_minimo:
                self.text_costos.insert(tk.END, f"  ALERTA: {len(vigilantes_bajo_minimo)} vigilante(s) bajo el minimo:\n")
                for nombre, sueldo in vigilantes_bajo_minimo:
                    faltante = sueldo_minimo_semanal - sueldo
                    self.text_costos.insert(tk.END, f"    - {nombre}: ${sueldo:.2f} (Falta: ${faltante:.2f})\n")
                messagebox.showwarning("Alerta Sueldo Minimo", 
                    f"ATENCION: {len(vigilantes_bajo_minimo)} vigilante(s) ganan menos del minimo semanal de ${sueldo_minimo_semanal:,.2f} MXN\n\n"
                    f"Revisa la pestaña 'Costos y Sueldos' para mas detalles.")
            else:
                self.text_costos.insert(tk.END, f"  Estado: TODOS los vigilantes cumplen el minimo\n")
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numericos validos para los pagos")
    
    def cargar_restricciones(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de restricciones CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir="base_conocimientos",
            initialfile="restricciones.csv"
        )
        
        if not archivo:
            return
        
        try:
            import csv
            
            nombre_archivo = os.path.basename(archivo)
            
            self.log(f"\n{'='*60}")
            self.log(f"CARGANDO RESTRICCIONES: {nombre_archivo}")
            self.log(f"{'='*60}\n")
            
            with open(archivo, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                filas = list(reader)
            
            self.datos_restricciones = []
            headers = filas[0] if len(filas) > 0 else []
            
            self.log(f"Total restricciones: {len(filas)-1}\n")
            self.log("Restricciones cargadas:\n")
            
            for i, fila in enumerate(filas):
                if i == 0:
                    self.log(f"  {', '.join(fila)}")
                    self.log("  " + "-"*50)
                elif i >= 1:
                    restriccion_dict = {}
                    for j, header in enumerate(headers):
                        if j < len(fila):
                            restriccion_dict[header] = fila[j]
                    self.datos_restricciones.append(restriccion_dict)
                    
                    if i <= 10:
                        tipo = restriccion_dict.get('Tipo', '')
                        desc = restriccion_dict.get('Descripcion', '')
                        valor = restriccion_dict.get('Valor', '')
                        self.log(f"  {tipo}: {desc} = {valor}")
            
            if len(filas) > 11:
                self.log(f"  ... y {len(filas)-11} mas")
            
            for restriccion in self.datos_restricciones:
                tipo = restriccion.get('Tipo', '').upper()
                desc = restriccion.get('Descripcion', '').lower()
                valor = restriccion.get('Valor', '')
                
                try:
                    if tipo == 'RESTRICCION':
                        if 'horas' in desc and 'maximas' in desc:
                            self.entries['horas_max'].delete(0, tk.END)
                            self.entries['horas_max'].insert(0, valor)
                            self.log(f"\n  Horas maximas actualizado: {valor}")
                        
                        elif 'turnos nocturnos' in desc:
                            self.entries['max_turnos_nocturnos'].delete(0, tk.END)
                            self.entries['max_turnos_nocturnos'].insert(0, valor)
                            self.log(f"  Max turnos nocturnos actualizado: {valor}")
                    
                    elif tipo == 'CONFIGURACION':
                        if 'poblacion' in desc and 'maxima' in desc:
                            pass
                        elif 'generaciones' in desc and 'recomendadas' in desc:
                            self.entries['max_generaciones'].delete(0, tk.END)
                            self.entries['max_generaciones'].insert(0, valor)
                            self.log(f"  Max generaciones actualizado: {valor}")
                        elif 'probabilidad cruza' in desc:
                            self.entries['prob_cruza'].delete(0, tk.END)
                            self.entries['prob_cruza'].insert(0, valor)
                            self.log(f"  Probabilidad cruza actualizado: {valor}")
                        elif 'probabilidad mutacion' in desc:
                            self.entries['prob_mutacion'].delete(0, tk.END)
                            self.entries['prob_mutacion'].insert(0, valor)
                            self.log(f"  Probabilidad mutacion actualizado: {valor}")
                    
                    elif tipo == 'SUELDO':
                        if 'turno' in desc and 'lunes' in desc.lower() or ('turno' in desc and 'sabado' in desc.lower()):
                            self.entry_pago_dia.delete(0, tk.END)
                            self.entry_pago_dia.insert(0, valor)
                            self.log(f"  Pago por turno (Lun-Sab) actualizado: {valor}")
                        elif 'domingo' in desc.lower():
                            self.entry_pago_domingo.delete(0, tk.END)
                            self.entry_pago_domingo.insert(0, valor)
                            self.log(f"  Pago turno Domingo actualizado: {valor}")
                        elif 'segundo' in desc.lower() or 'mismo dia' in desc.lower():
                            self.entry_pago_dia_extra.delete(0, tk.END)
                            self.entry_pago_dia_extra.insert(0, valor)
                            self.log(f"  Pago 2do turno actualizado: {valor}")
                
                except Exception as e:
                    self.log(f"  Error al aplicar restriccion: {str(e)}")
            
            self.log(f"\n{'='*60}")
            self.log("RESTRICCIONES CARGADAS Y APLICADAS")
            self.log(f"{'='*60}\n")
            
            # Actualizar el text widget de restricciones en el panel de configuracion
            self.actualizar_text_restricciones_config(filas)
            
            messagebox.showinfo("Exito", 
                f"Restricciones cargadas correctamente:\n\n{nombre_archivo}\n\n"
                f"Total restricciones: {len(filas)-1}\n"
                f"Parametros actualizados automaticamente")
            
        except Exception as e:
            import traceback
            error_completo = traceback.format_exc()
            self.log(f"\nERROR al cargar restricciones:")
            self.log("="*60)
            self.log(error_completo)
            self.log("="*60)
            messagebox.showerror("Error", f"Error al cargar restricciones:\n{str(e)}")
    
    def actualizar_text_restricciones_config(self, filas):
        """Actualiza el text widget de restricciones en el panel de configuracion"""
        try:
            self.text_restricciones_config.config(state=tk.NORMAL)
            self.text_restricciones_config.delete(1.0, tk.END)
            
            # Mostrar contenido del CSV
            texto = "RESTRICCIONES CARGADAS DESDE CSV\n"
            texto += "="*80 + "\n\n"
            
            for i, fila in enumerate(filas):
                if i == 0:
                    # Headers
                    texto += " | ".join(f"{col:20}" for col in fila) + "\n"
                    texto += "-"*80 + "\n"
                else:
                    # Datos
                    texto += " | ".join(f"{col:20}" for col in fila) + "\n"
            
            texto += "\n" + "="*80 + "\n"
            texto += f"Total: {len(filas)-1} restricciones cargadas\n"
            
            self.text_restricciones_config.insert(1.0, texto)
            self.text_restricciones_config.config(state=tk.DISABLED)
            
        except Exception as e:
            self.log(f"Error al actualizar text restricciones: {str(e)}")
    
    def exportar_excel(self):
        if self.ag is None:
            messagebox.showwarning("Advertencia", "Primero debes ejecutar el algoritmo")
            return
        
        try:
            archivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile="resultados_ag.xlsx"
            )
            
            if archivo:
                self.log("\nGenerando archivo Excel...")
                
                mejor_idx = self.ag.seleccionar_mejores(
                    self.ag.poblacion_final, 
                    self.ag.aptitudes_finales, 
                    n=3
                )
                
                poblacion_top = [self.ag.poblacion_final[i] for i in mejor_idx]
                aptitudes_top = [self.ag.aptitudes_finales[i] for i in mejor_idx]
                
                peor_idx = self.ag.seleccionar_peor(
                    self.ag.poblacion_final, 
                    self.ag.aptitudes_finales
                )
                
                poblacion_top.append(self.ag.poblacion_final[peor_idx])
                aptitudes_top.append(self.ag.aptitudes_finales[peor_idx])
                
                self.ag.exportar_excel(
                    poblacion_top,
                    aptitudes_top,
                    self.ag.historial,
                    archivo
                )
                
                self.log(f"Archivo Excel guardado: {archivo}")
                messagebox.showinfo("Exito", f"Archivo Excel exportado correctamente:\n{archivo}")
                
        except Exception as e:
            self.log(f"\nERROR al exportar: {str(e)}")
            messagebox.showerror("Error", f"Error al exportar Excel:\n{str(e)}")
    
    def seleccionar_archivo_vigilantes(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de vigilantes CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir="base_conocimientos",
            initialfile="vigilantes.csv"
        )
        
        if archivo:
            self.entry_archivo_vigilantes.delete(0, tk.END)
            self.entry_archivo_vigilantes.insert(0, archivo)
    
    def seleccionar_archivo_turnos(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de turnos CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir="base_conocimientos",
            initialfile="turnos.csv"
        )
        
        if archivo:
            self.entry_archivo_turnos.delete(0, tk.END)
            self.entry_archivo_turnos.insert(0, archivo)
    
    def seleccionar_archivo_puestos(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de puestos CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir="base_conocimientos",
            initialfile="puestos.csv"
        )
        
        if archivo:
            self.entry_archivo_puestos.delete(0, tk.END)
            self.entry_archivo_puestos.insert(0, archivo)
    
    def seleccionar_archivo_politicas(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de políticas CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir="base_conocimientos",
            initialfile="politicas_empresa.csv"
        )
        
        if archivo:
            self.entry_archivo_politicas.delete(0, tk.END)
            self.entry_archivo_politicas.insert(0, archivo)
    
    def seleccionar_archivo_normativas(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de normativas CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir="base_conocimientos",
            initialfile="normativas_laborales.csv"
        )
        
        if archivo:
            self.entry_archivo_normativas.delete(0, tk.END)
            self.entry_archivo_normativas.insert(0, archivo)
    
    def seleccionar_archivo_restricciones(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de restricciones CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir="base_conocimientos",
            initialfile="restricciones.csv"
        )
        
        if archivo:
            self.entry_archivo_restricciones.delete(0, tk.END)
            self.entry_archivo_restricciones.insert(0, archivo)
    
    def seleccionar_archivo_entradas(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de entradas del sistema CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir="base_conocimientos",
            initialfile="entradas_sistema.csv"
        )
        
        if archivo:
            self.entry_archivo_entradas.delete(0, tk.END)
            self.entry_archivo_entradas.insert(0, archivo)
    
    def cargar_y_ejecutar(self):
        # Obtener rutas de todos los archivos
        archivos = {
            'vigilantes': self.entry_archivo_vigilantes.get().strip(),
            'turnos': self.entry_archivo_turnos.get().strip(),
            'puestos': self.entry_archivo_puestos.get().strip(),
            'politicas': self.entry_archivo_politicas.get().strip(),
            'normativas': self.entry_archivo_normativas.get().strip(),
            'restricciones': self.entry_archivo_restricciones.get().strip(),
            'entradas': self.entry_archivo_entradas.get().strip()
        }
        
        # Validar que se hayan especificado TODOS los archivos (todos son obligatorios)
        nombres_archivos = {
            'vigilantes': 'Vigilantes',
            'turnos': 'Turnos',
            'puestos': 'Puestos',
            'politicas': 'Políticas Empresa',
            'normativas': 'Normativas Laborales',
            'restricciones': 'Restricciones',
            'entradas': 'Entradas Sistema'
        }
        
        for clave, nombre in nombres_archivos.items():
            if not archivos[clave]:
                messagebox.showerror("Error", f"Por favor especifica el archivo de {nombre}")
                return
            if not os.path.exists(archivos[clave]):
                messagebox.showerror("Error", f"El archivo de {nombre} no existe:\n{archivos[clave]}")
                return
        
        try:
            import csv
            
            self.log(f"\n{'='*70}")
            self.log(f"CARGANDO BASE DE CONOCIMIENTO")
            self.log(f"{'='*70}\n")
            
            # CARGAR VIGILANTES
            self.log(f"[1/6] VIGILANTES: {os.path.basename(archivos['vigilantes'])}")
            with open(archivos['vigilantes'], 'r', encoding='utf-8') as f:
                filas_vigilantes = list(csv.reader(f))
            
            self.datos_vigilantes = []
            headers = filas_vigilantes[0] if len(filas_vigilantes) > 0 else []
            
            for i, fila in enumerate(filas_vigilantes[1:], 1):
                vigilante_dict = {}
                for j, header in enumerate(headers):
                    if j < len(fila):
                        vigilante_dict[header] = fila[j]
                self.datos_vigilantes.append(vigilante_dict)
            
            num_vigilantes = len(filas_vigilantes) - 1
            self.entries['num_vigilantes'].delete(0, tk.END)
            self.entries['num_vigilantes'].insert(0, str(num_vigilantes))
            self.log(f"  ✓ {num_vigilantes} vigilantes cargados")
            
            # CARGAR TURNOS
            self.log(f"\n[2/6] TURNOS: {os.path.basename(archivos['turnos'])}")
            with open(archivos['turnos'], 'r', encoding='utf-8') as f:
                filas_turnos = list(csv.reader(f))
            
            self.datos_turnos = []
            headers_turnos = filas_turnos[0] if len(filas_turnos) > 0 else []
            
            for i, fila in enumerate(filas_turnos[1:], 1):
                turno_dict = {}
                for j, header in enumerate(headers_turnos):
                    if j < len(fila):
                        turno_dict[header] = fila[j]
                self.datos_turnos.append(turno_dict)
            
            num_turnos = len(filas_turnos) - 1
            self.entries['num_turnos'].delete(0, tk.END)
            self.entries['num_turnos'].insert(0, str(num_turnos))
            self.log(f"  ✓ {num_turnos} turnos cargados")
            
            # CARGAR PUESTOS
            self.log(f"\n[3/6] PUESTOS: {os.path.basename(archivos['puestos'])}")
            with open(archivos['puestos'], 'r', encoding='utf-8') as f:
                filas_puestos = list(csv.reader(f))
            
            self.datos_puestos = []
            headers_puestos = filas_puestos[0] if len(filas_puestos) > 0 else []
            
            for i, fila in enumerate(filas_puestos[1:], 1):
                puesto_dict = {}
                for j, header in enumerate(headers_puestos):
                    if j < len(fila):
                        puesto_dict[header] = fila[j]
                self.datos_puestos.append(puesto_dict)
            
            num_puestos = len(filas_puestos) - 1
            self.entries['num_puestos'].delete(0, tk.END)
            self.entries['num_puestos'].insert(0, str(num_puestos))
            self.log(f"  ✓ {num_puestos} puestos cargados")
            
            # CARGAR POLITICAS (ahora obligatorio)
            self.log(f"\n[4/7] POLITICAS: {os.path.basename(archivos['politicas'])}")
            with open(archivos['politicas'], 'r', encoding='utf-8') as f:
                filas_politicas = list(csv.reader(f))
            
            self.datos_politicas = []
            headers_politicas = filas_politicas[0] if len(filas_politicas) > 0 else []
            
            for i, fila in enumerate(filas_politicas[1:], 1):
                politica_dict = {}
                for j, header in enumerate(headers_politicas):
                    if j < len(fila):
                        politica_dict[header] = fila[j]
                self.datos_politicas.append(politica_dict)
            
            self.log(f"  ✓ {len(filas_politicas)-1} políticas cargadas")
            
            # CARGAR NORMATIVAS (ahora obligatorio)
            self.log(f"\n[5/7] NORMATIVAS: {os.path.basename(archivos['normativas'])}")
            with open(archivos['normativas'], 'r', encoding='utf-8') as f:
                filas_normativas = list(csv.reader(f))
            
            self.datos_normativas = []
            headers_normativas = filas_normativas[0] if len(filas_normativas) > 0 else []
            
            for i, fila in enumerate(filas_normativas[1:], 1):
                normativa_dict = {}
                for j, header in enumerate(headers_normativas):
                    if j < len(fila):
                        normativa_dict[header] = fila[j]
                self.datos_normativas.append(normativa_dict)
            
            self.log(f"  ✓ {len(filas_normativas)-1} normativas cargadas")
            
            # CARGAR RESTRICCIONES
            self.log(f"\n[6/7] RESTRICCIONES: {os.path.basename(archivos['restricciones'])}")
            with open(archivos['restricciones'], 'r', encoding='utf-8') as f:
                filas_restricciones = list(csv.reader(f))
            
            self.datos_restricciones = []
            headers_rest = filas_restricciones[0] if len(filas_restricciones) > 0 else []
            
            for i, fila in enumerate(filas_restricciones[1:], 1):
                restriccion_dict = {}
                for j, header in enumerate(headers_rest):
                    if j < len(fila):
                        restriccion_dict[header] = fila[j]
                self.datos_restricciones.append(restriccion_dict)
            
            self.log(f"  ✓ {len(filas_restricciones)-1} restricciones cargadas")
            
            # CARGAR ENTRADAS SISTEMA
            self.log(f"\n[7/7] ENTRADAS SISTEMA: {os.path.basename(archivos['entradas'])}")
            with open(archivos['entradas'], 'r', encoding='utf-8') as f:
                filas_entradas = list(csv.reader(f))
            
            self.datos_entradas = []
            headers_entradas = filas_entradas[0] if len(filas_entradas) > 0 else []
            
            for i, fila in enumerate(filas_entradas[1:], 1):
                entrada_dict = {}
                for j, header in enumerate(headers_entradas):
                    if j < len(fila):
                        entrada_dict[header] = fila[j]
                self.datos_entradas.append(entrada_dict)
            
            self.log(f"  ✓ {len(filas_entradas)-1} entradas cargadas")
            
            # Aplicar restricciones a los campos
            self.log(f"\nAplicando configuraciones...")
            for restriccion in self.datos_restricciones:
                tipo = restriccion.get('Tipo', '').upper()
                desc = restriccion.get('Descripcion', '').lower()
                valor = restriccion.get('Valor', '')
                
                try:
                    if tipo == 'RESTRICCION':
                        if 'horas' in desc and 'maximas' in desc:
                            self.entries['horas_max'].delete(0, tk.END)
                            self.entries['horas_max'].insert(0, valor)
                        elif 'turnos nocturnos' in desc:
                            self.entries['max_turnos_nocturnos'].delete(0, tk.END)
                            self.entries['max_turnos_nocturnos'].insert(0, valor)
                    
                    elif tipo == 'CONFIGURACION':
                        if 'generaciones' in desc and 'recomendadas' in desc:
                            self.entries['max_generaciones'].delete(0, tk.END)
                            self.entries['max_generaciones'].insert(0, valor)
                        elif 'probabilidad cruza' in desc:
                            self.entries['prob_cruza'].delete(0, tk.END)
                            self.entries['prob_cruza'].insert(0, valor)
                        elif 'probabilidad mutacion' in desc:
                            self.entries['prob_mutacion'].delete(0, tk.END)
                            self.entries['prob_mutacion'].insert(0, valor)
                    
                    elif tipo == 'SUELDO':
                        if 'turno' in desc and ('lunes' in desc.lower() or 'sabado' in desc.lower()):
                            self.entry_pago_dia.delete(0, tk.END)
                            self.entry_pago_dia.insert(0, valor)
                        elif 'domingo' in desc.lower():
                            self.entry_pago_domingo.delete(0, tk.END)
                            self.entry_pago_domingo.insert(0, valor)
                        elif 'segundo' in desc.lower() or 'mismo dia' in desc.lower():
                            self.entry_pago_dia_extra.delete(0, tk.END)
                            self.entry_pago_dia_extra.insert(0, valor)
                
                except Exception as e:
                    pass
            
            self.log(f"\n{'='*70}")
            self.log(f"BASE DE CONOCIMIENTO CARGADA CORRECTAMENTE")
            self.log(f"{'='*70}\n")
            
            # Ejecutar el algoritmo
            self.ejecutar_algoritmo()
            
        except Exception as e:
            self.log(f"\nERROR al cargar archivos: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar archivos:\n{str(e)}")
    
    def importar_csv(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir="base_conocimientos"
        )
        
        if not archivo:
            return
        
        try:
            import csv
            
            nombre_archivo = os.path.basename(archivo)
            
            self.log(f"\n{'='*60}")
            self.log(f"IMPORTANDO: {nombre_archivo}")
            self.log(f"{'='*60}\n")
            
            with open(archivo, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                filas = list(reader)
            
            if 'vigilantes' in nombre_archivo.lower():
                self.log("Tipo: VIGILANTES")
                self.log(f"Total vigilantes encontrados: {len(filas)-1}\n")
                
                self.datos_vigilantes = []
                headers = filas[0] if len(filas) > 0 else []
                
                self.log("Vigilantes cargados:")
                for i, fila in enumerate(filas):
                    if i == 0:
                        self.log(f"  {', '.join(fila)}")
                        self.log("  " + "-"*50)
                    elif i >= 1:
                        vigilante_dict = {}
                        for j, header in enumerate(headers):
                            if j < len(fila):
                                vigilante_dict[header] = fila[j]
                        self.datos_vigilantes.append(vigilante_dict)
                        
                        if i <= 5:
                            nombre = vigilante_dict.get('Nombre', 'N/A')
                            apellido = vigilante_dict.get('Apellido', '')
                            turno = vigilante_dict.get('Turno_Preferido', 'N/A')
                            self.log(f"  {nombre} {apellido} - Turno: {turno}")
                
                if len(filas) > 6:
                    self.log(f"  ... y {len(filas)-6} mas")
                
                num_vigilantes = len(filas) - 1
                self.entries['num_vigilantes'].delete(0, tk.END)
                self.entries['num_vigilantes'].insert(0, str(num_vigilantes))
                self.log(f"\nNumero de vigilantes actualizado a: {num_vigilantes}")
                self.log(f"Datos de {len(self.datos_vigilantes)} vigilantes guardados en memoria")
                
            elif 'restricciones' in nombre_archivo.lower() or 'restriccion' in nombre_archivo.lower():
                self.log("Tipo: RESTRICCIONES")
                self.log(f"Total restricciones encontradas: {len(filas)-1}\n")
                
                self.log("Restricciones principales:")
                for i, fila in enumerate(filas):
                    if i == 0:
                        continue
                    if len(fila) >= 3:
                        tipo = fila[0] if len(fila) > 0 else ""
                        desc = fila[1] if len(fila) > 1 else ""
                        valor = fila[2] if len(fila) > 2 else ""
                        
                        if tipo == "RESTRICCION":
                            self.log(f"  - {desc}: {valor}")
                
                for fila in filas[1:]:
                    if len(fila) >= 3:
                        desc = fila[1].lower() if len(fila) > 1 else ""
                        valor = fila[2] if len(fila) > 2 else ""
                        
                        if 'horas legales' in desc or 'horas maximas' in desc:
                            try:
                                self.entries['horas_max'].delete(0, tk.END)
                                self.entries['horas_max'].insert(0, valor)
                                self.log(f"\nHoras maximas actualizado a: {valor}")
                            except:
                                pass
                        
                        elif 'turnos nocturnos' in desc:
                            try:
                                self.entries['max_turnos_nocturnos'].delete(0, tk.END)
                                self.entries['max_turnos_nocturnos'].insert(0, valor)
                                self.log(f"Max turnos nocturnos actualizado a: {valor}")
                            except:
                                pass
            
            else:
                self.log("Tipo: DATOS GENERICOS")
                self.log(f"Total filas: {len(filas)}\n")
                
                self.log("Primeras 5 filas:")
                for i, fila in enumerate(filas[:5]):
                    self.log(f"  {', '.join(fila)}")
            
            self.log(f"\n{'='*60}")
            self.log("IMPORTACION COMPLETADA")
            self.log(f"{'='*60}\n")
            
            respuesta = messagebox.askyesno("Importacion Exitosa", 
                f"Archivo CSV importado correctamente:\n\n{nombre_archivo}\n\n"
                f"Total filas: {len(filas)}\n\n"
                f"¿Deseas ejecutar el algoritmo ahora con estos datos?")
            
            if respuesta:
                self.log("\nEjecutando algoritmo automaticamente...\n")
                self.root.after(500, self.ejecutar_algoritmo)
            
        except Exception as e:
            import traceback
            error_completo = traceback.format_exc()
            self.log(f"\nERROR al importar CSV:")
            self.log("="*60)
            self.log(error_completo)
            self.log("="*60)
            messagebox.showerror("Error", f"Error al importar CSV:\n{str(e)}")

def main():
    root = tk.Tk()
    app = AplicacionEscritorio(root)
    root.mainloop()

if __name__ == "__main__":
    main()
