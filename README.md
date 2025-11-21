# Proyecto 3 - Diorama 3D de Super Smash Bros Ultimate

- Curso: Gráficas por Computadora  
- Estudiante: Joel Antonio Jaquez López 
- Carnet: 23369 
- Fecha: 20 de Noviembre del 2025 

---

## Descripción

Diorama interactivo 3D temático de Super Smash Bros Ultimate con 7 personajes icónicos, sistema de cámara orbital avanzado, shaders creativos personalizados y post-processing cinematográfico.

---

## Características Implementadas

### **Modelos 3D **
- **7 personajes** posicionados estratégicamente:
  - Yoshi (Shader holográfico rainbow)
  - Stage/Plataforma (Shader hexagonal energy shield)
  - Mario (Shader de lava procedural)
  - Metal Sonic (Shader chrome metálico)
  - Captain Falcon (Shader plasma eléctrico)
  - Pac-Man (Shader portal wormhole)
  - Little Mac (Shader x-ray wireframe)

### **Sistema de Cámara Orbital**

#### **Movimientos básicos:**
- Zoom: Rueda del mouse / Teclas `I` (acercar) y `O` (alejar)
- Órbita horizontal: Arrastrar mouse / Flechas ⬅️ ➡️
- Órbita vertical: Arrastrar mouse / Flechas ⬆️ ⬇️

#### **Vistas predefinidas (8 teclas):**
| Tecla | Vista |
|-------|-------|
| `U` | Vista general (centro de la escena) |
| `J` | Enfocar Yoshi |
| `K` | Enfocar Stage |
| `L` | Enfocar Mario |
| `P` | Enfocar Metal Sonic |
| `T` | Enfocar Captain Falcon |
| `Y` | Enfocar Pac-Man |
| `R` | Enfocar Little Mac |

### **Shaders**

Cada personaje tiene una combinación de vertex + fragment shader:

| Personaje | Vertex Shader | Fragment Shader | Técnicas |
|-----------|---------------|-----------------|----------|
| **Yoshi** | Wave holográfico | Rainbow gradient | Fresnel, ondas multidireccionales, glitch |
| **Stage** | Normal (estático) | Energy shield | Distance functions, hexágonos, ondas |
| **Mario** | Pulse orgánico | Lava procedural | Noise 3D, gradiente de temperatura, burbujas |
| **Metal Sonic** | Liquid metal spin | Chrome reflections | Environment mapping, Blinn-Phong |
| **Captain Falcon** | Shockwave expansion | Plasma eléctrico | Noise 3D, rayos multiplicativos |
| **Pac-Man** | Portal vortex | Neon wormhole | Chromatic aberration, distorsión espacial |
| **Little Mac** | Scan slicing | X-ray wireframe | Subsurface scattering, grid 3D |

#### **Técnicas implementadas:**
- Procedural noise (smoothNoise, noise 3D)
- Fresnel effects (edge lighting)
- Environment mapping (reflections)
- Chromatic aberration
- Subsurface scattering
- Distance functions (hexágonos perfectos)
- Deformación geométrica avanzada
- Control de intensidad interactivo (`Z`/`X`)

### **Skybox/Cubemap**
- Skybox completo con 6 texturas (posx, negx, posy, negy, posz, negz)

### **Post-Processing**

Dos efectos de post-processing custom:

#### **1. Cinematic Bloom** 
- Blur gaussiano 9x9 con pesos exponenciales
- Color grading cinematográfico (+8% brillo, +15% contraste, +25% saturación)
- Tone mapping Reinhard
- Vignette suave
- Film grain animado
- Gamma correction (sRGB)

#### **2. Retro Neon Wave** 
- Scan lines tipo CRT (540 líneas animadas)
- Chromatic aberration (separación RGB)
- Gradient mapping a paleta neón (púrpura→magenta→cyan→amarillo)
- Wave distortion horizontal
- Bloom intenso estilo neón
- Edge glow pulsante
- Flicker de 60Hz tipo monitor antiguo

**Control:** Tecla `TAB` para ciclar entre efectos (None → Cinematic Bloom → Retro Neon Wave)

### **Música de Fondo**
- Tema oficial de **Super Smash Bros Ultimate**
- Reproducción en loop infinito (40% volumen)

### **Creatividad y Estética**
- Temática cohesiva (Super Smash Bros)
- Posicionamiento estratégico de personajes
- Efectos visuales impresionantes
- Pulido profesional

---

## Controles Completos

### **Shaders:**
- `G` - Activar/desactivar shaders creativos
- `Z` - Disminuir intensidad de efectos
- `X` - Aumentar intensidad de efectos

### **Cámara (Mouse):**
- **Click izquierdo + arrastrar** - Rotar cámara (órbita)
- **Rueda del mouse** - Zoom in/out

### **Cámara (Teclado):**
- `←` `→` - Órbita horizontal
- `↑` `↓` - Órbita vertical
- `I` - Zoom in (acercar)
- `O` - Zoom out (alejar)

### **Vistas:**
- `U` - Vista general
- `J` - Yoshi
- `K` - Stage
- `L` - Mario
- `P` - Metal Sonic
- `T` - Captain Falcon
- `Y` - Pac-Man
- `R` - Little Mac

### **Post-Processing:**
- `TAB` - Cambiar efecto (None → Cinematic Bloom → Retro Neon Wave)

### **Otros:**
- `F` - Toggle wireframe mode
- `W` `A` `S` `D` `Q` `E` - Mover luz puntual

---

## Instalación y Ejecución

### **Requisitos:**
```bash
Python 3.10+
PyOpenGL
PyGLM
Pygame
```
### **Clonar el repositorio:**
```bash
git clone https://github.com/jaq23369/Modulo3-OpenGL.git
cd Modulo3-OpenGL
git checkout Proyecto3
```

### **Crear y activar el entorno virtual de python 32 bits:**
```bash
python -m venv env32
..\env32\Scripts\Activate.ps1
```

### **Si ocurre un error al activar el entorno, ejecutar el siguiente comando:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Inatalar dependencias:**
```bash
pip install pygame PyOpenGL PyOpenGL_accelerate numpy
```

### **Ejecutar el proyecto:**
```bash
cd Proyecto3
python RendererOpenGL.py
```

### **Desactivar el entorno al terminar:**
```bash
deactivate
```
---

## Video del funcionamiento del proyecto
https://github.com/user-attachments/assets/d8f87c07-6747-491e-9b5d-8f5dc21d1744



