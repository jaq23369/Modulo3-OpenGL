import pygame
import pygame.display
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import *

import glm

from gl import Renderer
from buffer import Buffer
from model import Model
from vertexShaders import *
from fragmentShaders import *
from postProcessingShaders import *

width = 960
height = 540

deltaTime = 0.0


screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()

# Inicializar y reproducir música de fondo
pygame.mixer.init()
pygame.mixer.music.load("audio/Super Smash Bros. Ultimate.mp3")  
pygame.mixer.music.set_volume(0.4)  
pygame.mixer.music.play(-1)

rend = Renderer(screen)
rend.pointLight = glm.vec3(1,1,1)

currVertexShader = vertex_shader
currFragmentShader = fragment_shader

rend.SetShaders(currVertexShader, currFragmentShader)

skyboxTextures = ["skybox/posx.jpg",  # Right (derecha +X)
				  "skybox/negx.jpg",  # Left (izquierda -X)
				  "skybox/posy.jpg",  # Top (arriba +Y)
				  "skybox/negy.jpg",  # Bottom (abajo -Y)
				  "skybox/posz.jpg",  # Front (frente +Z)
				  "skybox/negz.jpg"]  # Back (atrás -Z)

rend.CreateSkybox(skyboxTextures)


# Model 1 - YOSHI con Toon Shader + Wave Vertex
model1 = Model("models/Yoshi.obj")
model1.AddTexture("textures/Jumping_Green_Charact_1107032123_texture.png")
model1.position = glm.vec3(-3, 0, -5)
model1.scale = glm.vec3(1.6, 1.6, 1.6)
model1.rotation = glm.vec3(0, 90, 0)
model1.vertexShader = yoshi_wave_vertex
model1.fragmentShader = yoshi_toon_shader

# Model 2 - STAGE con Grid Shader + Vertex normal
model2 = Model("models/SMS_HBStage.obj")
model2.AddTexture("textures/SMS_HBStage_Material.003_BaseColor.png")
model2.position = glm.vec3(0, -1.5, -5)
model2.scale = glm.vec3(0.01, 0.01, 0.01)
model2.vertexShader = vertex_shader  # Vertex normal (plataforma no se deforma)
model2.fragmentShader = stage_grid_shader

# Model 3 - MARIO con Fire Shader + Pulse Vertex
model3 = Model("models/Mario.obj")
model3.AddTexture("textures/Mario_Jumping_Action_1107234344_texture.png")
model3.position = glm.vec3(3, 0.5, -5)
model3.scale = glm.vec3(1.5, 1.5, 1.5)
model3.rotation = glm.vec3(0, -95, 0)
model3.vertexShader = mario_pulse_vertex
model3.fragmentShader = mario_fire_shader

# Model 4 - METAL SONIC con Metallic Shader + Spin Vertex
model4 = Model("models/Metal_Sonic.obj")
model4.AddTexture("textures/Metal_Sonic_1107235427_texture.png")
model4.position = glm.vec3(-1.3, 4.2, -5)
model4.scale = glm.vec3(1.35, 1.35, 1.35)
model4.rotation = glm.vec3(0, 90, 0)
model4.vertexShader = metal_sonic_spin_vertex
model4.fragmentShader = metal_sonic_metallic_shader

# Model 5 - CAPTAIN FALCON con Energy Aura Shader + Aura Vertex
model5 = Model("models/Captain_Falcon.obj")
model5.AddTexture("textures/Captain_Falcon_1108000736_texture.png")
model5.position = glm.vec3(1.4, 4.0, -5)
model5.scale = glm.vec3(1.36, 1.36, 1.36)
model5.rotation = glm.vec3(0, -80, 0)
model5.vertexShader = falcon_aura_vertex
model5.fragmentShader = falcon_aura_shader

# Model 6 - PAC-MAN con Neon Shader + Bounce Vertex
model6 = Model("models/Pac_Man.obj")
model6.AddTexture("textures/Pac_Dance_Move_1108002314_texture.png")
model6.position = glm.vec3(-8, 0, -5)
model6.scale = glm.vec3(1.55, 1.55, 1.55)
model6.rotation = glm.vec3(0, 0, 0)
model6.vertexShader = pacman_bounce_vertex
model6.fragmentShader = pacman_neon_shader

