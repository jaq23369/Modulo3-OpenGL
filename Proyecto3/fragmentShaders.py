# GLSL

fragment_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max( 0 , dot(fragNormal, lightDir)) + ambientLight;

    fragColor = texture(tex0, fragTexCoords) * intensity;
}

'''


toon_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max( 0 , dot(fragNormal, lightDir)) + ambientLight;

    if (intensity < 0.33)
        intensity = 0.2;
    else if (intensity < 0.66)
        intensity = 0.6;
    else
        intensity = 1.0;

    fragColor = texture(tex0, fragTexCoords) * intensity;
}

'''


negative_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;

void main()
{
    fragColor = 1 - texture(tex0, fragTexCoords);
}

'''


magma_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform sampler2D tex1;

uniform vec3 pointLight;
uniform float ambientLight;

uniform float time;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max( 0 , dot(fragNormal, lightDir)) + ambientLight;

    fragColor = texture(tex0, fragTexCoords) * intensity;
    fragColor += texture(tex1, fragTexCoords) * ((sin(time) + 1) / 2);
}

'''


hologram_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform float time;
uniform vec3 pointLight;

void main()
{
    
    vec3 hologramColor = vec3(0.0, 0.8, 1.0);
    
    
    vec4 texColor = texture(tex0, fragTexCoords);
    
    
    float stripes = sin(fragPosition.y * 20.0 + time * 3.0);
    stripes = smoothstep(0.3, 0.7, stripes);
    
    
    vec3 viewDir = normalize(pointLight - fragPosition.xyz);
    float fresnel = 1.0 - max(0.0, dot(fragNormal, viewDir));
    fresnel = pow(fresnel, 3.0);
    
    
    float flicker = sin(time * 10.0) * 0.1 + 0.9;
    
    
    vec3 finalColor = texColor.rgb * hologramColor;
    finalColor += hologramColor * fresnel * 0.8;
    finalColor *= stripes * flicker;
    
    
    float alpha = 0.7 + fresnel * 0.3;
    
    fragColor = vec4(finalColor, alpha);
}

'''


rainbow_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform float time;
uniform vec3 pointLight;
uniform float ambientLight;


vec3 rainbow(float t)
{
    vec3 color;
    color.r = sin(t) * 0.5 + 0.5;
    color.g = sin(t + 2.094) * 0.5 + 0.5;  // 2.094 = 2*PI/3
    color.b = sin(t + 4.189) * 0.5 + 0.5;  // 4.189 = 4*PI/3
    return color;
}

void main()
{
    
    vec4 texColor = texture(tex0, fragTexCoords);
    
    
    
    float stripePattern = fragPosition.y * 3.0 + time * 2.0;
    
    
    float wave = sin(fragPosition.x * 5.0 + time * 3.0) * 0.3;
    stripePattern += wave;
    
    
    vec3 rainbowColor = rainbow(stripePattern);
    
    
    vec3 finalColor = texColor.rgb * rainbowColor * 1.5;
    
    
    float pulse = sin(time * 4.0) * 0.2 + 0.8;
    finalColor *= pulse;
    
    
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0.0, dot(fragNormal, lightDir)) * 0.3 + ambientLight;
    finalColor *= (intensity + 0.7);
    
    fragColor = vec4(finalColor, 1.0);
}

'''


glitch_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform float time;
uniform vec3 pointLight;
uniform float ambientLight;


