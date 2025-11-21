

vertex_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(inPosition, 1.0);

    fragPosition = modelMatrix * vec4(inPosition, 1.0);

    fragNormal = normalize( vec3(modelMatrix * vec4(inNormals, 0.0)));

    fragTexCoords = inTexCoords;
}

'''


fat_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float value;


void main()
{
    fragPosition = modelMatrix * vec4(inPosition + inNormals * value, 1.0);

    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    fragNormal = normalize( vec3(modelMatrix * vec4(inNormals, 0.0)));

    fragTexCoords = inTexCoords;
}

'''

water_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;


void main()
{
    float displacement = sin(time + inPosition.x + inPosition.z) * value;
    fragPosition = modelMatrix * vec4(inPosition + vec3(0,displacement, 0)  , 1.0);

    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    fragNormal = normalize( vec3(modelMatrix * vec4(inNormals, 0.0)));

    fragTexCoords = inTexCoords;
}

'''

twist_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;

void main()
{
    vec3 pos = inPosition;
    
    
    float twistAmount = pos.y * (3.0 + value * 5.0);
    
    
    float angle = twistAmount + time * 2.0;
    
    
    float cosAngle = cos(angle);
    float sinAngle = sin(angle);
    
    
    vec3 twistedPos;
    twistedPos.x = pos.x * cosAngle - pos.z * sinAngle;
    twistedPos.y = pos.y;
    twistedPos.z = pos.x * sinAngle + pos.z * cosAngle;
    
    fragPosition = modelMatrix * vec4(twistedPos, 1.0);
    
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    
    
    vec3 twistedNormal;
    twistedNormal.x = inNormals.x * cosAngle - inNormals.z * sinAngle;
    twistedNormal.y = inNormals.y;
    twistedNormal.z = inNormals.x * sinAngle + inNormals.z * cosAngle;
    
    fragNormal = normalize(vec3(modelMatrix * vec4(twistedNormal, 0.0)));
    
    fragTexCoords = inTexCoords;
}

'''


bend_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;

void main()
{
    vec3 pos = inPosition;
    
    
    float bendAmount = (value * 2.0 + 0.5) * pos.y * pos.y;
    
    
    float bendDirection = sin(time * 1.5);
    
    
    pos.x += bendAmount * bendDirection;
    
    
    pos.z += bendAmount * cos(time * 1.5) * 0.5;
    
    
    pos.y += sin(time * 2.0 + pos.x * 2.0) * value * 0.1;
    
    fragPosition = modelMatrix * vec4(pos, 1.0);
    
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    
    
    vec3 bentNormal = inNormals;
    bentNormal.x += bendDirection * value * 0.3;
    
    fragNormal = normalize(vec3(modelMatrix * vec4(bentNormal, 0.0)));
    
    fragTexCoords = inTexCoords;
}

'''

# ═══════════════════════════
# VERTEX SHADERS PARA PROYECTO 3
# ══════════════════════════

# 1. YOSHI - Holographic Displacement
yoshi_wave_vertex = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform float value;

void main()
{
    vec3 pos = inPosition;
    
    float glitchAmount = mix(0.02, 0.1, value);
    
    // Ondas multidireccionales para glitch holográfico
    float wave1 = sin(pos.x * 15.0 + time * 3.0) * glitchAmount;
    float wave2 = cos(pos.y * 12.0 - time * 2.5) * glitchAmount;
    float wave3 = sin(pos.z * 10.0 + time * 4.0) * glitchAmount * 0.5;
    
    pos.x += wave1;
    pos.y += wave2 + sin(time * 2.0) * glitchAmount * 0.5;
    pos.z += wave3;
    
    float scanHeight = fract(time * 0.3) * 2.0 - 1.0;
    float scanEffect = smoothstep(0.2, 0.0, abs(pos.y - scanHeight));
    pos += inNormals * scanEffect * glitchAmount * 2.0;
    
    fragPosition = modelMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    
    fragNormal = normalize(vec3(modelMatrix * vec4(inNormals, 0.0)));
    fragTexCoords = inTexCoords;
}
'''


