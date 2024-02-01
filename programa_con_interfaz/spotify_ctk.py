from tkinter import *
import customtkinter as ctk
from PIL import Image
from io import BytesIO
import requests

class general_checkBox:
    def __init__(self, x, y, text, frameToDisable, lista_seleccion, root):
        self.x = x
        self.y = y
        self.text = text
        self.frameToDisable = frameToDisable
        self.lista_seleccion = lista_seleccion
        self.root = root

    def create_checkBox(self):
        
        def set_frame_state():
            print(check_var.get())
            if check_var.get() == "off":
                self.lista_seleccion.clear()
                for checkBox in self.frameToDisable.checkBoxes:
                    if checkBox.is_checked():
                        checkBox.frame_checkBox.deselect()
                    checkBox.frame_checkBox.configure(state="disabled")
            else:
                for checkBox in self.frameToDisable.checkBoxes:
                    checkBox.frame_checkBox.configure(state="normal")

        check_var = ctk.StringVar(value = "off") # variable que se va a usar para el checkbutton
        my_check = ctk.CTkCheckBox(self.root, text=self.text,
                                        variable = check_var, onvalue="on", offvalue="off",
                                        command = set_frame_state)
        my_check.pack(pady=2, padx=3)
        my_check.place(x=self.x, y=self.y)

class frame_checkBox:
    def __init__(self, text, state, pady, frame, lista_seleccion):
        self.text = text
        self.state = state
        self.pady = pady
        self.frame = frame # frame donde se va a meter el checkbutton
        self.lista_seleccion = lista_seleccion
        
    def create_frame_checkBox(self):
        def añadir_item():
            if self.frame_checkBox.get() == "on":
                self.lista_seleccion.append(self.text)
            elif self.text in self.lista_seleccion:
                self.lista_seleccion.remove(self.text)
            print(self.lista_seleccion)

        
        check_var = ctk.StringVar(value = "off") # variable que se va a usar para el checkbutton
        self.frame_checkBox = ctk.CTkCheckBox(self.frame, 
                                         text=self.text,
                                         variable = check_var, onvalue="on", offvalue="off",
                                         command = añadir_item)
        self.frame_checkBox.pack(pady=self.pady, padx=3, anchor="w") # anchor para que se alinee a la izquierda
    
    def is_checked(self):
        return self.frame_checkBox.get() == "on"

class scrollable_frame:
    def __init__(self, list, x, y, state, title, lista_seleccion, root):
        self.list = list # lista de strings
        self.x = x
        self.y = y
        self.state = state
        self.title = title
        self.checkBoxes = []
        self.lista_seleccion = lista_seleccion
        self.root = root

    def create_scrollable_frame(self):
        # create a scrollable frame
        self.scrollFrame = ctk.CTkScrollableFrame(self.root, label_text=self.title)
        self.scrollFrame.pack(pady = 2, padx = 3)
        self.scrollFrame.place(x=self.x, y=self.y)
        self.scrollFrame.configure(height=300, width=300)
        # loop for buttons
        for i in self.list:
            checkBox = frame_checkBox(i, self.state, 2, self.scrollFrame,self.lista_seleccion)
            checkBox.create_frame_checkBox()
            checkBox.frame_checkBox.configure(state="disabled")
            self.checkBoxes.append(checkBox)
    def create_submit_button(self, referencia_lista_artists):
        def submit(referencia_lista_artists):
            print(self.lista_seleccion)
            referencia_lista_artists[0] = self.lista_seleccion
        self.submit_button = ctk.CTkButton(self.root, text="Elegir selección", command = lambda: submit(referencia_lista_artists), width=300, height=30)
        self.submit_button.place(x=self.x, y=self.y+358)

