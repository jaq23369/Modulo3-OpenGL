vertex_postProcess = '''
#version 430

out vec2 fragTexCoords;

const vec2 pos[4] = vec2[](
	vec2(-1.0, -1.0),
	vec2( 1.0, -1.0),
	vec2( 1.0,  1.0),
	vec2(-1.0,  1.0)
);

void main()
{
	gl_Position = vec4( pos[gl_VertexID], 0.0, 1.0);
	fragTexCoords = ( pos[gl_VertexID] + 1 ) / 2;
}

'''

none_postProcess = '''
#version 430

in vec2 fragTexCoords;

uniform sampler2D frameBuffer;

out vec4 fragColor;

void main(){
	fragColor = texture(frameBuffer, fragTexCoords);
}

'''

grayScale_postProcess = '''
#version 430

in vec2 fragTexCoords;

uniform sampler2D frameBuffer;

out vec4 fragColor;

void main(){
	vec4 color = texture(frameBuffer, fragTexCoords);
	float gray = dot(color.rgb, vec3(0.3, 0.6, 0.1) );
	fragColor = vec4(gray, gray, gray, 1.0);
}

'''

negative_postProcess = '''
#version 430

in vec2 fragTexCoords;

uniform sampler2D frameBuffer;

out vec4 fragColor;

void main(){
	fragColor = 1 - texture(frameBuffer, fragTexCoords);
}

'''

hurt_postProcess = '''
#version 430

in vec2 fragTexCoords;

uniform sampler2D frameBuffer;
uniform float time;

out vec4 fragColor;

void main(){
	vec3 color = texture(frameBuffer, fragTexCoords).rgb;

	vec2 centered = fragTexCoords * 2.0 - 1.0;
	float dist = length(centered);
	float vignetteStrength = smoothstep(sin(time * 5) * 0.1 + 0.6, 1.0, dist) * 0.5;
	vec3 redTint = vec3(1.0, 0.0, 0.0);

	color = mix(color, redTint, vignetteStrength);

	fragColor = vec4(color, 1.0);

}

'''

depth_postProcess = '''
#version 430

in vec2 fragTexCoords;

uniform sampler2D frameBuffer;
uniform sampler2D depthTexture;

out vec4 fragColor;

void main(){
	float depth = texture(depthTexture, fragTexCoords).r;

	depth = 1 - depth;
	depth = clamp(depth, 0.0, 0.1) * 10;

	fragColor = vec4(vec3(depth), 1.0);
}

'''

fog_postProcess = '''
#version 430

in vec2 fragTexCoords;

uniform sampler2D frameBuffer;
uniform sampler2D depthTexture;

out vec4 fragColor;

void main(){
	vec3 color = texture(frameBuffer, fragTexCoords).rgb;
	float depth = texture(depthTexture, fragTexCoords).r;

	depth = 1 - depth;
	depth = clamp(depth, 0.0, 0.1) * 10;

	vec3 fogColor = vec3(0.5,0.5,0.5);
	color = mix(fogColor, color, depth);

	fragColor = vec4(color, 1.0);
}

'''

dof_postProcess = '''
#version 430 core

in vec2 fragTexCoords;

uniform sampler2D frameBuffer;
uniform sampler2D depthTexture;

out vec4 fragColor;

void main() {
    vec2 texelSize = 1.0 / vec2(textureSize(frameBuffer,0));
    float depth = texture(depthTexture, fragTexCoords).r;
    depth = clamp(depth,0.0, 0.1) * 10;

    vec3 color = vec3(0.0);
    int samples = 0;
    for(int x=-1;x<=1;x++){
        for(int y=-1;y<=1;y++){
            vec2 offset = vec2(x,y) * texelSize * depth * 2;
            color += texture(frameBuffer, fragTexCoords+offset).rgb;
            samples++;
        }
    }
    color /= float(samples);

    fragColor = vec4(color, 1.0);
}
'''

