

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









