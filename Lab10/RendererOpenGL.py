import pygame
import pygame.display
from pygame.locals import *

import glm

from gl import Renderer
from buffer import Buffer
from model import Model
from vertexShaders import *
from fragmentShaders import *

width = 960
height = 540

deltaTime = 0.0


screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()


rend = Renderer(screen)
rend.pointLight = glm.vec3(1,1,1)

currVertexShader = vertex_shader
currFragmentShader = fragment_shader

rend.SetShaders(currVertexShader, currFragmentShader)

skyboxTextures = ["skybox/posx.jpg",  # Right (derecha)
				  "skybox/negx.jpg",  # Left (izquierda)
				  "skybox/posy.jpg",  # Top (arriba)
				  "skybox/negy.jpg",  # Bottom (abajo)
				  "skybox/posz.jpg",  # Front (frente)
				  "skybox/negz.jpg"]  # Back (atrás)

rend.CreateSkybox(skyboxTextures)


# Cargar los 3 modelos
model1 = Model("models/among us.obj")
model1.AddTexture("textures/Plastic_4K_Diffuse.jpg")
model1.position = glm.vec3(-0.3, -1.5, -5)
model1.scale = glm.vec3(0.01, 0.01, 0.01)

model2 = Model("models/SlothSword.obj")
model2.AddTexture("textures/Material_BaseColor.png")
model2.position = glm.vec3(-0.3, -1.5, -5)
model2.scale = glm.vec3(0.04, 0.04, 0.04)  

model3 = Model("models/obj file.obj")
model3.AddTexture("textures/CaptainCupcake_material.jpg")
model3.position = glm.vec3(-0.3, -1.5, -5)
model3.scale = glm.vec3(0.2, 0.2, 0.2)  

# Lista de todos los modelos
allModels = [model1, model2, model3]

# Índice del modelo actual (empezamos con el primero)
currentModelIndex = 0

# Agregar solo el modelo actual a la escena
rend.scene.append(allModels[currentModelIndex])

# Variables para control de mouse
mouseDown = False
lastMousePos = (0, 0)

isRunning = True

while isRunning:

	deltaTime = clock.tick(60) / 1000

	rend.elapsedTime += deltaTime

	keys = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_f:
				rend.ToggleFilledMode()

			if event.key == pygame.K_1:
				currFragmentShader = hologram_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_2:
				currFragmentShader = rainbow_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
			
			if event.key == pygame.K_3:
				currFragmentShader = glitch_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
			
			if event.key == pygame.K_4:
				currVertexShader = twist_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
			
			if event.key == pygame.K_5:
				currVertexShader = bend_shader
				rend.SetShaders(currVertexShader, currFragmentShader)	

			if event.key == pygame.K_9:
				currVertexShader = vertex_shader
				currFragmentShader = fragment_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
		
			# Cambiar entre modelos
			if event.key == pygame.K_m:
				# Remover modelo actual de la escena
				rend.scene.clear()
				currentModelIndex = 0
				# Agregar nuevo modelo
				rend.scene.append(allModels[currentModelIndex])
		
			if event.key == pygame.K_n:
				rend.scene.clear()
				currentModelIndex = 1
				rend.scene.append(allModels[currentModelIndex])
		
			if event.key == pygame.K_b:
				rend.scene.clear()
				currentModelIndex = 2
				rend.scene.append(allModels[currentModelIndex])
		
		# Control de ZOOM con rueda del mouse
		elif event.type == pygame.MOUSEWHEEL:
			rend.camera.Zoom(-event.y * 0.5)  # Zoom in/out
		
		# Detectar cuando se presiona el botón del mouse
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:  # Botón izquierdo del mouse
				mouseDown = True
				lastMousePos = pygame.mouse.get_pos()
		
		# Detectar cuando se suelta el botón del mouse
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				mouseDown = False
	
	# Control de CÁMARA con MOUSE (arrastrar)
	if mouseDown:
		currentMousePos = pygame.mouse.get_pos()
		deltaX = currentMousePos[0] - lastMousePos[0]
		deltaY = currentMousePos[1] - lastMousePos[1]
		
		# Rotar cámara según el movimiento del mouse
		rend.camera.Orbit(deltaX * 0.5, -deltaY * 0.3)  # Sensibilidad ajustable
		
		lastMousePos = currentMousePos

	# Controles de CÁMARA con TECLADO
	# Órbita horizontal (izquierda/derecha)
	if keys[K_LEFT]:
		rend.camera.Orbit(-50 * deltaTime, 0)  # Rotar a la izquierda
	
	if keys[K_RIGHT]:
		rend.camera.Orbit(50 * deltaTime, 0)  # Rotar a la derecha
	
	# Órbita vertical (arriba/abajo)
	if keys[K_UP]:
		rend.camera.Orbit(0, 30 * deltaTime)  # Subir
	
	if keys[K_DOWN]:
		rend.camera.Orbit(0, -30 * deltaTime)  # Bajar
	
	# Zoom con teclado
	if keys[K_i]:  # Tecla I
		rend.camera.Zoom(-2 * deltaTime)  # Acercar (Zoom In)
	
	if keys[K_o]:  # Tecla O
		rend.camera.Zoom(2 * deltaTime)  # Alejar (Zoom Out)

	# Controles de LUZ (mantener los originales)
	if keys[K_w]:
		rend.pointLight.z -= 10 * deltaTime

	if keys[K_s]:
		rend.pointLight.z += 10 * deltaTime

	if keys[K_a]:
		rend.pointLight.x -= 10 * deltaTime

	if keys[K_d]:
		rend.pointLight.x += 10 * deltaTime

	if keys[K_q]:
		rend.pointLight.y -= 10 * deltaTime

	if keys[K_e]:
		rend.pointLight.y += 10 * deltaTime


	if keys[K_z]:
		if rend.value > 0.0:
			rend.value -= 1 * deltaTime

	if keys[K_x]:
		if rend.value < 1.0:
			rend.value += 1 * deltaTime


	# Rotar el modelo actual
	#allModels[currentModelIndex].rotation.y += 45 * deltaTime


	rend.Render()
	pygame.display.flip()

pygame.quit()