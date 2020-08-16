import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Объявляем все глобальные переменные
global xrot  # Величина вращения по оси x
global yrot  # Величина вращения по оси y
global ambient  # рассеянное освещение
global greencolor  # Цвет елочных иголок
global treecolor  # Цвет елочного стебля
global lightpos  # Положение источника освещения


# Процедура перерисовки
def draw():
    global xrot
    global yrot
    global lightpos
    global greencolor
    global treecolor
    global window

    glClear(GL_COLOR_BUFFER_BIT)  # Очищаем экран и заливаем серым цветом
    glPushMatrix()  # Сохраняем текущее положение "камеры"
    glRotatef(xrot, 1.0, 0.0, 0.0)  # Вращаем по оси X на величину xrot
    glRotatef(yrot, 0.0, 1.0, 0.0)  # Вращаем по оси Y на величину yrot
    glLightfv(GL_LIGHT0, GL_POSITION, lightpos)  # Источник света вращаем вместе с елкой

    # # Рисуем ствол елки
    # triangle = [-0.5, -0.5, 0.0,
    #             0.5, -0.5, 0.0,
    #             0.0, 0.5, 0.0]
    #
    # VBO = glGenBuffers(1)
    # glBindBuffer(GL_ARRAY_BUFFER, VBO)
    # glBufferData(GL_ARRAY_BUFFER, 36, triangle, GL_STATIC_DRAW)



    glPopMatrix()


# Процедура инициализации
def init():
    global xrot  # Величина вращения по оси x
    global yrot  # Величина вращения по оси y
    global ambient  # Рассеянное освещение
    global greencolor  # Цвет елочных иголок
    global treecolor  # Цвет елочного ствола
    global lightpos  # Положение источника освещения
    global window

    xrot = 0.0  # Величина вращения по оси x = 0
    yrot = 0.0  # Величина вращения по оси y = 0
    ambient = (1.0, 1.0, 1.0, 1)  # Первые три числа цвет в формате RGB, а последнее - яркость
    greencolor = (0.2, 0.8, 0.0, 0.8)  # Зеленый цвет для иголок
    treecolor = (0.9, 0.6, 0.3, 0.8)  # Коричневый цвет для ствола
    lightpos = (1.0, 1.0, 1.0)  # Положение источника освещения по осям xyz

    glClearColor(0.5, 0.5, 0.5, 1.0)  # Серый цвет для первоначальной закраски
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)  # Определяем границы рисования по горизонтали и вертикали
    glRotatef(-90, 1.0, 0.0, 0.0)  # Сместимся по оси Х на 90 градусов
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient)  # Определяем текущую модель освещения
    glEnable(GL_LIGHTING)  # Включаем освещение
    glEnable(GL_LIGHT0)  # Включаем один источник света
    glLightfv(GL_LIGHT0, GL_POSITION, lightpos)  # Определяем положение источника света


if __name__ == '__main__':
    global window

    # Initialize the library
    if not glfw.init():
        print("Can not init the module")

    width, heigth = 800, 600
    window = glfw.create_window(width, heigth, "Hello world", None, None)

    if not window:
        glfw.terminate()

    # Make the window's context current
    glfw.make_context_current(window)

    init()
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render here, e.g. using pyOpenGL
        draw()
        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()