class segmented_button:
    def __init__(self, x, y, playlist_public, options, root):
        self.x = x
        self.y = y
        self.options = options
        self.playlist_public = playlist_public
        self.root = root
    
    def create_segmented_button(self):
        
        def clicker(value):
            if self.segmentedButton.get() == "Playlist PRIVADA":
                self.playlist_public = False
                print(f'La playlist es publica: {self.playlist_public}')
            else:
                self.playlist_public = True
                print(f'La playlist es publica: {self.playlist_public}')

        self.segmentedButton = ctk.CTkSegmentedButton(self.root, values = self.options, command=clicker,
                                                      width=300, height = 30,
                                                      font = ("Helvetica", 12))
        self.segmentedButton.place(x=self.x, y=self.y)
        self.segmentedButton.set("Playlist PUBLICA")
    
    def add_label(self, text = "Privacidad de la playlist:"):
        x = self.x
        y = self.y - 30
        self.label = ctk.CTkLabel(self.root, text=text, font = ("Helvetica", 16))
        self.label.place(x=x, y=y)

class entry:
    def __init__(self, x, y, text, string_list, root):
        self.x = x
        self.y = y
        self.text = text
        self.string_list = string_list
        self.root = root
    
    def create_entry(self):
        self.entry = ctk.CTkEntry(self.root, placeholder_text= self.text,
                                  width = 300, height=50)
        self.entry.place(x=self.x, y=self.y)
        
    def add_button(self, text = "Enviar"):
        def submit():
            self.string_list.append(self.entry.get())
            print(f"{self.text}: {self.string_list[0]}")
            if len(self.string_list) == 0:
                self.string_list.append("no_name")
        
        x = self.x + 300 + 5
        y = self.y
        self.button = ctk.CTkButton(self.root, text=text, command = submit)
        self.button.place(x=x+ 5, y=y)

    def add_label(self):
        text = self.text
        x = self.x
        y = self.y - 30
        self.label = ctk.CTkLabel(self.root, text=text, font = ("Helvetica", 16))
        self.label.place(x=x, y=y)

class image_label:
    def __init__(self, x, y, image_path, size, root):
        self.x = x
        self.y = y
        self.image_path = image_path
        self.size = size # (width, height)
        self.root = root
    
    def create_image_label(self):
        self.image = ctk.CTkImage(light_image=Image.open(self.image_path), dark_image=Image.open(self.image_path),
                                  size = self.size)
        self.image_label = ctk.CTkLabel(self.root, image=self.image, text="")
        self.image_label.place(x=self.x, y=self.y)

class Slider:
    def __init__(self, x, y, min_año_playlist, max_año_playlist, año_inicio, año_fin, title1, title2, list_years, root):
        self.x = x
        self.y = y
        self.min_año_playlist = min_año_playlist
        self.max_año_playlist = max_año_playlist
        self.value = min_año_playlist
        self.title = title1
        self.title2 = title2
        self.año_fin = año_fin
        self.año_inicio = año_inicio
        self.root = root
        self.list_years = list_years

    def create_disabling_checkBox(self):
        def toggle_state():
            if self.check_var.get() == "off":
                self.slider.configure(state="disabled")
                self.label1.configure(text="")
                self.slider.set(self.min_año_playlist)
                self.submit_button.configure(state="disabled")
                self.list_years.clear()

                try:
                    self.submit_button2.destroy()
                    self.label2.configure(text="")
                    self.slider2.configure(state="disabled")
                    self.slider2.destroy()
                except:
                    pass
            else:
                self.slider.configure(state="normal")
                self.submit_button.configure(state="normal")
                self.label1.configure(text=f"{self.title}: {self.min_año_playlist}")
                try:
                    self.slider2.configure(state="normal")
                except:
                    pass


        self.check_var = ctk.StringVar(value = "off") # variable que se va a usar para el checkbutton
        self.checkbox = ctk.CTkCheckBox(self.root, text="Quiero un periodo de años:",
                                        variable = self.check_var, onvalue="on", offvalue="off",
                                        command = toggle_state)
        self.checkbox.place(x=self.x, y=self.y-50)
        


    def create_slider(self):
        
        def slider_function(value):
            self.año_inicio = int(value)
            self.label1.configure(text=f"{self.title}: {self.año_inicio}")

        self.slider = ctk.CTkSlider(self.root,
                                    from_=self.min_año_playlist,
                                    to=self.max_año_playlist,
                                    command=slider_function,
                                    width=300)
        self.slider.configure(state="disabled")
        self.slider.place(x=self.x, y=self.y)
        self.slider.set(self.min_año_playlist)

        self.label1 = ctk.CTkLabel(self.root, text=f"{self.title}: {self.min_año_playlist}")
        self.label1.place(x=self.x, y=self.y-30)

    def add_button(self, text = "Enviar"):
        
        def submit():

            def slider_function2(value):
                self.año_fin = int(value)
                self.label2.configure(text=f"{self.title2}: {self.año_fin}")
                
            def submit2():
                print(f"El año de fin es: {self.año_fin}")
                self.slider2.configure(state="disabled")
                self.submit_button2.configure(state="disabled")
                self.list_years.append(self.año_inicio)
                self.list_years.append(self.año_fin)

            print(f"El año de inicio es: {self.año_inicio}")
            self.slider.configure(state="disabled")
            self.submit_button.configure(state="disabled")

            self.slider2 = ctk.CTkSlider(self.root,
                                        from_=self.año_inicio,
                                        to=self.max_año_playlist,
                                        command=slider_function2,
                                        width=300)
            self.slider2.place(x=self.x, y=self.y+60)
            self.slider2.set(self.año_inicio)

            self.submit_button2 = ctk.CTkButton(self.root, text="Enviar", command = submit2)
            self.submit_button2.place(x=self.x + 300, y=self.y+60)

            self.label2 = ctk.CTkLabel(self.root, text=f"{self.title2}: {self.año_inicio}")
            self.label2.place(x=self.x, y=self.y+30)

        self.submit_button = ctk.CTkButton(self.root, text=text, command = submit)
        self.submit_button.place(x=self.x + 300, y=self.y)

