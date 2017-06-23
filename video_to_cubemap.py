from OpenGL import GL
from OpenGL import GLU
from OpenGL import GLUT
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

import numpy as np

import imageio
import argparse


def TexFromArray(img_data):
    sx, sy = img_data.shape[:2]
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, sy, sx, 0, GL.GL_RGB,
                    GL.GL_UNSIGNED_BYTE, img_data)


class QuadRenderer():
    def __init__(self, size=(1200, 900)):
        GLUT.glutInit([])
        GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB |
                                 GLUT.GLUT_DEPTH)
        GLUT.glutInitWindowSize(*size)
        GLUT.glutInitWindowPosition(0, 0)
        GLUT.glutCreateWindow("Render")
        self.size = size

        # Create the VBO
        vertices = np.array([
            [1, 1, 0, 1, 1],
            [1, -1, 0, 1, 0],
            [-1, -1, 0, 0, 0],
            [-1, 1, 0, 0, 1]], dtype='f')
        self.vertexPositions = vbo.VBO(vertices)

        # Create the index buffer object
        indices = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.int32)
        self.indexPositions = vbo.VBO(indices,
                                      target=GL.GL_ELEMENT_ARRAY_BUFFER)

        # Now create the shaders
        VERTEX_SHADER = shaders.compileShader("""
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
        """, GL.GL_VERTEX_SHADER)
        fragment_shader_text = open('./fragment-shader-cubemap.glsl').read()
        FRAGMENT_SHADER = shaders.compileShader(fragment_shader_text,
                                                GL.GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)
        self.create_texture()

    def create_texture(self):
        texture = GL.glGenTextures(1)
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)

        # Texture parameters are part of the texture object, so you need to
        # specify them only once for a given texture object.
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER,
                           GL.GL_LINEAR)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER,
                           GL.GL_LINEAR)
        GL.glUseProgram(self.shader)
        self.indexPositions.bind()
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
        TexFromArray(frame)
        GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, None)

    def render_to_image(self, frame):
        self.render(frame)
        buff = GL.glReadPixels(0, 0, self.size[0], self.size[1], GL.GL_RGB,
                               GL.GL_UNSIGNED_BYTE)
        image_array = np.fromstring(buff, np.uint8)
        image = image_array.reshape(self.size[1], self.size[0], 3)
        return np.flipud(image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= 'Cube-map to equiretangular \
                                     conversor.')
    parser.add_argument('--input', type=str, required=True,
                        help='Equiretangular video to be converted.')
    parser.add_argument('--output', type=str, dest='output',
                        help='Output cube-map video.', required=True)
    parser.add_argument('--width', type=int, default=512 * 3, dest='width',
                        help='Cube-map video total width')
    parser.add_argument('--height', type=int, default=512 * 2, dest='height',
                        help='Cube-map video total height')
    args = parser.parse_args()

    reader = imageio.get_reader(args.input)
    metadata = reader.get_meta_data()

    renderer = QuadRenderer((args.width, args.height))
    if "fps" in metadata:
        # Handle videos
        fps = metadata["fps"]
        with imageio.get_writer(args.output, fps=fps) as video_writer:
            for i, frame in enumerate(reader):
                img = renderer.render_to_image(np.asarray(frame))
                video_writer.append_data(img)
    else:
        # Handle images
        with imageio.get_writer(args.output) as writer:
            frame = reader.get_data(0)
            img = renderer.render_to_image(np.asarray(frame))
            writer.append_data(img)
