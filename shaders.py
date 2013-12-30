import OpenGL 
OpenGL.ERROR_ON_COPY = True 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *


def generateShaders():
	return compileProgram(
        compileShader('''
			// Application to vertex shader
			varying vec4 color ; 
			varying vec3 mynormal ; 
			varying vec4 myvertex ; 

			void main() {
			    gl_TexCoord[0] = gl_MultiTexCoord0 ; 
			    gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex ; 
			    color = gl_Color ; 
			    mynormal = gl_Normal ; 
			    myvertex = gl_Vertex ; 

			}
 
        ''',GL_VERTEX_SHADER),
        compileShader('''
			// Application to fragment shader
			varying vec4 color ;
			varying vec3 mynormal ; 
			varying vec4 myvertex ;
			uniform int isTex ;
			uniform sampler2D tex;

			uniform int isBump;
			uniform sampler2D normalTexture;

			const int numLights = 10 ; 
			uniform bool enablelighting ; // are we lighting at all (global).
			uniform vec4 lightposn[numLights] ; // positions of lights 
			uniform vec4 lightcolor[numLights] ; // colors of lights
			uniform int numused ;               // number of lights used

			uniform vec4 ambient ; 
			uniform vec4 diffuse ; 
			uniform vec4 specular ; 
			uniform vec4 emission ; 
			uniform float shininess ; 

			void main (void) 
			{
			    if(isTex > 0){
			       gl_FragColor = texture2D(tex, gl_TexCoord[0].st);
			 	} else if (enablelighting) { 
			        
			        vec4 finalcolor ; 

			        // Implementation of Fragment Shader
			        
			        finalcolor = ambient + emission;
			        
			        const vec3 eyepos = vec3(0,0,0) ; 
					vec4 _mypos = gl_ModelViewMatrix * myvertex ; 
					vec3 mypos = _mypos.xyz / _mypos.w ;
					vec3 eyedir = normalize(eyepos - mypos) ;

					vec3 normal = normalize((gl_ModelViewMatrixInverseTranspose*vec4(mynormal,0.0)).xyz) ; 

			        if(isBump > 0){
			            normal = 2.0 * texture2D (normalTexture, gl_TexCoord[0].st).rgb - 1.0;
			            normal = normalize (normal);
			        }
			        
			        //Iterate through all lights
			        for(int i = 0; i < numused; i++){
			        
			            //Decalare variables that will be used for computation
			            vec3 direction;
			            vec3 halfVec;
			            vec4 lightColor = lightcolor[i];
			        
			            //Directional lights
			            if(lightposn[i][3] == 0.0){
			                vec3 currentPos = lightposn[i].xyz;
			                direction = normalize(currentPos);
			                halfVec = normalize(direction + eyedir);
			            }
			            
			            //Point lights
			            else{
			                vec4 currentPos = lightposn[i];
			                vec3 position = currentPos.xyz / currentPos.w;
			                direction = normalize(position - mypos);
			                halfVec = normalize(direction + eyedir);
			            }
			            
			            //Lambert
			            float nDotL = dot(normal, direction);
			            vec4 lambert = diffuse * lightColor * max(nDotL, 0.0);
			            
			            //Phong
			            float nDotH = dot(normal, halfVec);
			            vec4 phong = specular * lightColor * pow(max(nDotH, 0.0), shininess);
			            
			            vec4 lightContribution = lambert + phong;
			            
			            finalcolor += lightContribution;
			        }
			        
				gl_FragColor = finalcolor;
			    }

			}
    	''',GL_FRAGMENT_SHADER),
		)