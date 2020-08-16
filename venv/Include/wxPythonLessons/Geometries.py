import OpenGL.GL.shaders
import OpenGL.GL as gl
import numpy as np
from pyrr import Matrix44


class Geometries():
    def __init__(self):
        # These method create vertex view of triangle, quad and cube.
        # They create new fields in object
        self._triangle()
        self._quad()
        self._cube()

    def _triangle(self):
        """
        # These method create vertex view of triangle
        # They create new fields in object
        # Comments have at _triangle() method.
        :return:
        """
        # vertices(x,y,z) and its color(RGB)
        triangle = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                    0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                    0.0, 0.5, 0.0, 0.0, 0.0, 1.0]
        self.tv_count = len(triangle) // 6 # triangle vertex count = 3
        triangle = np.array(triangle, dtype=np.float32)

        # vertex array object
        self.vao_triangle = gl.glGenVertexArrays(1)
        # Bind the vertex array
        gl.glBindVertexArray(self.vao_triangle)
        # vertex buffered object. May be we give parametr - count of buffers
        vbo_triangle = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_triangle)
        # type and size in bites (72 = 6x3x 4bites in 1 real number)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, len(triangle) * 4, triangle, gl.GL_STATIC_DRAW)

        # zero from the string 13 'in layout(location = 0) vec3 positions;'
        # 3 vertex coor
        # normilase = false
        # next vertex position in bites 0,24,48 (number of cell), because in row 6 values(24 = 6x4)
        # gl.ctypes.c_void_p(0) - number of bites in array there begining the vertex
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 24, gl.ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        # zero from the string 14 'in layout(location = 1) vec3 colors;'
        # 3 vertex coor and eash of them have a color
        # normilase = false
        # next color position in bites 0,24,48 (number of cell), because in row 6 values(24 = 6x4)
        # gl.ctypes.c_void_p(12) - number of bites in array there begining the color
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 24, gl.ctypes.c_void_p(12))
        gl.glEnableVertexAttribArray(1)
        # unbind triangle vao
        gl.glBindVertexArray(0)

    def _quad(self):
        """
        # These method create vertex view of quad
        # They create new fields in object
        # Comments have at _triangle() method.
        :return:
       """
        # The quad vertex Array object
        # quad  vertexes         colors
        quad = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                -0.5, 0.5, 0.0, 0.0, 0.0, 1.0,
                0.5, 0.5, 0.0, 1.0, 1.0, 1.0]
        # quad vertex count = 4
        self.qv_count = len(quad) // 6

        quad = np.array(quad, dtype=np.float32)
        self.vao_quad = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao_quad)

        vbo_quad = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_quad)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, len(quad) * 4, quad, gl.GL_STATIC_DRAW)
        # vertex attribute pointers
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 24, gl.ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)
        # color attribute pointers
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 24, gl.ctypes.c_void_p(12))
        gl.glEnableVertexAttribArray(1)
        gl.glBindVertexArray(0)

    def _cube(self):
        """
        # These method create vertex view of cube
        # They create new fields in object
        # Comments have at _triangle() method.
        :return:
        """
        # The ube array object
        # cube      vertexes    colors
        cube = [-0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
                0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
                0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
                -0.5, 0.5, 0.5, 1.0, 1.0, 1.0,

                -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
                0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
                0.5, 0.5, -0.5, 0.0, 0.0, 1.0,
                -0.5, 0.5, -0.5, 1.0, 1.0, 1.0,

                0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
                0.5, 0.5, -0.5, 0.0, 1.0, 0.0,
                0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
                0.5, -0.5, 0.5, 1.0, 1.0, 1.0,

                -0.5, 0.5, -0.5, 1.0, 0.0, 0.0,
                -0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
                -0.5, -0.5, 0.5, 0.0, 0.0, 1.0,
                -0.5, 0.5, 0.5, 1.0, 1.0, 1.0,

                -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
                0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
                0.5, -0.5, 0.5, 0.0, 0.0, 1.0,
                -0.5, -0.5, 0.5, 1.0, 1.0, 1.0,

                0.5, 0.5, -0.5, 1.0, 0.0, 0.0,
                -0.5, 0.5, -0.5, 0.0, 1.0, 0.0,
                -0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
                0.5, 0.5, 0.5, 1.0, 1.0, 1.0]

        cube = np.array(cube, dtype=np.float32)

        indexes = [0, 1, 2, 2, 3, 0,
                   4, 5, 6, 6, 7, 4,
                   8, 9, 10, 10, 11, 8,
                   12, 13, 14, 14, 15, 12,
                   16, 17, 18, 18, 19, 16,
                   20, 21, 22, 22, 23, 20]

        self.ci_count = len(indexes)  # cube indexes count

        indexes = np.array(indexes, dtype=np.uint32)
        self.vao_cube = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao_cube)
        vbo_cube = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_cube)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, len(cube) * 4, cube, gl.GL_STATIC_DRAW)

        # element buffer object
        ebo_cube = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo_cube)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize * len(indexes), indexes, gl.GL_STATIC_DRAW)
        # vertex attribute pointer
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 24, gl.ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)
        # vertex attribute pointer
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 24, gl.ctypes.c_void_p(12))
        gl.glEnableVertexAttribArray(1)
        # unbind cube vao
        gl.glBindVertexArray(0)

    def bind_triangle(self):
        """
        Just need call for drawing
        :return:
        """
        gl.glBindVertexArray(self.vao_triangle)

    def bind_quad(self):
        gl.glBindVertexArray(self.vao_quad)

    def bind_cube(self):
        gl.glBindVertexArray(self.vao_cube)


class A():
    pass