class scrollable_frame_playlist:
    def __init__(self, list, x, y, title, image_url, root):
        self.list = list # lista de strings
        self.x = x
        self.y = y
        self.title = title
        self.image_url = image_url
        self.root = root

    def create_scrollable_frame(self):
        # create a scrollable frame
        self.scrollFrame = ctk.CTkScrollableFrame(self.root, label_text=self.title)
        self.scrollFrame.pack(pady = 2, padx = 3)
        self.scrollFrame.place(x=self.x, y=self.y)
        self.scrollFrame.configure(height=300, width=300)
        #loop for labels
        for i in self.list:
            track_label = ctk.CTkLabel(self.scrollFrame, text=i)
            track_label.pack(pady=2, padx=3, anchor="w", fill="x")
            track_label.configure(state="disabled")

    def add_cover(self):
        response = requests.get(self.image_url)
        image = Image.open(BytesIO(response.content))

        self.image = ctk.CTkImage(light_image=image, dark_image=image, size = (300,300))
        self.image_label = ctk.CTkLabel(self.root, image=self.image, text="")
        self.image_label.place(x=self.x, y=self.y-300)

class toplevel_window:
    def __init__(self, root, url):
        self.root = root
        self.url = url
    
    def create_toplevel_window(self):
        self.toplevel = ctk.CTkToplevel(self.root)
        self.toplevel.title = "Playlist creada con éxito!"
        self.toplevel.geometry("600x200")
        self.toplevel.iconbitmap("assets\icono.ico")
        self.toplevel.resizable(False, False) # Width, Height

        def close():
            self.toplevel.destroy()
            self.root.destroy()
            self.toplevel.update()
        close_button = ctk.CTkButton(self.toplevel, text="Cerrar", command = close)
        close_button.pack(pady=2, padx=3, anchor="w", fill="x")

        
        text = f"Playlist creada con éxito! \n Accede a ella en tu cuenta de Spotify o a través de este link: \n {self.url}"
        self.label = ctk.CTkLabel(self.toplevel, fg_color = "transparent",text = text, font = ("Helvetica", 16))
        self.label.pack(pady=2, padx=3, anchor="w", fill="x")

class Input_dialog:
    def __init__(self, url):
        self.url = url

    def create_input_dialog(self):
        dialog = ctk.CTkInputDialog(title="Spotify Playlist Creator", text = "Introduce la url de la playlist")
        dialog.iconbitmap("assets\logo_solo.png")
        url = dialog.get_input()
        return url