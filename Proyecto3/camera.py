import glm
import math

class Camera(object):
	def __init__(self, width, height):

		self.screenWidth = width
		self.screenHeight = height
		
		self.position = glm.vec3(0,0,0)

		# Angulos de Euler
		self.rotation = glm.vec3(0,0,0)

		self.viewMatrix = None

		# Parámetros para cámara orbital
		self.target = glm.vec3(0, 0, -5)  # Punto al que mira la cámara (centro del modelo)
		self.distance = 5.0  # Distancia al objetivo
		self.orbitAngleY = 0.0  # Ángulo horizontal (rotación alrededor del eje Y)
		self.orbitAngleX = 0.0  # Ángulo vertical (elevación)
		
		# Límites de movimiento
		self.minDistance = 2.0
		self.maxDistance = 20.0
		self.minOrbitAngleX = -80.0  # Límite inferior (no puede ir más abajo)
		self.maxOrbitAngleX = 80.0   # Límite superior (no puede ir más arriba)

		self.CreateProjectionMatrix(60, 0.1, 1000)

	# Actualiza la posición de la cámara en modo orbital
	def UpdateOrbital(self):
		# Convertir ángulos a radianes
		angleXRad = math.radians(self.orbitAngleX)
		angleYRad = math.radians(self.orbitAngleY)
		
		# Calcular posición de la cámara en coordenadas esféricas
		# x = distancia * cos(elevación) * sin(azimut)
		# y = distancia * sin(elevación)
		# z = distancia * cos(elevación) * cos(azimut)
		self.position.x = self.target.x + self.distance * math.cos(angleXRad) * math.sin(angleYRad)
		self.position.y = self.target.y + self.distance * math.sin(angleXRad)
		self.position.z = self.target.z + self.distance * math.cos(angleXRad) * math.cos(angleYRad)
		
		# Crear la matriz de vista mirando siempre al objetivo
		self.viewMatrix = glm.lookAt(self.position, self.target, glm.vec3(0, 1, 0))

	def Update(self):
		# M = T * R
		# R = pitchMat * yawMat * rollMat

		identity = glm.mat4(1)

		translateMat = glm.translate(identity, self.position)

		pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
		yawMat =   glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
		rollMat =  glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))

		rotationMat = pitchMat * yawMat * rollMat

		camMat = translateMat * rotationMat

		self.viewMatrix = glm.inverse(camMat)

	# Rota la cámara alrededor del objetivo
	def Orbit(self, deltaX, deltaY):
		self.orbitAngleY += deltaX
		self.orbitAngleX += deltaY
		
		# Aplicar límites verticales
		if self.orbitAngleX < self.minOrbitAngleX:
			self.orbitAngleX = self.minOrbitAngleX
		if self.orbitAngleX > self.maxOrbitAngleX:
			self.orbitAngleX = self.maxOrbitAngleX
	
	# Acerca o aleja la cámara del objetivo
	def Zoom(self, delta):
		self.distance += delta
		
		# Aplicar límites de distancia
		if self.distance < self.minDistance:
			self.distance = self.minDistance
		if self.distance > self.maxDistance:
			self.distance = self.maxDistance
	
	# Cambia el punto al que mira la cámara (enfoca un modelo específico)
	def SetTarget(self, newTarget):
		self.target = newTarget

	def CreateProjectionMatrix(self, fov, nearPlane, farPlane):
		self.projectionMatrix = glm.perspective( glm.radians(fov), self.screenWidth / self.screenHeight, nearPlane, farPlane)