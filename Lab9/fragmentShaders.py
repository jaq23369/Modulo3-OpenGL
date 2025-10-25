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






