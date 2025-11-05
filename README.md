# Lab 10 - OpenGL 3D Model Viewer 
## Descripción

Este laboratorio implementa un renderizador 3D completo que permite visualizar múltiples modelos OBJ con texturas, aplicar efectos visuales mediante shaders personalizados, y navegar alrededor de los modelos usando una cámara orbital intuitiva.

## Características

- **Visualización de Modelos 3D**: Carga y renderiza archivos .obj con sus texturas correspondientes
- **Skybox Personalizado**: Entorno 3D inmersivo con texturas de cielo
- **Cámara Orbital**: Sistema completo de cámara con controles de mouse y teclado
- **Shaders Creativos**: Efectos visuales personalizados (hologram, rainbow, glitch, twist, bend)
- **Interfaz Intuitiva**: Controles fluidos para navegar y cambiar entre modelos

## Requisitos

### Software
- Python 3 (32-bit)
- pip (gestor de paquetes de Python)

### Librerías
```bash
pip install pygame
pip install PyOpenGL
pip install PyGLM
pip install numpy
```

## Instalación y Configuración

### 1. Preparación del Entorno

Este proyecto requiere **Python 3 de 32 bits** para compatibilidad con PyOpenGL.

#### Activar el entorno virtual (32-bit)
```bash
# Navegar al directorio del proyecto
cd C:\Users\[TU_USUARIO]\OneDrive\Escritorio\OpenGL\Lab10

# Activar el entorno virtual de 32 bits
..\env32\Scripts\activate

# Verificar que estás usando Python 32-bit
python -c "import struct; print('Python', struct.calcsize('P') * 8, 'bits')"

# Deberías ver:
Python 32 bits
```

## Estructura del Laboratorio
```
Lab10/
│
├── RendererOpenGL.py      # Archivo principal
├── gl.py                  # Renderer y lógica de renderizado
├── camera.py              # Sistema de cámara orbital
├── model.py               # Carga y gestión de modelos
├── obj.py                 # Parser de archivos .obj
├── buffer.py              # Buffers de OpenGL
├── skybox.py              # Renderizado del skybox
├── vertexShaders.py       # Shaders de vértices
├── fragmentShaders.py     # Shaders de fragmentos
│
├── models/                # Modelos 3D (.obj)
│   ├── among us.obj
│   ├── SlothSword.obj
│   └── obj file.obj
│
├── textures/              # Texturas de modelos
│   ├── Plastic_4K_Diffuse.jpg
│   ├── Material_BaseColor.png
│   └── CaptainCupcake_material.jpg
│
└── skybox/                # Texturas del skybox
    ├── posx.jpg
    ├── negx.jpg
    ├── posy.jpg
    ├── negy.jpg
    ├── posz.jpg
    └── negz.jpg
```

## Controles

### Cambio de Modelos
| Tecla | Acción |
|-------|--------|
| `M` | Modelo 1 (Among Us) |
| `N` | Modelo 2 (Sloth Sword) |
| `B` | Modelo 3 (Captain Cupcake) |

### Cámara - Teclado
| Tecla | Acción |
|-------|--------|
| `←` `→` | Rotar horizontalmente |
| `↑` `↓` | Rotar verticalmente |
| `I`  | Zoom in (acercar) |
| `O` | Zoom out (alejar) |

### Cámara - Mouse
| Control | Acción |
|---------|--------|
| **Click izquierdo + arrastrar** | Rotar cámara |
| **Rueda del mouse** | Zoom in/out |

### Shaders de Fragmento
| Tecla | Efecto |
|-------|--------|
| `1` | Hologram (efecto holográfico) |
| `2` | Rainbow (colores arcoíris) |
| `3` | Glitch (efecto de distorsión) |

### Shaders de Vértice
| Tecla | Efecto |
|-------|--------|
| `4` | Twist (torsión del modelo) |
| `5` | Bend (curvatura del modelo) |
| `9` | Regresarlo a la normalidad|

### Otros Controles
| Tecla | Acción |
|-------|--------|
| `9` | Resetear shaders (normal) |
| `F` | Toggle wireframe/filled |
| `W` `S` | Mover luz (Z) |
| `A` `D` | Mover luz (X) |
| `Q` `E` | Mover luz (Y) |
| `Z` `X` | Ajustar valor de shader |

## Ejecución

1. Asegúrate de tener todas las dependencias instaladas
2. Navega al directorio del proyecto
3. Ejecuta el programa:
```bash
python RendererOpenGL.py
```

## Shaders Incluidos

### Fragment Shaders
- **Hologram**: Efecto holográfico con franjas animadas y efecto fresnel
- **Rainbow**: Colores arcoíris dinámicos con ondas animadas
- **Glitch**: Efecto de distorsión digital con aberración cromática

### Vertex Shaders
- **Twist**: Torsión rotacional del modelo basada en altura
- **Bend**: Curvatura dinámica con oscilación animada

## Características Técnicas

### Sistema de Cámara
- **Modo Orbital**: La cámara siempre mira hacia el centro del modelo
- **Límites verticales**: -80° a +80° (previene inversión)
- **Límites de zoom**: 2.0 a 20.0 unidades
- **Coordenadas esféricas**: Movimiento suave y natural

### Renderizado
- **Resolución**: 960x540
- **Frame rate**: 60 FPS
- **Iluminación**: Point light dinámica con luz ambiental
- **Skybox**: Textura cúbica de 6 caras

##  Notas Importantes

- El proyecto está optimizado para **Python 3 de 32 bits**
- Solo un modelo es visible a la vez para optimizar rendimiento
- Los shaders funcionan con todos los modelos cargados
- El skybox se renderiza con depth mask desactivado para estar siempre al fondo

## Video de como funciona el laboratorio
https://github.com/user-attachments/assets/d3d6f9b9-fb4e-42e0-bfa3-a6dc9cb87a2b


## Autor
- Joel Antonio Jaquez López #23369