edgeDetection_postProcess = '''
#version 430 core

in vec2 fragTexCoords;

uniform sampler2D frameBuffer;
uniform sampler2D depthTexture;

out vec4 fragColor;

float depthAt(vec2 uv) { return texture(depthTexture, uv).r; }

void main()
{
    vec2 texelSize = 5 / vec2(textureSize(depthTexture,0));
    float depthC = texture(depthTexture, fragTexCoords).r;
    float depthL = texture(depthTexture, fragTexCoords + vec2(-texelSize.x,0)).r;
    float depthR = texture(depthTexture, fragTexCoords + vec2(texelSize.x,0)).r;
    float depthU = texture(depthTexture, fragTexCoords + vec2(0,texelSize.y)).r;
    float depthD = texture(depthTexture, fragTexCoords + vec2(0,-texelSize.y)).r;

    float edge = abs(depthL-depthR) + abs(depthU-depthD);
    edge *= 5.0;
    fragColor = vec4(vec3(edge),1.0);
}
'''

outline_postProcess = '''
#version 430 core

in vec2 fragTexCoords;

uniform sampler2D frameBuffer;
uniform sampler2D depthTexture;

out vec4 fragColor;

void main() {
    vec2 texelSize = 3.0 / vec2(textureSize(depthTexture,0));
    float depthC = texture(depthTexture, fragTexCoords).r;
    float depthL = texture(depthTexture, fragTexCoords + vec2(-texelSize.x,0)).r;
    float depthR = texture(depthTexture, fragTexCoords + vec2(texelSize.x,0)).r;
    float depthU = texture(depthTexture, fragTexCoords + vec2(0,texelSize.y)).r;
    float depthD = texture(depthTexture, fragTexCoords + vec2(0,-texelSize.y)).r;

    float edge = abs(depthL-depthR) + abs(depthU-depthD);
    edge *= 5.0;
    if(edge > 0.01)
    {
        fragColor = vec4(0.0,0.0,0.0,1.0);
    }
    else
    {
        fragColor = texture(frameBuffer, fragTexCoords);
    }
}
'''
# Post-processing utilizados en el proyecto
cinematicBloom_postProcess = '''
#version 430 core

in vec2 fragTexCoords;

uniform sampler2D frameBuffer;
uniform float time;

out vec4 fragColor;

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

vec3 sampleBloom(vec2 uv, float radius) {
    vec3 bloom = vec3(0.0);
    vec2 texelSize = 1.0 / vec2(textureSize(frameBuffer, 0));
    
    // Blur gaussiano 9x9 con pesos exponenciales
    float totalWeight = 0.0;
    for(int x = -4; x <= 4; x++) {
        for(int y = -4; y <= 4; y++) {
            vec2 offset = vec2(x, y) * texelSize * radius;
            float weight = exp(-length(vec2(x, y)) * 0.5);
            bloom += texture(frameBuffer, uv + offset).rgb * weight;
            totalWeight += weight;
        }
    }
    return bloom / totalWeight;
}

vec3 colorGrade(vec3 color) {
    color = pow(color, vec3(0.95));
    
    float brightness = 1.08;
    float contrast = 1.15;
    float saturation = 1.25;
    
    color *= brightness;
    color = (color - 0.5) * contrast + 0.5;
    
    float luminance = dot(color, vec3(0.299, 0.587, 0.114));
    color = mix(vec3(luminance), color, saturation);
    
    vec3 warmTint = vec3(1.05, 1.0, 0.95);
    color *= warmTint;
    
    // Tone mapping Reinhard
    color = color / (color + vec3(1.0));
    
    return color;
}

void main() {
    vec3 color = texture(frameBuffer, fragTexCoords).rgb;
    
    // Extracción de áreas brillantes (threshold 0.7)
    vec3 bright = max(color - 0.7, 0.0) * 2.5;
    vec3 bloom = sampleBloom(fragTexCoords, 2.0) * bright;
    
    color += bloom * 0.6;
    
    color = colorGrade(color);
    
    vec2 centered = fragTexCoords * 2.0 - 1.0;
    float vignette = 1.0 - dot(centered, centered) * 0.25;
    vignette = smoothstep(0.4, 1.0, vignette);
    color *= vignette;
    
    // Film grain animado
    float grain = hash(fragTexCoords + fract(time)) * 0.015;
    color += grain;
    
    // Gamma correction (sRGB)
    color = pow(color, vec3(1.0 / 2.2));
    
    fragColor = vec4(color, 1.0);
}
'''