# 2. MARIO - Lava Bubbling
mario_pulse_vertex = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform float value;

float noise(vec3 p) {
    return fract(sin(dot(p, vec3(12.9898, 78.233, 45.164))) * 43758.5453);
}

void main()
{
    vec3 pos = inPosition;
    
    float bubbleAmount = mix(0.03, 0.12, value);
    
    // Múltiples octavas de ruido para movimiento orgánico
    float n1 = noise(pos * 5.0 + time * 0.5);
    float n2 = noise(pos * 10.0 - time * 0.8);
    float n3 = noise(pos * 20.0 + time * 1.2);
    
    float bubbleRise = sin(pos.y * 8.0 - time * 2.0) * n1 * bubbleAmount;
    
    pos += inNormals * (n1 * n2 * bubbleAmount * 2.0);
    pos.y += bubbleRise;
    
    float heatWave = sin(pos.x * 10.0 + time * 3.0) * cos(pos.z * 8.0 - time * 2.5);
    pos += inNormals * heatWave * bubbleAmount * 0.5;
    
    float heatPulse = sin(time * 1.5) * 0.02 + 1.0;
    pos *= heatPulse;
    
    fragPosition = modelMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    
    fragNormal = normalize(vec3(modelMatrix * vec4(inNormals, 0.0)));
    fragTexCoords = inTexCoords;
}
'''


# 3. METAL SONIC - Liquid Metal Morphing
metal_sonic_spin_vertex = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform float value;

void main()
{
    vec3 pos = inPosition;
    
    float morphAmount = mix(0.03, 0.15, value);
    
    float wave1 = sin(pos.y * 15.0 - time * 4.0);
    float wave2 = cos(pos.x * 12.0 + time * 3.5);
    float wave3 = sin(pos.z * 10.0 - time * 5.0);
    
    // Flujo líquido combinando ondas
    float liquidFlow = (wave1 + wave2 + wave3) / 3.0;
    pos += inNormals * liquidFlow * morphAmount;
    
    float spinAngle = time * 0.5;
    float s = sin(spinAngle);
    float c = cos(spinAngle);
    
    float newX = pos.x * c - pos.z * s * 0.3;
    float newZ = pos.x * s * 0.3 + pos.z * c;
    pos.x = newX;
    pos.z = newZ;
    
    float vibration = sin(time * 20.0 + pos.x * 50.0) * sin(time * 18.0 + pos.y * 45.0);
    pos += inNormals * vibration * 0.002 * value;
    
    float energyPulse = sin(time * 2.0) * 0.02 + 1.0;
    pos *= energyPulse;
    
    fragPosition = modelMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    
    // Normales ajustadas para el flow
    vec3 modifiedNormal = inNormals + vec3(wave2, wave1, wave3) * 0.3;
    
    fragNormal = normalize(vec3(modelMatrix * vec4(modifiedNormal, 0.0)));
    fragTexCoords = inTexCoords;
}
'''


# 4. CAPTAIN FALCON - Shockwave Expansion
falcon_aura_vertex = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform float value;

