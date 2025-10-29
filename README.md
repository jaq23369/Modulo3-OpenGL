# Lab 9 - Shaders Personalizados en OpenGL

## Descripción del Laboratorio

Laboratorio de shaders GLSL para OpenGL, implementa 3 Fragment Shaders y 2 Vertex Shaders personalizados con efectos visuales creativos y complejos. El laboratorio utiliza un modelo de Among Us con texturas y un skybox para demostrar los diferentes efectos de shaders.

## Objetivos del Lab

- Crear shaders personalizados (Vertex y Fragment) en GLSL
- Implementar efectos visuales complejos e interesantes
- Permitir cambio dinámico de shaders durante la ejecución
- Demostrar compatibilidad entre todos los shaders (cada Vertex funciona con cada Fragment)

## Shaders Implementados

### Fragment Shaders (60 puntos)

#### 1. Hologram Shader (Tecla 1) - 20 puntos
Efecto holográfico futurista con:
- Color base cyan/azul brillante característico de hologramas
- Franjas horizontales animadas con `sin()` y `smoothstep()`
- Efecto Fresnel para brillo en los bordes del modelo
- Sistema de parpadeo/glitch con variaciones temporales
- Transparencia dinámica basada en el ángulo de vista

**Técnicas usadas:** Fresnel effect, procedural stripes, temporal glitches, alpha blending

#### 2. Rainbow Shader (Tecla 2) - 20 puntos
Efecto de arcoíris disco animado con:
- Función `rainbow()` personalizada usando desfases de fase (2π/3)
- Franjas de colores que se mueven verticalmente
- Ondas horizontales sinusoidales para agregar dinamismo
- Pulso de brillo sincronizado con el tiempo
- Mezcla con iluminación ambiental y direccional

**Técnicas usadas:** Color theory (RGB phase shifting), wave functions, temporal animation, lighting integration

#### 3. Glitch/Cyberpunk Shader (Tecla 3) - 20 puntos
Efecto cyberpunk con distorsión digital:
- Aberración cromática (separación de canales RGB)
- Bloques de glitch que se desplazan horizontalmente de forma aleatoria
- Función de ruido pseudo-aleatorio para patrones impredecibles
- Líneas de escaneo CRT animadas
- Colores neón (magenta y cyan) con flashes dinámicos
- Aumento de saturación para estética cyberpunk

**Técnicas usadas:** Chromatic aberration, pseudo-random noise, scanlines, color grading, UV manipulation

### Vertex Shaders (40 puntos)

#### 4. Twist Shader (Tecla 4) - 20 puntos
Efecto de torsión espiral:
- Rotación progresiva basada en la altura (coordenada Y)
- Transformación de coordenadas usando matriz de rotación manual
- Animación continua con el tiempo
- Control de intensidad mediante uniform `value`
- Rotación de normales para mantener iluminación correcta
- Efecto tipo "retorcido" o "espiral DNA"

**Técnicas usadas:** Parametric rotation, matrix transformations, normal transformation, procedural deformation

#### 5. Bend Shader (Tecla 5) - 20 puntos
Efecto de curvatura/doblado flexible:
- Deformación parabólica basada en altura (Y²)
- Oscilación lateral usando funciones seno/coseno
- Curvatura en múltiples ejes (X y Z) para efecto 3D
- Movimiento vertical adicional con ondas
- Ajuste de normales para iluminación coherente
- Simula objeto flexible que se dobla

**Técnicas usadas:** Quadratic deformation, multi-axis bending, oscillation, wave propagation

## Controles

### Cambio de Shaders
| Tecla | Shader | Tipo |
|-------|--------|------|
| **1** | Hologram | Fragment |
| **2** | Rainbow | Fragment |
| **3** | Glitch/Cyberpunk | Fragment |
| **4** | Twist | Vertex |
| **5** | Bend | Vertex |
| **9** | Reset (normalidad) | Ambos |
| **F** | Toggle Wireframe | Render Mode |

### Controles de Cámara
- **Flechas ↑↓←→**: Mover cámara en espacio 3D
- Cámara en perspectiva con FOV configurable

### Controles de Iluminación
- **W**: Mover luz hacia adelante (-Z)
- **S**: Mover luz hacia atrás (+Z)
- **A**: Mover luz a la izquierda (-X)
- **D**: Mover luz a la derecha (+X)
- **Q**: Mover luz hacia abajo (-Y)
- **E**: Mover luz hacia arriba (+Y)

### Controles de Efectos
- **Z**: Disminuir intensidad de efectos (`value`)
- **X**: Aumentar intensidad de efectos (`value`)

## Requisitos Técnicos

### Software Necesario
- **Python 3.10** (32-bit)
- **PyOpenGL** - Wrapper de OpenGL para Python
- **PyGLM** - Biblioteca de matemáticas 3D (vectores, matrices)
- **Pygame** - Ventana, input y carga de texturas

### Instalación

#### Requisitos Previos
- Python 3.10 (32-bit) - [Descargar aquí](https://www.python.org/downloads/release/python-31011/)
  - Durante la instalación, marcar "Add Python to PATH"
  - Seleccionar la versión de 32-bit (Windows x86)

#### Pasos de Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/jaq23369/Modulo3-OpenGL.git
cd Modulo3-OpenGL/Lab9

# 2. Crear entorno virtual de 32 bits (usar el Python de 32-bit instalado)
python -m venv env32

# 3. Activar el entorno virtual
.\env32\Scripts\Activate.ps1

# Si aparece error de permisos en PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 4. Instalar dependencias
pip install PyOpenGL PyGLM pygame

# 5. Ejecutar el programa
python RendererOpenGL.py

## Comprobación del funcionamiento
https://github.com/user-attachments/assets/278989ec-ae9f-4ef4-a1ee-3a86f53244ba
```

## Comprobación del funcionamiento
https://github.com/user-attachments/assets/278989ec-ae9f-4ef4-a1ee-3a86f53244ba

## Hecho por
- Joel Antonio Jaquez López #23369

