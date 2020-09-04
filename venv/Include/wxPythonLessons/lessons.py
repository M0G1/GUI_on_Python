"""
GUI interface with wxPython and OpenGL from video lessons
https://www.youtube.com/watch?v=o02uw9-rRqo&list=PL1P11yPQAo7oOmiQQI35arzpVez6AxrDj&index=8
"""

import time
import sys

import wx
from view.opengl.sphere_ellipse_data3D import Sphere_Ellipse_data_3D
from wx import glcanvas
import OpenGL.GL.shaders
import OpenGL.GL as gl
from pyrr import Matrix44, matrix44, Vector3

from wxPythonLessons.Geometries import Geometries

# Shaders is running on GPU. fragment,vertecs shader
# We need to compile shader
# Some C++ code for Shaders
vertex_shader = """
# version 330

in layout(location = 0) vec3 positions;
in layout(location = 1) vec3 colors;

out vec3 newColor;
uniform mat4 rotate;
uniform mat4 translate;
uniform mat4 vp;    //view projection

void main(){
    //put worlds space into cliping space
    //put coordinat(pos) in world space
    
    //in the first rotate, secondary translate semethere
    gl_Position = vp * translate * rotate * vec4(positions, 1.0);
    newColor = colors;
}
"""

fragment_shader = """
# version 330

in vec3 newColor;
out vec4 outColor;

void main(){
    outColor = vec4(newColor, 1.0);
}
"""


class OpenGLCanvas(glcanvas.GLCanvas):
    """
    Canvas - полотно
    Canvas work with OpenGl library
    """

    def __init__(self, parent):
        self.size = (1120, 630)
        self.aspect_ratio = self.size[0] / self.size[1]  # соотношение сторон
        glcanvas.GLCanvas.__init__(self, parent, -1, size=self.size)
        # Flag of initialisation
        self.init = False
        # fields for figure continuous rotation
        self.__is_animation_start = False
        self.__animation_end = 0
        self.__animation_time_dif = 0
        # Contex where OpenGL will draw
        self.contex = glcanvas.GLContext(self)
        self.SetCurrent(self.contex)
        self.rotate = False
        self.rot_y = Matrix44.identity()
        # geometries flags
        self.show_triangle = False
        self.show_quad = False
        self.show_cube = False
        self.rot_loc = None
        # translation = shift = сдвиг
        self.trans_loc = None
        # for sliders
        self.trans_x, self.trans_y, self.trans_z = 0.0, 0.0, 0.0
        self.translate = Matrix44.identity()
        # checkBox
        self.bg_color = False
        self.wireframe = False  # wireframe - каркасный

        self.combined_matrix = Matrix44.identity()

        # OpenGL
        # bind a drawing method
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        # bind a resize method
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def OnResize(self, event):
        size = self.GetClientSize()
        # change the Viewport (Окно просмотра)
        gl.glViewport(0, 0, size.width, size.height)

    def OnPaint(self, event):
        wx.PaintDC(self)
        # Initialise the work with OpenGL
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw(event)

    def InitGL(self):

        self.mesh = Geometries()
        self.mesh.bind_triangle()
        # compile and use the shader
        shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, gl.GL_VERTEX_SHADER),
                                                  OpenGL.GL.shaders.compileShader(fragment_shader,
                                                                                  gl.GL_FRAGMENT_SHADER))
        # to set up first a view matrix
        view = matrix44.create_from_translation(Vector3([0.0, 0.0, -2.0]))
        projection = matrix44.create_perspective_projection_matrix(45.0, self.aspect_ratio, 0.1, 100.0)

        vp = matrix44.multiply(view, projection)  # view projection

        gl.glUseProgram(shader)
        gl.glEnable(gl.GL_DEPTH_TEST)

        vp_loc = gl.glGetUniformLocation(shader, "vp")
        gl.glUniformMatrix4fv(vp_loc, 1, gl.GL_FALSE, vp)

        # location of variable rotate and translate - program shader
        self.rot_loc = gl.glGetUniformLocation(shader, "rotate")
        self.trans_loc = gl.glGetUniformLocation(shader, "translate")

    def OnDraw(self, event):
        # rbga_color = (0.1, 0.15, 0.1, 1.0) dark green
        #              (0.1, 0.15, 0.1, 1.0) - black
        # set the Clear color
        if self.bg_color:
            gl.glClearColor(0.0, 0.0, 0.0, 0.0)
        else:
            gl.glClearColor(0.1, 0.15, 0.1, 1.0)

        if self.wireframe:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        else:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        # clear the Canvas and swap buffered Canvas and current
        # gl.GL_DEPTH_BUFFER_BIT for depth testing. Previously need to enable it(gl.glEnable(gl.GL_DEPTH_TEST))
        # make 3d rotation model more pleasant for eyes. U can understand the direction of rotation
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        self.translate = matrix44.create_from_translation(Vector3(
            (self.trans_x, self.trans_y, self.trans_z)
        ))

        self.combined_matrix = matrix44.multiply(self.rot_y, self.translate)

        ct = time.time()
        if self.rotate:
            if not self.__is_animation_start:
                self.__animation_time_dif += ct - self.__animation_end
                self.__is_animation_start = True

            self.rot_y = Matrix44.from_y_rotation(ct - self.__animation_time_dif)
            # upload the matrices to the shader
            gl.glUniformMatrix4fv(self.rot_loc, 1, gl.GL_FALSE, self.rot_y)
            gl.glUniformMatrix4fv(self.trans_loc, 1, gl.GL_FALSE, self.translate)
            self.Refresh()
        else:
            gl.glUniformMatrix4fv(self.rot_loc, 1, gl.GL_FALSE, self.rot_y)
            gl.glUniformMatrix4fv(self.trans_loc, 1, gl.GL_FALSE, self.translate)

            self.__animation_end = ct
            self.__is_animation_start = False

        if self.show_triangle:
            self.mesh.bind_triangle()
            # draw the triangle from array. Start from 0, end is 3. 3 vertex -> 0,1,2
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.mesh.tv_count)
        elif self.show_quad:
            self.mesh.bind_quad()
            gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, self.mesh.qv_count)
        elif self.show_cube:
            self.mesh.bind_cube()
            # unsigned int array - indexes in class Geometries, method _cube()
            gl.glDrawElements(gl.GL_TRIANGLES, self.mesh.ci_count, gl.GL_UNSIGNED_INT, None)
        else:
            self.spher = Sphere_Ellipse_data_3D(6,6)
            self.spher.draw_sphere(None)

        self.SwapBuffers()