float random(vec2 st)
{
    return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

void main()
{
    vec2 uv = fragTexCoords;
    
    
    float glitchBlock = floor(uv.y * 20.0);
    float glitchTrigger = random(vec2(glitchBlock, floor(time * 3.0)));
    
    
    if(glitchTrigger > 0.92)
    {
        uv.x += (random(vec2(glitchBlock, time)) - 0.5) * 0.15;
    }
    
    
    float aberration = sin(time * 4.0) * 0.015 + 0.01;
    
    
    float r = texture(tex0, uv + vec2(aberration, 0.0)).r;
    float g = texture(tex0, uv).g;
    float b = texture(tex0, uv - vec2(aberration, 0.0)).b;
    
    vec3 texColor = vec3(r, g, b);
    
    
    float scanline = sin(uv.y * 300.0 + time * 2.0) * 0.05 + 0.95;
    
    
    float wave = sin(uv.y * 10.0 + time * 5.0) * 0.02;
    
    
    vec3 neonGlow = vec3(0.0);
    float glitchFlash = step(0.98, glitchTrigger);
    neonGlow += vec3(1.0, 0.0, 1.0) * glitchFlash * 0.5; // Magenta
    neonGlow += vec3(0.0, 1.0, 1.0) * wave * 0.3; // Cyan
    
    
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0.0, dot(fragNormal, lightDir)) * 0.6 + ambientLight;
    
    
    vec3 finalColor = texColor * intensity;
    finalColor *= scanline;
    finalColor += neonGlow;
    
    
    float pulse = sin(time * 2.5) * 0.15 + 0.85;
    finalColor *= pulse;
    
    
    finalColor = mix(vec3(dot(finalColor, vec3(0.299, 0.587, 0.114))), finalColor, 1.3);
    
    fragColor = vec4(finalColor, 1.0);
}

'''


# ══════════════════════════
# SHADERS PARA PROYECTO 3
# ══════════════════════════

# 1. YOSHI - Rainbow Shader
yoshi_toon_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;
uniform float value;

void main()
{
    vec4 texColor = texture(tex0, fragTexCoords);
    vec3 viewDir = normalize(-fragPosition.xyz);
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    
    float rainbowFactor = fragPosition.y * 2.0 + time * 0.8;
    
    // Desfase de 120° (2π/3) para generar RGB
    vec3 rainbowColor;
    rainbowColor.r = sin(rainbowFactor) * 0.5 + 0.5;
    rainbowColor.g = sin(rainbowFactor + 2.094) * 0.5 + 0.5;
    rainbowColor.b = sin(rainbowFactor + 4.189) * 0.5 + 0.5;
    
    rainbowColor = normalize(rainbowColor) * length(rainbowColor) * 1.5;
    rainbowColor = clamp(rainbowColor, 0.0, 1.0);
    
    // Efecto fresnel para bordes brillantes
    float fresnel = pow(1.0 - max(dot(viewDir, fragNormal), 0.0), 2.5);
    
    vec3 reflectDir = reflect(-lightDir, fragNormal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 64.0);
    vec3 specular = rainbowColor * spec * 2.0;
    
    float diffuse = max(0.0, dot(fragNormal, lightDir)) + ambientLight;
    float rainbowIntensity = mix(0.5, 1.0, value);
    
    vec3 finalColor = texColor.rgb * diffuse * 0.3 + rainbowColor * rainbowIntensity * 1.5;
    finalColor += rainbowColor * fresnel * 0.8;
    finalColor += specular;
    
    float pulse = sin(time * 2.0) * 0.1 + 0.9;
    finalColor *= pulse;
    
    fragColor = vec4(finalColor, 1.0);
}
'''


# 2. STAGE - Energy Shield
stage_grid_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;
uniform float value;

// Distancia a hexágono perfecto
float hexagon(vec2 p, float size) {
    vec2 q = abs(p);
    return max(abs(q.y), q.x * 0.866025 + q.y * 0.5) - size;
}

