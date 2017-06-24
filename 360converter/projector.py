import os
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


class Equirectangular2Cubemap():
    def __init__(self, size=(1200, 900)):
        self.size = size

        GLUT.glutInit([])
        GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB |
                                 GLUT.GLUT_DEPTH)
        GLUT.glutInitWindowSize(*size)
        GLUT.glutInitWindowPosition(0, 0)
        GLUT.glutCreateWindow("Render")

        vertex_shader_txt = """
        #version 320 es
        precision highp float;
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec2 texCoord;
        out vec2 texCoordOut;
        void main()
        {
            gl_Position = vec4(position, 1.0);
            texCoordOut = texCoord;
        }
        """
        self.vertex_shader = shaders.compileShader(vertex_shader_txt,
                                                   GL.GL_VERTEX_SHADER)

        basepath = os.path.dirname(__file__)
        shader_path = os.path.abspath(os.path.join(basepath, './fragment-shader-cubemap.glsl'))
        with open(shader_path) as fragment_shader_txt:
            self.fragment_shader = shaders.compileShader(fragment_shader_txt,
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
