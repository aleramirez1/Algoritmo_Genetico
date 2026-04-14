# Sistema de Asignación de Vigilantes - Algoritmo Genético

Sistema inteligente para la asignación óptima de horarios de vigilantes utilizando algoritmos genéticos.

## 📋 Descripción

Este sistema utiliza un algoritmo genético para generar horarios óptimos de vigilantes, considerando múltiples restricciones laborales, legales y de cobertura. El objetivo es maximizar la cobertura, minimizar horas extras, balancear la carga de trabajo y cumplir con todas las normativas laborales.

## 🚀 Instalación

### Requisitos
- Python 3.8 o superior
- Windows (el sistema está optimizado para Windows)

### Pasos de instalación

1. Clonar o descargar el repositorio

2. Ejecutar el script de instalación:
```bash
cd backend
setup.bat
```

Este script instalará automáticamente todas las dependencias necesarias.

## 💻 Uso

### Ejecución rápida

```bash
cd backend
ejecutar_app.bat
```

### Configuración

1. **Cargar Vigilantes**: Importar el archivo `base_conocimientos/vigilantes.csv`
2. **Configurar Parámetros**: Ajustar los valores en el panel izquierdo
3. **Ejecutar**: Hacer clic en el botón "EJECUTAR"
4. **Ver Resultados**: Explorar las diferentes pestañas de resultados

## 📊 Base de Conocimientos

El sistema utiliza varios archivos CSV en la carpeta `base_conocimientos/`:

- **vigilantes.csv**: Catálogo de vigilantes disponibles
- **turnos.csv**: Definición de turnos (Día/Noche)
- **puestos.csv**: Puestos de vigilancia a cubrir
- **restricciones.csv**: Restricciones del sistema
- **politicas_empresa.csv**: Políticas internas de la empresa
- **normativas_laborales.csv**: Normativas laborales vigentes
- **entradas_sistema.csv**: Documentación de entradas del sistema

## 🎯 Características

### Algoritmo Genético
- Población configurable
- Cruza y mutación adaptativa
- Selección por torneo
- Elitismo para preservar mejores soluciones

### Restricciones
- ✅ Cobertura 100% de todos los puestos
- ✅ Máximo 60 horas semanales por vigilante
- ✅ Máximo 3 turnos nocturnos por semana
- ✅ Hasta 2 turnos por día (con pago extra)
- ✅ Sueldo mínimo semanal de $2,396 MXN

### Sistema de Pagos
- Turno normal (Lun-Sab): $316 MXN
- Turno Domingo: $632 MXN (doble)
- Segundo turno mismo día: $632 MXN (extra)

### Interfaz Gráfica
- **Métricas**: Fitness, cobertura, horas extra, balance, violaciones
- **Gráfica Evolución**: Visualización del progreso del algoritmo
- **Costos y Sueldos**: Cálculo detallado de pagos
- **Restricciones**: Visualización de reglas del sistema
- **Horarios**: Top 1, 2, 3 y Peor con explicaciones detalladas

## 📈 Resultados

El sistema genera 4 horarios:

1. **Top 1 (Mejor Global)**: Mejor solución encontrada en todas las generaciones
2. **Top 2**: Mejor solución de la población final
3. **Top 3**: Segunda mejor solución de la población final
4. **Peor**: Peor solución (para comparación)

Cada horario incluye:
- Tabla de asignaciones por día y turno
- Métricas de calidad
- Explicación de por qué es bueno/malo
- Información sobre cómo se seleccionó

## 🔧 Configuración Avanzada

### Parámetros del Algoritmo
- **Tamaño Población**: 20 (recomendado)
- **Probabilidad Cruza**: 0.85
- **Probabilidad Mutación**: 0.20
- **Max Generaciones**: 100

### Función de Fitness
```
Fitness = CT × (1 - 0.3×HE - 0.2×BCL - 0.5×VL)
```

Donde:
- CT = Cobertura de turnos (0-1)
- HE = Penalización horas extra (0-1)
- BCL = Penalización balance carga laboral (0-1)
- VL = Penalización violaciones (0-1)

## 📁 Estructura del Proyecto

```
.
├── backend/
│   ├── algoritmo_genetico.py    # Lógica del algoritmo genético
│   ├── app_escritorio.py         # Interfaz gráfica
│   ├── ejecutar_app.bat          # Script de ejecución
│   ├── setup.bat                 # Script de instalación
│   └── requirements.txt          # Dependencias Python
│
└── base_conocimientos/
    ├── vigilantes.csv            # Catálogo de vigilantes
    ├── turnos.csv                # Definición de turnos
    ├── puestos.csv               # Puestos de vigilancia
    ├── restricciones.csv         # Restricciones del sistema
    ├── politicas_empresa.csv     # Políticas internas
    ├── normativas_laborales.csv  # Normativas legales
    └── entradas_sistema.csv      # Documentación de entradas
```

## 🛠️ Tecnologías

- **Python 3.8+**
- **tkinter**: Interfaz gráfica
- **matplotlib**: Visualización de gráficas
- **numpy**: Cálculos numéricos
- **openpyxl**: Exportación a Excel

## 📝 Licencia

Este proyecto es de uso interno para la gestión de horarios de vigilantes.

## 👥 Soporte

Para soporte o preguntas sobre el sistema, consultar la documentación en `base_conocimientos/`.

---

**Versión**: 1.0  
**Última actualización**: 2024