void main()
{
    vec4 texColor = texture(tex0, fragTexCoords);
    vec3 viewDir = normalize(-fragPosition.xyz);
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    
    vec2 hexPos = fragPosition.xz * 8.0;
    hexPos += vec2(sin(time * 0.5), cos(time * 0.3)) * 2.0;
    
    float hexSize = 0.3;
    float hex = hexagon(fract(hexPos) - 0.5, hexSize);
    hex = smoothstep(0.02, 0.0, hex);
    
    // Ondas de energía propagándose
    float wave = sin(hexPos.x * 3.0 + hexPos.y * 2.0 + time * 4.0) * 0.5 + 0.5;
    float energy = hex * wave;
    
    float fresnel = pow(1.0 - max(dot(viewDir, fragNormal), 0.0), 2.5);
    
    vec3 energyColor = vec3(0.2, 0.8, 1.0) * energy * 3.0;
    vec3 fresnelColor = vec3(0.4, 1.0, 1.0) * fresnel * 2.5;
    
    float pulse = sin(time * 2.0) * 0.3 + 0.7;
    
    float particles = fract(sin(dot(hexPos, vec2(12.9898, 78.233))) * 43758.5453);
    particles = step(0.98, particles) * wave;
    vec3 particleGlow = vec3(1.0, 1.0, 0.8) * particles * 5.0;
    
    float diffuse = max(0.0, dot(fragNormal, lightDir)) + ambientLight;
    float shieldIntensity = mix(0.4, 1.0, value);
    
    vec3 shieldEffect = (energyColor + fresnelColor + particleGlow) * pulse * shieldIntensity;
    vec3 finalColor = texColor.rgb * diffuse * 0.3 + shieldEffect + fresnelColor * 0.5;
    
    fragColor = vec4(finalColor, 1.0);
}
'''


# 3. MARIO - Lava/Magma
mario_fire_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;
uniform float value;

float noise(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

// Interpolación bilinear para ruido suave
float smoothNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    
    float a = noise(i);
    float b = noise(i + vec2(1.0, 0.0));
    float c = noise(i + vec2(0.0, 1.0));
    float d = noise(i + vec2(1.0, 1.0));
    
    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

void main()
{
    vec3 viewDir = normalize(-fragPosition.xyz);
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    
    vec2 uv = fragPosition.xz * 2.0 + fragPosition.yy * 0.5;
    // Ruido procedural en múltiples octavas
    float noise1 = smoothNoise(uv * 3.0 + time * 0.5);
    float noise2 = smoothNoise(uv * 6.0 - time * 0.8) * 0.5;
    float noise3 = smoothNoise(uv * 12.0 + time * 1.2) * 0.25;
    float lavaPattern = noise1 + noise2 + noise3;
    
    vec2 distortion = vec2(
        sin(fragPosition.y * 8.0 + time * 4.0 + lavaPattern * 10.0),
        cos(fragPosition.x * 8.0 - time * 3.0 + lavaPattern * 10.0)
    ) * 0.03;
    
    vec2 distortedUV = fragTexCoords + distortion;
    vec4 texColor = texture(tex0, distortedUV);
    
    vec3 lavaColor1 = vec3(0.1, 0.0, 0.0);
    vec3 lavaColor2 = vec3(0.8, 0.1, 0.0);
    vec3 lavaColor3 = vec3(1.0, 0.4, 0.0);
    vec3 lavaColor4 = vec3(1.0, 1.0, 0.2);
    
    // Gradiente de temperatura (negro → rojo → naranja → amarillo)
    vec3 lavaGradient;
    if (lavaPattern < 0.4) {
        lavaGradient = mix(lavaColor1, lavaColor2, lavaPattern / 0.4);
    } else if (lavaPattern < 0.7) {
        lavaGradient = mix(lavaColor2, lavaColor3, (lavaPattern - 0.4) / 0.3);
    } else {
        lavaGradient = mix(lavaColor3, lavaColor4, (lavaPattern - 0.7) / 0.3);
    }
    
    float flow = sin(fragPosition.y * 5.0 - time * 2.0 + lavaPattern * 15.0) * 0.5 + 0.5;
    lavaGradient += vec3(1.0, 0.6, 0.0) * flow * 0.4;
    
    float cracks = smoothstep(0.3, 0.35, lavaPattern);
    cracks *= smoothstep(0.7, 0.65, lavaPattern);
    vec3 crackColor = vec3(0.0) * (1.0 - cracks);
    
    float emission = pow(lavaPattern, 2.0) * 3.0;
    float diffuse = max(0.0, dot(fragNormal, lightDir)) + ambientLight;
    
    float lavaIntensity = mix(0.5, 1.0, value);
    vec3 finalColor = texColor.rgb * diffuse * 0.2 + lavaGradient * lavaIntensity + crackColor;
    finalColor += lavaGradient * emission * 0.5;
    
    float heatPulse = sin(time * 2.0) * 0.2 + 0.8;
    finalColor *= heatPulse;
    
    fragColor = vec4(finalColor, 1.0);
}
'''