void main()
{
    vec3 pos = inPosition;
    
    float shockAmount = mix(0.04, 0.15, value);
    float dist = length(pos);
    
    // Múltiples ondas expansivas desde el centro
    float shockwave1 = sin(dist * 10.0 - time * 5.0) * shockAmount;
    float shockwave2 = sin(dist * 15.0 - time * 7.0 + 1.5) * shockAmount * 0.7;
    float shockwave3 = sin(dist * 20.0 + time * 4.0) * shockAmount * 0.5;
    
    float totalShock = shockwave1 + shockwave2 + shockwave3;
    
    float energyPulse = sin(time * 2.5) * 0.05 + 1.0;
    pos *= energyPulse;
    pos += inNormals * totalShock;
    
    float electricShake = sin(time * 25.0) * cos(time * 22.0);
    pos += inNormals * electricShake * 0.01 * value;
    
    float flowY = sin(pos.y * 10.0 + time * 8.0) * 0.02 * value;
    pos.x += flowY;
    pos.z += cos(pos.y * 8.0 - time * 6.0) * 0.02 * value;
    
    fragPosition = modelMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    
    fragNormal = normalize(vec3(modelMatrix * vec4(inNormals, 0.0)));
    fragTexCoords = inTexCoords;
}
'''


# 5. PAC-MAN - Portal Vortex
pacman_bounce_vertex = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform float value;

void main()
{
    vec3 pos = inPosition;
    
    float vortexAmount = mix(0.05, 0.2, value);
    float distFromAxis = length(pos.xz);
    float angle = atan(pos.z, pos.x);
    
    // Rotación espiral con succión
    float spiralSpeed = time * 2.0 + distFromAxis * 3.0;
    float newAngle = angle + spiralSpeed;
    
    float suctionForce = sin(time * 3.0) * 0.1 + 0.9;
    float newDist = distFromAxis * suctionForce;
    
    pos.x = cos(newAngle) * newDist;
    pos.z = sin(newAngle) * newDist;
    
    float verticalWave = sin(distFromAxis * 8.0 - time * 4.0) * vortexAmount;
    pos.y += verticalWave;
    
    float portalPulse = sin(time * 2.0 + distFromAxis * 5.0) * vortexAmount;
    pos += inNormals * portalPulse;
    
    float portalScale = sin(time * 1.5) * 0.05 + 1.0;
    pos *= portalScale;
    
    // Torsión helicoidal
    float twistAngle = pos.y * 2.0 + time;
    float ts = sin(twistAngle * 0.2);
    float tc = cos(twistAngle * 0.2);
    float twistedX = pos.x * tc - pos.z * ts;
    float twistedZ = pos.x * ts + pos.z * tc;
    pos.x = twistedX;
    pos.z = twistedZ;
    
    fragPosition = modelMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    
    fragNormal = normalize(vec3(modelMatrix * vec4(inNormals, 0.0)));
    fragTexCoords = inTexCoords;
}
'''


# 6. LITTLE MAC - X-Ray Scan Slicing
littlemac_punch_vertex = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform float value;

void main()
{
    vec3 pos = inPosition;
    
    float scanAmount = mix(0.05, 0.2, value);
    
    // Plano de escaneo vertical animado
    float scanPlane = sin(time * 1.0) * 2.0;
    float distToScan = abs(pos.y - scanPlane);
    
    // Separación de capas al pasar el scan
    float layerSeparation = smoothstep(0.3, 0.0, distToScan) * scanAmount;
    
    if (pos.y > scanPlane) {
        pos.y += layerSeparation;
    } else {
        pos.y -= layerSeparation;
    }
    
    float scanExpand = smoothstep(0.2, 0.0, distToScan) * 0.1;
    pos.x *= (1.0 + scanExpand);
    pos.z *= (1.0 + scanExpand);
    
    float ripple = sin(distToScan * 20.0 - time * 10.0) * 
                   smoothstep(0.5, 0.0, distToScan) * 0.02;
    pos += inNormals * ripple;
    
    float dataVibration = sin(time * 30.0 + pos.y * 50.0) * 0.002 * value;
    pos.x += dataVibration;
    pos.z += dataVibration;
    
    float glitchZone = smoothstep(0.15, 0.05, distToScan);
    float glitchOffset = sin(time * 100.0) * glitchZone * 0.01;
    pos.x += glitchOffset;
    
    fragPosition = modelMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    
    fragNormal = normalize(vec3(modelMatrix * vec4(inNormals, 0.0)));
    fragTexCoords = inTexCoords;
}
'''