retroNeonWave_postProcess = '''
#version 430 core

in vec2 fragTexCoords;

uniform sampler2D frameBuffer;
uniform float time;

out vec4 fragColor;

vec3 chromaticAberration(vec2 uv, float amount) {
    vec2 texelSize = 1.0 / vec2(textureSize(frameBuffer, 0));
    
    // Separación RGB para efecto retro
    float r = texture(frameBuffer, uv + vec2(amount, 0) * texelSize).r;
    float g = texture(frameBuffer, uv).g;
    float b = texture(frameBuffer, uv - vec2(amount, 0) * texelSize).b;
    
    return vec3(r, g, b);
}

vec3 neonGradient(vec3 color) {
    float luma = dot(color, vec3(0.299, 0.587, 0.114));
    
    vec3 cyan = vec3(0.0, 0.8, 1.0);
    vec3 magenta = vec3(1.0, 0.0, 0.8);
    vec3 yellow = vec3(1.0, 0.9, 0.0);
    vec3 purple = vec3(0.6, 0.0, 1.0);
    
    // Gradient mapping a paleta neón (púrpura→magenta→cyan→amarillo)
    vec3 neonColor;
    if(luma < 0.25) {
        neonColor = mix(purple, magenta, luma * 4.0);
    } else if(luma < 0.5) {
        neonColor = mix(magenta, cyan, (luma - 0.25) * 4.0);
    } else if(luma < 0.75) {
        neonColor = mix(cyan, yellow, (luma - 0.5) * 4.0);
    } else {
        neonColor = mix(yellow, vec3(1.0), (luma - 0.75) * 4.0);
    }
    
    return mix(color, neonColor, 0.4);
}

vec3 applyBloom(vec2 uv, vec3 color) {
    vec3 bloom = vec3(0.0);
    vec2 texelSize = 1.0 / vec2(textureSize(frameBuffer, 0));
    
    for(int x = -3; x <= 3; x++) {
        for(int y = -3; y <= 3; y++) {
            vec2 offset = vec2(x, y) * texelSize * 2.5;
            vec3 texSample = texture(frameBuffer, uv + offset).rgb;
            float weight = exp(-length(vec2(x, y)) * 0.6);
            bloom += max(texSample - 0.6, 0.0) * weight;
        }
    }
    
    return color + bloom * 0.8;
}

void main() {
    vec2 uv = fragTexCoords;
    
    // Scan lines tipo CRT (540 líneas animadas)
    float scanline = sin(uv.y * 540.0 + time * 2.0) * 0.04 + 0.96;
    
    // Wave distortion horizontal
    float wave = sin(uv.y * 8.0 - time * 1.5) * 0.005;
    uv.x += wave;
    
    vec3 color = chromaticAberration(uv, 2.5);
    
    color = neonGradient(color);
    
    color = applyBloom(uv, color);
    
    // Edge glow pulsante (púrpura)
    float pulse = sin(time * 3.0) * 0.1 + 0.9;
    vec2 centered = uv * 2.0 - 1.0;
    float edgeGlow = 1.0 - length(centered) * 0.7;
    edgeGlow = pow(edgeGlow, 2.0);
    color += vec3(0.2, 0.0, 0.4) * edgeGlow * pulse * 0.3;
    
    color *= scanline;
    
    float contrast = 1.3;
    float saturation = 1.4;
    color = (color - 0.5) * contrast + 0.5;
    float luma = dot(color, vec3(0.299, 0.587, 0.114));
    color = mix(vec3(luma), color, saturation);
    
    vec2 vignetteUV = uv * 2.0 - 1.0;
    float vignette = 1.0 - dot(vignetteUV, vignetteUV) * 0.35;
    vignette = smoothstep(0.3, 1.0, vignette);
    color *= vignette;
    
    // Flicker de 60Hz tipo monitor CRT
    float flicker = sin(time * 60.0) * 0.005 + 0.995;
    color *= flicker;
    
    color = pow(color, vec3(1.0 / 2.2));
    
    fragColor = vec4(color, 1.0);
}
'''