# 4. METAL SONIC - Chrome Reflective
metal_sonic_metallic_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;
uniform float value;

void main()
{
    vec4 texColor = texture(tex0, fragTexCoords);
    vec3 viewDir = normalize(-fragPosition.xyz);
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    
    // Reflexión para simular entorno
    vec3 reflectDir = reflect(-viewDir, fragNormal);
    
    vec3 envColor;
    float refY = reflectDir.y;
    if (refY > 0.3) {
        envColor = vec3(0.5, 0.7, 1.0);
    } else if (refY > -0.3) {
        envColor = vec3(0.3, 0.4, 0.5);
    } else {
        envColor = vec3(0.1, 0.15, 0.2);
    }
    
    float refPattern = sin(reflectDir.x * 20.0 + time * 2.0) * 0.5 + 0.5;
    refPattern += sin(reflectDir.z * 15.0 - time * 1.5) * 0.3;
    envColor += vec3(0.8, 0.9, 1.0) * refPattern * 0.3;
    
    float fresnel = pow(1.0 - max(dot(viewDir, fragNormal), 0.0), 4.0);
    
    // Blinn-Phong con exponente alto para metal
    vec3 halfDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(fragNormal, halfDir), 0.0), 256.0);
    vec3 specular = vec3(1.0) * spec * 5.0;
    
    vec2 anisoDir = vec2(dot(fragNormal, vec3(1.0, 0.0, 0.0)), 
                         dot(fragNormal, vec3(0.0, 0.0, 1.0)));
    float aniso = sin(anisoDir.x * 30.0 + time) * sin(anisoDir.y * 25.0 - time * 0.8);
    aniso = smoothstep(0.8, 1.0, aniso);
    vec3 anisoHighlight = vec3(0.7, 0.85, 1.0) * aniso * fresnel * 2.0;
    
    float diffuse = max(0.0, dot(fragNormal, lightDir)) * 0.3 + ambientLight;
    float chromeLevel = mix(0.7, 0.98, value);
    vec3 chromeColor = envColor * (1.0 + fresnel * 2.0);
    
    vec3 finalColor = mix(texColor.rgb * diffuse, chromeColor, chromeLevel);
    finalColor += specular + anisoHighlight;
    finalColor *= vec3(0.9, 0.95, 1.0);
    
    fragColor = vec4(finalColor, 1.0);
}
'''


# 5. CAPTAIN FALCON - Plasma Energy
falcon_aura_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;
uniform float value;

// Ruido 3D para electricidad
float noise(vec3 p) {
    return fract(sin(dot(p, vec3(12.9898, 78.233, 45.164))) * 43758.5453);
}

void main()
{
    vec4 texColor = texture(tex0, fragTexCoords);
    vec3 viewDir = normalize(-fragPosition.xyz);
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    
    float fresnel = pow(1.0 - max(dot(viewDir, fragNormal), 0.0), 2.0);
    
    vec3 electricPos = fragPosition.xyz * 10.0;
    float elec1 = noise(electricPos + time * 5.0);
    float elec2 = noise(electricPos * 2.0 - time * 7.0);
    float elec3 = noise(electricPos * 4.0 + time * 3.0);
    
    // Patrón de rayos eléctricos (multiplicación de capas)
    float lightning = elec1 * elec2 * elec3;
    lightning = step(0.85, lightning);
    
    float dist = length(fragPosition.xz);
    float shockwave1 = abs(sin((dist - time * 3.0) * 10.0));
    float shockwave2 = abs(sin((dist - time * 2.5 + 1.5) * 8.0));
    shockwave1 = smoothstep(0.8, 1.0, shockwave1);
    shockwave2 = smoothstep(0.7, 1.0, shockwave2);
    
    float energyPulse = sin(fragPosition.y * 20.0 - time * 8.0) * 0.5 + 0.5;
    energyPulse *= sin(fragPosition.x * 15.0 + time * 6.0) * 0.5 + 0.5;
    energyPulse = pow(energyPulse, 3.0);
    
    vec3 plasmaBlue = vec3(0.3, 0.6, 1.0);
    vec3 plasmaPurple = vec3(0.8, 0.2, 1.0);
    vec3 plasmaWhite = vec3(1.0, 1.0, 1.0);
    
    vec3 plasmaColor = mix(plasmaBlue, plasmaPurple, energyPulse);
    plasmaColor = mix(plasmaColor, plasmaWhite, lightning);
    
    vec3 auraGlow = plasmaColor * fresnel * 3.0;
    vec3 lightningGlow = plasmaWhite * lightning * 8.0;
    vec3 shockwaveGlow = vec3(0.5, 0.8, 1.0) * (shockwave1 + shockwave2) * 2.0;
    vec3 pulseGlow = plasmaColor * energyPulse * 1.5;
    
    float diffuse = max(0.0, dot(fragNormal, lightDir)) + ambientLight;
    float plasmaIntensity = mix(0.5, 1.0, value);
    
    vec3 energyEffect = (auraGlow + lightningGlow + shockwaveGlow + pulseGlow) * plasmaIntensity;
    vec3 finalColor = texColor.rgb * diffuse * 0.3 + energyEffect;
    
    float flicker = noise(vec3(time * 10.0)) * 0.2 + 0.8;
    finalColor *= flicker;
    
    fragColor = vec4(finalColor, 1.0);
}
'''


