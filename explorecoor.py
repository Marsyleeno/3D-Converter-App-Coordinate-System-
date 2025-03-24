import math
import threading
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
import pygame

# Conversion Functions
def cartesian_to_spherical(x, y, z):
    r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = math.atan2(y, x)
    phi = math.acos(z / r)
    return r, math.degrees(theta), math.degrees(phi)

def spherical_to_cartesian(r, theta, phi):
    theta_rad = math.radians(theta)
    phi_rad = math.radians(phi)
    x = r * math.sin(phi_rad) * math.cos(theta_rad)
    y = r * math.sin(phi_rad) * math.sin(theta_rad)
    z = r * math.cos(phi_rad)
    return x, y, z

def cartesian_to_cylindrical(x, y, z):
    rho = math.sqrt(x ** 2 + y ** 2)
    phi = math.atan2(y, x)
    return rho, math.degrees(phi), z

def cylindrical_to_cartesian(rho, phi, z):
    phi_rad = math.radians(phi)
    x = rho * math.cos(phi_rad)
    y = rho * math.sin(phi_rad)
    return x, y, z

class ConverterApp(App):
    def build(self):
        self.start_background_music()

        layout = BoxLayout(orientation='vertical', padding=10)

        self.x_label = Label(text='X:')
        self.x_input = TextInput(hint_text='Enter X', multiline=False)

        self.y_label = Label(text='Y:')
        self.y_input = TextInput(hint_text='Enter Y', multiline=False)

        self.z_label = Label(text='Z:')
        self.z_input = TextInput(hint_text='Enter Z', multiline=False)

        self.convert_to_cylindrical_btn = Button(text='Cylindrical Conversion')
        self.convert_to_cylindrical_btn.bind(on_press=self.convert_to_cylindrical)

        self.convert_to_cartesian_btn = Button(text='Cylindrical to Cartesian Conversion')
        self.convert_to_cartesian_btn.bind(on_press=self.convert_to_cartesian_from_cylindrical)

        self.convert_to_spherical_btn = Button(text='Spherical Conversion')
        self.convert_to_spherical_btn.bind(on_press=self.convert_to_spherical)

        self.convert_to_cartesian_from_spherical_btn = Button(text=' Spherical to Cartesian Conversion')
        self.convert_to_cartesian_from_spherical_btn.bind(on_press=self.convert_to_cartesian_from_spherical)

        self.plot_spinner = Spinner(
            text='3D Plot Type',
            values=('Cartesian', 'Spherical', 'Cylindrical'),
            size_hint=(None, None),
            size=(200, 60)
        )

        self.plot_btn = Button(
            text='Plot',
            size_hint=(None, None),
            size=(200, 60)
        )
        self.plot_btn.bind(on_press=self.plot_graph)

        self.result_label = Label(
            text="Conversion Results:",
            font_size='20sp',
            size_hint=(1, None),  
            height=50,  
            halign="left",  
            valign="middle"  
        )

        self.results_output = Label(
            text="", 
            halign="left",
            size_hint_y=None,
            height=40    , 
            color=(1, 1, 1, 1)
        )

        layout.add_widget(self.x_label)
        layout.add_widget(self.x_input)
        layout.add_widget(self.y_label)
        layout.add_widget(self.y_input)
        layout.add_widget(self.z_label)
        layout.add_widget(self.z_input)
        layout.add_widget(self.convert_to_cylindrical_btn)
        layout.add_widget(self.convert_to_cartesian_btn)
        layout.add_widget(self.convert_to_spherical_btn)
        layout.add_widget(self.convert_to_cartesian_from_spherical_btn)
        layout.add_widget(self.plot_spinner)
        layout.add_widget(self.plot_btn)
        layout.add_widget(self.result_label)
        layout.add_widget(self.results_output)

        return layout

    def convert_to_cylindrical(self, instance):
        try:
            x = float(self.x_input.text)
            y = float(self.y_input.text)
            z = float(self.z_input.text)
            rho, phi, z_cyl = cartesian_to_cylindrical(x, y, z)
            # Round the results to 4 decimal places
            rho = round(rho, 4)
            phi = round(phi, 4)
            z_cyl = round(z_cyl, 4)
            self.result_label.text = f'Cylindrical Coordinates:\nρ: {rho}\nφ: {phi}\nz: {z_cyl}'
        except ValueError:
            self.show_error('Please enter valid numbers.')

    def convert_to_cartesian_from_cylindrical(self, instance):
        try:
            rho = float(self.x_input.text)
            phi = float(self.y_input.text)
            z = float(self.z_input.text)
            x, y, z_cart = cylindrical_to_cartesian(rho, phi, z)
            # Round the results to 4 decimal places
            x = round(x, 4)
            y = round(y, 4)
            z_cart = round(z_cart, 4)
            self.result_label.text = f'Cartesian Coordinates:\nX: {x}\nY: {y}\nZ: {z_cart}'
        except ValueError:
            self.show_error('Please enter valid numbers.')

    def convert_to_spherical(self, instance):
        try:
            x = float(self.x_input.text)
            y = float(self.y_input.text)
            z = float(self.z_input.text)
            r, theta, phi = cartesian_to_spherical(x, y, z)
            # Round the results to 4 decimal places
            r = round(r, 4)
            theta = round(theta, 4)
            phi = round(phi, 4)
            self.result_label.text = f'Spherical Coordinates:\nRadius: {r}\nθ: {theta}\nφ: {phi}'
        except ValueError:
            self.show_error('Please enter valid numbers.')

    def convert_to_cartesian_from_spherical(self, instance):
        try:
            r = float(self.x_input.text)
            theta = float(self.y_input.text)
            phi = float(self.z_input.text)
            x, y, z = spherical_to_cartesian(r, theta, phi)
            # Round the results to 4 decimal places
            x = round(x, 4)
            y = round(y, 4)
            z = round(z, 4)
            self.result_label.text = f'Cartesian Coordinates:\nX: {x}\nY: {y}\nZ: {z}'
        except ValueError:
            self.show_error('Please enter valid numbers.')

    def plot_graph(self, instance):
        try:
            plot_type = self.plot_spinner.text
            x = float(self.x_input.text)    
            y = float(self.y_input.text)
            z = float(self.z_input.text)

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            if plot_type == 'Cartesian':
                # Define the size of the cube
                size = 1.5

                # Define cube vertices
                vertices = [
                    [x - size/2, y - size/2, z - size/2],
                    [x + size/2, y - size/2, z - size/2],
                    [x + size/2, y + size/2, z - size/2],
                    [x - size/2, y + size/2, z - size/2],
                    [x - size/2, y - size/2, z + size/2],
                    [x + size/2, y - size/2, z + size/2],
                    [x + size/2, y + size/2, z + size/2],
                    [x - size/2, y + size/2, z + size/2],
                ]

                # Define faces using the vertices
                faces = [
                    [vertices[0], vertices[1], vertices[2], vertices[3]],  # Bottom
                    [vertices[4], vertices[5], vertices[6], vertices[7]],  # Top
                    [vertices[0], vertices[1], vertices[5], vertices[4]],  # Front
                    [vertices[2], vertices[3], vertices[7], vertices[6]],  # Back
                    [vertices[1], vertices[2], vertices[6], vertices[5]],  # Right
                    [vertices[0], vertices[3], vertices[7], vertices[4]],  # Left
                ]

                # Create a 3D polygon collection and add it to the plot
                cube = Poly3DCollection(faces, alpha=0.5, facecolor='red', edgecolor='grey')
                ax.add_collection3d(cube)

                ax.set_xlabel('X Label')
                ax.set_ylabel('Y Label')
                ax.set_zlabel('Z Label')

                # Adjust the aspect ratio to make it look like a cube
                ax.set_xlim([x - 1, x + 1])
                ax.set_ylim([y - 1, y + 1])
                ax.set_zlim([z - 1, z + 1])

            elif plot_type == 'Spherical':
                u = np.linspace(0, 2 * np.pi, 100)
                v = np.linspace(0, np.pi, 100)
                x_s = x + 10 * np.outer(np.cos(u), np.sin(v))
                y_s = y + 10 * np.outer(np.sin(u), np.sin(v))
                z_s = z + 10 * np.outer(np.ones(np.size(u)), np.cos(v))
                ax.plot_surface(x_s, y_s, z_s, color='b', alpha=0.5)
                ax.set_xlabel('X Label')
                ax.set_ylabel('Y Label')
                ax.set_zlabel('Z Label')

            elif plot_type == 'Cylindrical':
                z_c = np.linspace(0, 10, 100)
                theta = np.linspace(0, 2 * np.pi, 100)
                theta_grid, z_grid = np.meshgrid(theta, z_c)
                x_c = x + 5 * np.cos(theta_grid)
                y_c = y + 5 * np.sin(theta_grid)
                ax.plot_surface(x_c, y_c, z_grid, color='g', alpha=0.5)
                ax.set_xlabel('X Label')
                ax.set_ylabel('Y Label')
                ax.set_zlabel('Z Label')

            plt.show()
        except ValueError:
            self.show_error('Please enter valid numbers.')

    def show_error(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def start_background_music(self):
        threading.Thread(target=self.play_background_music, daemon=True).start()

    def play_background_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load("Traverse Town.mp3")  # Replace with your own music file
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

if __name__ == '__main__':
    ConverterApp().run()
