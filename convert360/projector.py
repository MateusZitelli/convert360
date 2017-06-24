import numpy as np

from OpenGL import GL
from OpenGL import GLU
from OpenGL import GLUT
from OpenGL.GL import shaders
from OpenGL.arrays import vbo


def tex_from_array(img_data):
    img_data_array = np.asarray(img_data)
    sx, sy = img_data_array.shape[:2]
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, sy, sx, 0, GL.GL_RGB,
                    GL.GL_UNSIGNED_BYTE, img_data_array)


PLAIN_VERTEX_SHADER = """
#version 320 es
precision highp float;
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoord;
out vec2 texCoordOut;
void main()
{
    gl_Position = vec4(position, 1.0);
    texCoordOut = texCoord;
} """

CUBEMAP_FRAGMENT_SHADER = """
#version 320 es
#define M_PI 3.141592653589

precision highp float;
out vec4 outputColor;
in vec2 texCoordOut;
uniform vec4 quaternion;
uniform sampler2D BaseImage;

vec2 flatToSpherical(vec3 flatCoord, float r)
{
  return vec2(
      atan(flatCoord.y, flatCoord.x),
      acos(flatCoord.z / r));
}

mat3 constructCompleteRotation(vec3 a)
{
  return mat3(
      cos(a.x) * cos(a.z) - sin(a.x) * cos(a.y) * sin(a.z),
      -cos(a.x) * sin(a.z) - sin(a.x) * cos(a.y) * cos(a.z),
      sin(a.x) * sin(a.y),
      sin(a.x) * cos(a.z) + cos(a.x) * cos(a.y) * sin(a.z),
      -sin(a.x) * sin(a.z) + cos(a.x) * cos(a.y) * cos(a.z),
      -cos(a.x) * sin(a.y),
      sin(a.y) * sin(a.z),
      sin(a.y) * cos(a.z),
      cos(a.y)
      );
}

int get_face(vec2 uv){
  int x = int(floor(uv.x * 3.0));
  int y = 1 - int(floor(uv.y * 2.0));
  return y * 3 + x;
}

void main() {
  vec2 uv = texCoordOut;
  vec2 faceCoord = uv * 2.0 - 1.0;
  int face = get_face(uv);
  vec3 latSphereCoord;
  vec3 rot;

  if(face == 0){
    rot = vec3(-M_PI / 2.0, 0, 0);
  }else if(face == 1){
    rot = vec3(M_PI / 2.0, 0, 0);
  }else if(face == 2){
    rot = vec3(M_PI / 2.0, M_PI / 2.0, M_PI / 2.0);
  }else if(face == 3){
    rot = vec3(M_PI / 2.0, -M_PI / 2.0, M_PI / 2.0);
  }else if(face == 4){
    rot = vec3(M_PI, 0, 0);
  }else if(face == 5){
    rot = vec3(0, 0, 0);
  }

  latSphereCoord = vec3(1.0,
                        faceCoord.x * 3.0 + 2.0 - float(face % 3) * 2.0,
                        faceCoord.y * 2.0 - 1.0 + float(face / 3) * 2.0);

  float r = sqrt(latSphereCoord.x * latSphereCoord.x +
                latSphereCoord.y * latSphereCoord.y +
                latSphereCoord.z * latSphereCoord.z);

  vec3 rotatedCoord = latSphereCoord * constructCompleteRotation(rot);
  vec2 invRotatedSphericalCoord = flatToSpherical(rotatedCoord, r);

  vec2 finalCoordenates;
  finalCoordenates.x = (invRotatedSphericalCoord.x) / (2.0 * M_PI);
  finalCoordenates.y = (invRotatedSphericalCoord.y) / (M_PI);

  outputColor = texture(BaseImage, mod(finalCoordenates, 1.0));
} """


class Equirectangular2Cubemap():
    def __init__(self, size=(1200, 900)):
        self.size = size

        GLUT.glutInit([])
        GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB |
                                 GLUT.GLUT_DEPTH)
        GLUT.glutInitWindowSize(*size)
        GLUT.glutInitWindowPosition(0, 0)
        GLUT.glutCreateWindow("Render")

        self.vertex_shader = shaders.compileShader(PLAIN_VERTEX_SHADER,
                                                   GL.GL_VERTEX_SHADER)

        self.fragment_shader = shaders.compileShader(CUBEMAP_FRAGMENT_SHADER,
                                                     GL.GL_FRAGMENT_SHADER)

    def create_texture(self):
        self.texture = GL.glGenTextures(1)
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)

        # Texture parameters are part of the texture object, so you need to
        # specify them only once for a given texture object.
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER,
                           GL.GL_LINEAR)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER,
                           GL.GL_LINEAR)
        GL.glUseProgram(self.shader)
        self.index_positions.bind()
        self.vertexPositions.bind()

        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 20, None)
        GL.glVertexAttribPointer(1, 2, GL.GL_FLOAT, False, 20,
                                 GLU.ctypes.c_void_p(12))
        GL.glEnable(GL.GL_TEXTURE_2D)

    def render(self, frame):
        # The draw loop
        # GLUT.glutSwapBuffers()
        tex_from_array(frame)
        GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, None)

    def render_to_image(self, frame):
        self.render(frame)
        buff = GL.glReadPixels(0, 0, self.size[0], self.size[1], GL.GL_RGB,
                               GL.GL_UNSIGNED_BYTE)
        image_array = np.fromstring(buff, np.uint8)
        image = image_array.reshape(self.size[1], self.size[0], 3)
        return np.flipud(image)

    def __enter__(self):
        # Create the VBO
        vertices = np.array([
            [1, 1, 0, 1, 1],
            [1, -1, 0, 1, 0],
            [-1, -1, 0, 0, 0],
            [-1, 1, 0, 0, 1]], dtype='f')
        self.vertexPositions = vbo.VBO(vertices)

        # Create the index buffer object
        indices = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.int32)
        self.index_positions = vbo.VBO(indices,
                                       target=GL.GL_ELEMENT_ARRAY_BUFFER)
        self.shader = shaders.compileProgram(self.vertex_shader,
                                             self.fragment_shader)
        self.create_texture()
        return self

    def __exit__(self, type, value, traceback):
        self.clean()

    def clean(self):
        self.vertexPositions.delete()
        self.index_positions.delete()
        GL.glDeleteTextures(self.texture)
        GL.glDeleteTextures(self.texture)


class ProjectorNotImplemented(Exception):
    pass


projectors = {
    'equirectangular' : {
        'cubemap' : Equirectangular2Cubemap
    }
}


def get_projector(from_type, to_type):
    if from_type in projectors and to_type in projectors[from_type]:
        return projectors[from_type][to_type]
    else:
        message = "Projetor from %s to %s was not implemented" % (from_type,
                                                                  to_type)
        raise ProjectorNotImplemented(message)