# 6. PAC-MAN - Portal Wormhole
pacman_neon_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;
uniform float value;

void main()
{
    vec3 viewDir = normalize(-fragPosition.xyz);
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    
    vec2 center = vec2(0.5, 0.5);
    vec2 toCenter = fragTexCoords - center;
    float dist = length(toCenter);
    
    // Distorsión espacial tipo vórtice
    float angle = atan(toCenter.y, toCenter.x);
    float warpAmount = sin(dist * 15.0 - time * 3.0) * 0.1;
    angle += warpAmount * (1.0 - dist);
    
    float rotation = time * 0.5;
    vec2 warpedUV;
    warpedUV.x = cos(angle + rotation) * dist + 0.5;
    warpedUV.y = sin(angle + rotation) * dist + 0.5;
    
    vec4 texColor = texture(tex0, warpedUV);
    
    // Anillos concéntricos del portal
    float rings = sin(dist * 30.0 - time * 5.0) * 0.5 + 0.5;
    rings = pow(rings, 3.0);
    
    float spiral = sin(angle * 8.0 - dist * 20.0 + time * 4.0) * 0.5 + 0.5;
    spiral *= (1.0 - dist);
    
    float fresnel = pow(1.0 - max(dot(viewDir, fragNormal), 0.0), 3.0);
    
    vec3 portalColor1 = vec3(0.1, 0.3, 1.0);
    vec3 portalColor2 = vec3(0.6, 0.2, 1.0);
    vec3 portalColor3 = vec3(1.0, 0.3, 0.8);
    
    float colorMix = sin(dist * 10.0 - time * 2.0) * 0.5 + 0.5;
    vec3 portalGradient = mix(portalColor1, portalColor2, colorMix);
    portalGradient = mix(portalGradient, portalColor3, spiral);
    
    vec3 particlePos = fragPosition.xyz * 20.0 + time * 2.0;
    float particles = fract(sin(dot(particlePos.xy, vec2(12.9898, 78.233))) * 43758.5453);
    particles *= fract(sin(dot(particlePos.yz, vec2(39.346, 11.135))) * 22345.6789);
    particles = step(0.97, particles);
    vec3 particleGlow = vec3(1.0, 0.8, 1.0) * particles * 5.0;
    
    vec2 offset = normalize(toCenter) * warpAmount * 0.02;
    float r = texture(tex0, warpedUV + offset).r;
    float g = texture(tex0, warpedUV).g;
    float b = texture(tex0, warpedUV - offset).b;
    vec3 chromatic = vec3(r, g, b);
    
    float diffuse = max(0.0, dot(fragNormal, lightDir)) + ambientLight;
    float portalIntensity = mix(0.5, 1.0, value);
    
    vec3 portalEffect = portalGradient * (rings + spiral * 0.5 + fresnel * 2.0) * portalIntensity;
    vec3 finalColor = mix(chromatic * diffuse, portalEffect, 0.7);
    finalColor += particleGlow + portalGradient * fresnel * 0.5;
    
    float dimensionalPulse = sin(time * 2.0) * 0.2 + 0.8;
    finalColor *= dimensionalPulse;
    
    float vignette = 1.0 - dist * 0.5;
    finalColor *= vignette;
    
    fragColor = vec4(finalColor, 1.0);
}
'''


# 7. LITTLE MAC - X-Ray Wireframe
littlemac_crt_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;
uniform float value;

// Grid 3D para efecto wireframe
float wireframe(vec3 pos, float thickness) {
    vec3 grid = abs(fract(pos - 0.5) - 0.5);
    vec3 edgeDetect = smoothstep(vec3(thickness), vec3(thickness + 0.02), grid);
    return 1.0 - min(min(edgeDetect.x, edgeDetect.y), edgeDetect.z);
}

void main()
{
    vec4 texColor = texture(tex0, fragTexCoords);
    vec3 viewDir = normalize(-fragPosition.xyz);
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    
    vec3 gridPos = fragPosition.xyz * 12.0;
    float wire = wireframe(gridPos, 0.47);
    
    // Subsurface scattering simulado
    float scatter = pow(1.0 - max(dot(viewDir, fragNormal), 0.0), 2.0);
    scatter += pow(max(dot(-viewDir, fragNormal), 0.0), 1.5) * 0.5;
    
    float depth = length(fragPosition.xyz);
    float transparency = smoothstep(2.0, 8.0, depth);
    
    // Líneas de escaneo recorriendo el modelo
    float scanline = sin(fragPosition.y * 30.0 - time * 3.0) * 0.5 + 0.5;
    scanline = pow(scanline, 5.0);
    
    vec3 innerGrid = fragPosition.xyz * 20.0 + time * 0.5;
    float innerWire = wireframe(innerGrid, 0.48);
    innerWire *= scatter;
    
    vec3 xrayColor = vec3(0.2, 0.8, 1.0);
    vec3 wireColor = vec3(0.0, 1.0, 1.0);
    vec3 scanColor = vec3(0.5, 1.0, 0.5);
    vec3 innerColor = vec3(0.8, 0.3, 1.0);
    
    float fresnel = pow(1.0 - max(dot(viewDir, fragNormal), 0.0), 3.0);
    
    float edgeDetect = step(0.2, length(vec3(dFdx(fragPosition.x), 
                                             dFdy(fragPosition.y), 
                                             dFdx(fragPosition.z))));
    
    float diffuse = max(0.0, dot(fragNormal, lightDir)) + ambientLight;
    float xrayIntensity = mix(0.5, 1.0, value);
    
    vec3 baseXray = texColor.rgb * 0.3 + xrayColor * scatter * 2.0;
    baseXray = mix(baseXray, wireColor, wire * 0.8);
    baseXray += innerColor * innerWire * 0.6;
    baseXray += scanColor * scanline * 2.0;
    baseXray += wireColor * fresnel * 1.5;
    baseXray += wireColor * edgeDetect * 0.8;
    
    vec3 finalColor = baseXray * xrayIntensity;
    
    float dataGrid = fract(sin(dot(fragPosition.xy * 50.0, vec2(12.9898, 78.233))) * 43758.5453);
    dataGrid = step(0.95, dataGrid);
    finalColor += vec3(0.0, 1.0, 0.5) * dataGrid * 0.5;
    
    float pulse = sin(time * 2.0) * 0.15 + 0.85;
    finalColor *= pulse;
    finalColor = mix(finalColor, texColor.rgb * diffuse, 0.15);
    
    fragColor = vec4(finalColor, 1.0);
}
'''