# Model 7 - LITTLE MAC con CRT Shader + Punch Vertex
model7 = Model("models/Little_Mac.obj")
model7.AddTexture("textures/Boxing_Challenger_in__1108003843_texture.png")
model7.position = glm.vec3(9, -0.5, -5)
model7.scale = glm.vec3(1.65, 1.65, 1.65)
model7.rotation = glm.vec3(0, -120, 0)
model7.vertexShader = littlemac_punch_vertex
model7.fragmentShader = littlemac_crt_shader

# Lista de todos los modelos
allModels = [model1, model2, model3, model4, model5, model6, model7] 

# Agregar TODOS los modelos a la escena desde el inicio
for model in allModels:
	rend.scene.append(model)

# Variables para control de mouse
mouseDown = False
lastMousePos = (0, 0)

# Variable para activar/desactivar shaders creativos
creativeShadersEnabled = False  

# Configurar post-processing 
postProcessIndex = 0  
postProcesses = [none_postProcess,           
				 cinematicBloom_postProcess,
				 retroNeonWave_postProcess]  

rend.SetPostProcessingShaders(vertex_postProcess, postProcesses[postProcessIndex])

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
			
			# Toggle shaders creativos (ON/OFF)
			if event.key == pygame.K_g:
				creativeShadersEnabled = not creativeShadersEnabled

			# Ciclar entre efectos creativos con TAB
			if event.key == pygame.K_TAB:
				postProcessIndex += 1
				postProcessIndex %= len(postProcesses)
				rend.SetPostProcessingShaders(vertex_postProcess, postProcesses[postProcessIndex])

			if event.key == pygame.K_u:  # Tecla U - Vista general
				rend.camera.SetTarget(glm.vec3(0, 0, -5))  # Centro de la escena
			
			if event.key == pygame.K_j:  # Tecla J - Enfocar Yoshi
				rend.camera.SetTarget(model1.position)
			
			if event.key == pygame.K_k:  # Tecla K - Enfocar Stage
				rend.camera.SetTarget(model2.position)
			
			if event.key == pygame.K_l:  # Tecla L - Enfocar Mario
				rend.camera.SetTarget(model3.position)
			
			if event.key == pygame.K_p:  # Tecla P - Enfocar Metal Sonic
				rend.camera.SetTarget(model4.position)
			
			if event.key == pygame.K_t:  # Tecla T - Enfocar Captain Falcon
				rend.camera.SetTarget(model5.position)
			
			if event.key == pygame.K_y:  # Tecla Y - Enfocar Pac-Man
				rend.camera.SetTarget(model6.position)
			
			if event.key == pygame.K_r:  # Tecla R - Enfocar Little Mac
				rend.camera.SetTarget(model7.position)
		
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
	
	# Aplicar o quitar shaders creativos según el flag
	if creativeShadersEnabled:
		# Asegurar que cada modelo tenga sus shaders 
		model1.vertexShader = yoshi_wave_vertex
		model1.fragmentShader = yoshi_toon_shader
		
		model2.vertexShader = vertex_shader
		model2.fragmentShader = stage_grid_shader
		
		model3.vertexShader = mario_pulse_vertex
		model3.fragmentShader = mario_fire_shader
		
		model4.vertexShader = metal_sonic_spin_vertex
		model4.fragmentShader = metal_sonic_metallic_shader
		
		model5.vertexShader = falcon_aura_vertex
		model5.fragmentShader = falcon_aura_shader
		
		model6.vertexShader = pacman_bounce_vertex
		model6.fragmentShader = pacman_neon_shader
		
		model7.vertexShader = littlemac_punch_vertex
		model7.fragmentShader = littlemac_crt_shader
	else:
		# Usar shaders básicos para todos
		for model in allModels:
			model.vertexShader = vertex_shader
			model.fragmentShader = fragment_shader


	rend.Render()
	
	pygame.display.flip()

pygame.quit()