class MyPanel(wx.Panel):
    """
        Panel class, what contain buttons, scrollbar, canvas and othet widgets
        It encapsulate some working with wx library classes
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # set light green background
        self.SetBackgroundColour("#626D58")
        # Canvas for OpenGL view
        self.canvas = OpenGLCanvas(self)
        self.rot_btn = wx.Button(self, -1, label="start/stop rotation", pos=(1130, 10), size=(105, 50))
        # BackgroundColour(RGB 0-255) is field of Button object.
        # SetBackgroundColour is method of panel.
        # Background and Foreground (задний и передний планы)
        self.rot_btn.BackgroundColour = (125, 125, 125)
        self.rot_btn.ForegroundColour = (255, 255, 255)
        # radio buttons
        self.rad_btn1 = wx.RadioButton(self, -1, label="Show Triangle", pos=(1130, 70))
        self.rad_btn2 = wx.RadioButton(self, -1, label="Show Quad", pos=(1130, 90))
        self.rad_btn3 = wx.RadioButton(self, -1, label="Show Cube", pos=(1130, 110))

        # the sliders
        # wx.SL_VERTICAL - make the slider vertial. wx.SL_AUTOTICKS - visual landmark
        self.COEFFICIENTS_SLIDERS = (-2, -2, 10)
        #######################################
        self.x_slider = wx.Slider(self, -1, pos=(1130, 180), size=(40, 150), style=wx.SL_VERTICAL | wx.SL_AUTOTICKS,
                                  value=0, minValue=-5, maxValue=5)
        self.y_slider = wx.Slider(self, -1, pos=(1170, 180), size=(40, 150), style=wx.SL_VERTICAL | wx.SL_AUTOTICKS,
                                  value=0, minValue=-5, maxValue=5)
        self.z_slider = wx.Slider(self, -1, pos=(1210, 180), size=(40, 150), style=wx.SL_VERTICAL | wx.SL_AUTOTICKS,
                                  value=0, minValue=-5, maxValue=5)

        # the slider labels using static texts
        # This doesn't need to bind! uAu
        # Font - шрифт
        font = wx.Font(14, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.x_slider_label = wx.StaticText(self, -1, label="X", pos=(1142, 155))
        self.x_slider_label.SetFont(font)
        self.y_slider_label = wx.StaticText(self, -1, label="Y", pos=(1182, 155))
        self.y_slider_label.SetFont(font)
        self.z_slider_label = wx.StaticText(self, -1, label="Z", pos=(1222, 155))
        self.z_slider_label.SetFont(font)

        # checkboxes
        self.bg_color = wx.CheckBox(self, -1, pos=(1130, 360), label="Black?")
        self.wireframe = wx.CheckBox(self, -1, pos=(1130, 390), label="Wireframe mode")

        # text control
        self.log_text = wx.TextCtrl(self, -1, size=(1120, 110), pos=(0, 630), style=wx.TE_MULTILINE)
        self.log_text.BackgroundColour = (70, 125, 70)
        self.log_text.SetFont(font)
        self.log_text.AppendText(str(self.canvas.combined_matrix.T))

        # identity button
        self.identity_btn = wx.Button(self, -1, label="set identity \nmatrix", pos=(1130, 630), size=(100, 50))
        self.identity_btn.BackgroundColour = (125, 125, 125)
        self.identity_btn.ForegroundColour = (255, 255, 255)

        # bind the callback method to the events and view element
        # Maybe it works like this, when the radio button is active. This calls the call back method
        self.Bind(wx.EVT_BUTTON, self.rotate, self.rot_btn)
        self.Bind(wx.EVT_RADIOBUTTON, self.triangle, self.rad_btn1)
        self.Bind(wx.EVT_RADIOBUTTON, self.quad, self.rad_btn2)
        self.Bind(wx.EVT_RADIOBUTTON, self.cube, self.rad_btn3)
        # if u don't give the object. Call back method will process all events of this type(EVT_SLIDER),
        # not only 1 object
        self.Bind(wx.EVT_SLIDER, self.translate)
        self.Bind(wx.EVT_CHECKBOX, self.set_bg_color, self.bg_color)
        self.Bind(wx.EVT_CHECKBOX, self.set_wireframe, self.wireframe)
        self.Bind(wx.EVT_BUTTON, self.set_identity, self.identity_btn)

    # =============================methods==============================================================================

    def set_identity(self, event):
        # identity matrix - единичная матрица
        self.canvas.combined_matrix = Matrix44.identity()
        self.canvas.rotate = False
        self.canvas.trans_x, self.canvas.trans_y, self.canvas.trans_z = 0.0, 0.0, 0.0
        self.canvas.rot_y = Matrix44.identity()
        self.x_slider.SetValue(0)
        self.y_slider.SetValue(0)
        self.z_slider.SetValue(0)
        self.log_matrix()
        self.canvas.Refresh()

    def log_matrix(self):
        self.log_text.Clear()
        self.log_text.AppendText(str(self.canvas.combined_matrix.T))

    def set_wireframe(self, event):
        # checkBox returm the boolean value(T|F)
        self.canvas.wireframe = self.wireframe.GetValue()
        self.canvas.Refresh()

    def set_bg_color(self, event):
        # checkBox returm the boolean value(T|F)
        self.canvas.bg_color = self.bg_color.GetValue()
        self.canvas.Refresh()

    def translate(self, event):
        self.canvas.trans_x = self.x_slider.GetValue() * self.COEFFICIENTS_SLIDERS[0]
        self.canvas.trans_y = self.y_slider.GetValue() * self.COEFFICIENTS_SLIDERS[1]
        self.canvas.trans_z = self.z_slider.GetValue() * self.COEFFICIENTS_SLIDERS[2]
        self.log_matrix()
        self.canvas.Refresh()

    def triangle(self, event):
        self.canvas.show_triangle = True
        self.canvas.show_quad = False
        self.canvas.show_cube = False
        self.canvas.Refresh()

    def quad(self, event):
        self.canvas.show_triangle = False
        self.canvas.show_quad = True
        self.canvas.show_cube = False
        self.canvas.Refresh()

    def cube(self, event):
        self.canvas.show_triangle = False
        self.canvas.show_quad = False
        self.canvas.show_cube = True
        self.canvas.Refresh()

    def rotate(self, event):
        # change the state
        self.canvas.rotate ^= True
        if self.canvas.rotate:
            self.canvas.Refresh()


class MyFrame(wx.Frame):
    """
        Frame class
        It encapsulate some working with wx library classes
    """

    def __init__(self):
        # size of the window
        self.size = (1280, 780)
        # create the Frame
        wx.Frame.__init__(self, None, title="My first wx frame", size=self.size,
                          style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)
        # make window not resizable
        self.SetMinSize(self.size)
        self.SetMaxSize(self.size)
        # assign processing to exit button
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.panel = MyPanel(self)

    def on_close(self, event):
        self.Destroy()
        sys.exit(0)


class MyApp(wx.App):
    """
        Application class
        It encapsulate some working with wx library classes
    """

    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True


def main_func():
    app = MyApp()
    app.MainLoop()

if __name__ == '__main__':
    main_func()
