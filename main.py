import tkinter as tk
import pickle
from tkinter.filedialog import asksaveasfilename, askopenfilename

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint Piotr Szumowski")
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.canvas = tk.Canvas(self.root, width=self.screen_width, height=self.screen_height-200, bg="white")
        self.canvas.pack()

        self.initLabelsAndButtons(self.screen_height)

        self.canvas.bind("<ButtonPress-1>", self.startDraw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.endDraw)
        self.canvas.bind("<Button-3>", self.markShape)

        self.start_x, self.start_y = None, None
        self.current_shape = None

        self.selected_shape = None
        self.offset_x, self.offset_y = 0, 0

    def startDraw(self, event):
        x, y = event.x, event.y
        shapes = self.canvas.find_overlapping(x-1, y-1, x+1, y+1)
        if shapes and self.selected_shape and shapes[-1] == self.selected_shape:
            #print("Kliknieto zaznaczony obiekt. Zmienia rozmiar")
            self.current_shape = shapes[-1]
        elif shapes:
            #print("Kliknieto obiekt do przesuniecia. Przesuwa.")

            #self.unmarkShape(self.selected_shape)
            if self.selected_shape:
                self.colorBorder(self.selected_shape, "black")

            self.selected_shape = shapes[-1]
            self.offset_x = x - self.canvas.coords(self.selected_shape)[0]
            self.offset_y = y - self.canvas.coords(self.selected_shape)[1]
            self.colorBorder(self.selected_shape, "green")
        else:
            #print("Kliknieto pusta przestrzen. Tworzy nowy obiekt")
            self.start_x, self.start_y = x, y
            if self.draw_type.get() == "line":
                self.current_shape = self.canvas.create_line(x, y, x, y, width=3)
            elif self.draw_type.get() == "rectangle":
                self.current_shape = self.canvas.create_rectangle(x, y, x, y, width=3)
            elif self.draw_type.get() == "circle":
                self.current_shape = self.canvas.create_oval(x, y, x, y, width=3)
            self.colorBorder(self.current_shape, "red")

    def draw(self, event):
        x, y = event.x, event.y
        shapes = self.canvas.find_overlapping(x - 1, y - 1, x + 1, y + 1)
        if self.selected_shape and self.current_shape:
            #print("Zmien rozmiar obecnie zaznaczonej figury")
            if self.canvas.type(self.current_shape) == "line":
                # Calculate the new endpoint coordinates
                x1, y1, x2, y2 = self.canvas.coords(self.current_shape)
                new_x2, new_y2 = x, y
                # Move the endpoint
                self.canvas.coords(self.current_shape, x1, y1, new_x2, new_y2)
            elif self.canvas.type(self.current_shape) == "rectangle":
                x1, y1, x2, y2 = self.canvas.coords(self.current_shape)
                new_width, new_height = x - x1, y - y1
                if x < x1:
                    x1 = x
                if y < y1:
                    y1 = y
                x2, y2 = x1 + new_width, y1 + new_height
                self.canvas.coords(self.current_shape, x1, y1, x2, y2)
            elif self.canvas.type(self.current_shape) == "oval":
                x1, y1, x2, y2 = self.canvas.coords(self.current_shape)
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                new_width = abs(x - center_x) * 2
                new_height = abs(y - center_y) * 2
                if new_width < new_height:
                    new_height = new_width
                else:
                    new_width = new_height
                self.canvas.coords(self.current_shape, center_x - new_width / 2, center_y - new_height / 2, center_x + new_width / 2, center_y + new_height / 2)
            self.fillInputs(self.current_shape)
        elif self.selected_shape:
            #print("Przesun figure")
            self.canvas.coords(self.selected_shape, x - self.offset_x, y - self.offset_y, x - self.offset_x + self.canvas.coords(self.selected_shape)[2] - self.canvas.coords(self.selected_shape)[0], y - self.offset_y + self.canvas.coords(self.selected_shape)[3] - self.canvas.coords(self.selected_shape)[1])
            self.fillInputs(self.selected_shape)
        elif self.current_shape:
            #print("Rysuj nowa figure")
            if self.draw_type.get() == "circle":
                radius = max(abs(x - self.start_x), abs(y - self.start_y))
                self.canvas.coords(self.current_shape, self.start_x - radius, self.start_y - radius, self.start_x + radius, self.start_y + radius)
            else:
                self.canvas.coords(self.current_shape, self.start_x, self.start_y, x, y)
            self.fillInputs(self.current_shape)

    def endDraw(self, event):
        #print("Puszczono")
        self.unmarkShape(None)
        self.colorBorder(self.selected_shape, "black")
        self.selected_shape = None
        self.colorBorder(self.current_shape, "black")
        self.current_shape = None

    def drawWithParameters(self):
        x = int(self.param_x.get())
        y = int(self.param_y.get())
        if self.draw_type.get() == "line" or self.draw_type.get() == "rectangle":
            width = int(self.param_width.get())
            height = int(self.param_height.get())
        elif self.draw_type.get() == "circle":
            radius = int(self.param_radius.get())
        if self.draw_type.get() == "line":
            self.canvas.create_line(x, y, x + width, y + height, width=3)
        elif self.draw_type.get() == "rectangle":
            self.canvas.create_rectangle(x, y, x + width, y + height, width=3)
        elif self.draw_type.get() == "circle":
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, width=3)

    def changeWithParameters(self):
        print(self.selected_shape)
        self.canvas.delete(self.selected_shape)
        self.drawWithParameters()
        self.unmarkShape(None)

    def colorBorder(self, shape, color):
        if shape:
            if self.canvas.type(shape) == "line":
                self.canvas.itemconfig(shape, fill=color)
            elif self.canvas.type(shape) == "rectangle" or self.canvas.type(shape) == "oval":
                self.canvas.itemconfig(shape, outline=color)
            else:
                print("Selected shape is of an unknown type.")


    def markShape(self, event):
        self.unmarkShape(self.selected_shape)
        x, y = event.x, event.y
        shapes = self.canvas.find_overlapping(x - 1, y - 1, x + 1, y + 1)
        if shapes:
            if self.selected_shape == shapes[-1]:
                self.selected_shape = self.unmarkShape(self.selected_shape)
            else:
                self.selected_shape = self.unmarkShape(self.selected_shape)
                self.selected_shape = shapes[-1]
                self.colorBorder(self.selected_shape, "blue")
                self.fillInputs(self.selected_shape)
                self.draw_button.place_forget()
                self.change_button.place(x=205, y=self.screen_height - 110)

    def fillInputs(self, shape):
        self.clearInputs()
        if shape:
            shape_type = self.canvas.type(shape)
            shape_coords = self.canvas.coords(shape)
            print(f"Selected Shape Type: {shape_type}")
            print(f"Selected Shape Coordinates: {shape_coords}")
            shape_type = 'circle' if shape_type == 'oval' else shape_type
            self.draw_type.set(shape_type)
            self.updateLabel(shape_type)
            if shape_type == "line" or shape_type == "rectangle":
                width = int(shape_coords[2] - shape_coords[0])
                height = int(shape_coords[3] - shape_coords[1])
                self.param_x.insert(0, str(int(shape_coords[0])))
                self.param_y.insert(0, str(int(shape_coords[1])))
                self.param_width.insert(0, str(width))
                self.param_height.insert(0, str(height))
            elif shape_type == "circle":
                x1, y1, x2, y2 = shape_coords
                radius = int(max(abs(x2 - x1), abs(y2 - y1)) / 2)
                self.param_x.insert(0, str(int((shape_coords[2]+shape_coords[0])/2)))
                self.param_y.insert(0, str(int((shape_coords[3]+shape_coords[1])/2)))
                self.param_radius.insert(0, str(radius))

    def unmarkShape(self, shape):
        if shape:
            self.colorBorder(shape, "black")
        self.clearInputs()
        self.change_button.place_forget()
        self.draw_button.place(x=205, y=self.screen_height - 110)
        return None

    def clearInputs(self):
        self.param_x.delete(0, tk.END)
        self.param_y.delete(0, tk.END)
        self.param_width.delete(0, tk.END)
        self.param_height.delete(0, tk.END)
        self.param_radius.delete(0, tk.END)

    def initLabelsAndButtons(self, screen_height):
        # Create radio buttons
        self.selected_value = tk.StringVar()
        self.draw_type = tk.StringVar()
        self.draw_type.set("line")
        self.radio_line = tk.Radiobutton(root, text="Line", variable=self.draw_type, value="line", command=self.onRadioButtonSelect)
        self.radio_rect = tk.Radiobutton(root, text="Rectangle", variable=self.draw_type, value="rectangle", command=self.onRadioButtonSelect)
        self.radio_circle = tk.Radiobutton(root, text="Circle", variable=self.draw_type, value="circle", command=self.onRadioButtonSelect)
        self.radio_line.place(x=25, y=screen_height - 170)
        self.radio_rect.place(x=25, y=screen_height - 150)
        self.radio_circle.place(x=25, y=screen_height - 130)
        # Create label to display chosen radio button
        self.label = tk.Label(root, text="")
        self.label.place(x=25, y=screen_height - 190)
        # Create input fields for parameters
        self.param_x = tk.Entry(root)
        self.param_y = tk.Entry(root)
        self.param_width = tk.Entry(root)
        self.param_height = tk.Entry(root)
        self.param_radius = tk.Entry(root)
        # Set inputs x and y position
        self.param_x.place(x=205, y=screen_height-190)
        self.param_y.place(x=205, y=screen_height-170)
        # Button to trigger drawing with parameters
        self.draw_button = tk.Button(root, text="Draw with Parameters", command=self.drawWithParameters)
        self.draw_button.place(x=205, y=screen_height-110)
        # Button to trigger change with parameters
        self.change_button = tk.Button(root, text="Change with Parameters", command=self.changeWithParameters)
        # Create labels to discribe inputs
        self.label_x = tk.Label(root, text="X:")
        self.label_y = tk.Label(root, text="Y:")
        self.label_width = tk.Label(root, text="Width:")
        self.label_height = tk.Label(root, text="Height:")
        self.label_radius = tk.Label(root, text="Radius:")
        # Set labels x and y position
        self.label_x.place(x=189, y=screen_height - 190)
        self.label_y.place(x=189, y=screen_height - 170)
        self.updateLabel(self.draw_type.get())
        # Save and load buttons
        self.save_button = tk.Button(root, text="Save", command=self.save)
        self.save_button.place(x=400, y=screen_height - 170)
        self.load_button = tk.Button(root, text="Load", command=self.load)
        self.load_button.place(x=400, y=screen_height - 140)

    def onRadioButtonSelect(self):
        self.selected_value.set(self.draw_type.get())
        self.updateLabel(self.draw_type.get())

    def updateLabel(self, value):
        screen_height = self.screen_height
        if value == 'line':
            self.label.config(text="Line drawing selected")
            self.updateLineAndRectangleLabelAndInput(screen_height)
        elif value == 'rectangle':
            self.label.config(text="Rectangle drawing selected")
            self.updateLineAndRectangleLabelAndInput(screen_height)
        elif value == 'circle':
            self.label.config(text="Circle drawing selected")
            self.updateCircleLabelAndInput(screen_height)
        else:
            self.label.config(text="Nie wybrano figury do rysowania")

    def updateLineAndRectangleLabelAndInput(self, screen_height):
        self.label_width.config(text="Width:")
        self.label_height.config(text="Height:")
        self.label_width.place(x=164, y=screen_height - 150)
        self.label_height.place(x=160, y=screen_height - 130)
        self.param_width.place(x=205, y=screen_height-150)
        self.param_height.place(x=205, y=screen_height-130)
        self.label_radius.place_forget()
        self.param_radius.place_forget()

    def updateCircleLabelAndInput(self, screen_height):
        self.label_radius.config(text="Radius:")
        self.param_radius.place(x=205, y=screen_height - 150)
        self.label_radius.place(x=161, y=screen_height - 150)
        self.label_height.place_forget()
        self.param_height.place_forget()
        self.label_width.place_forget()
        self.param_width.place_forget()

    def save(self):
        filename = asksaveasfilename(initialfile='Untitled.pkl', defaultextension=".pkl", filetypes=[("Pickle Files", "*.pkl")])
        if filename is not None:
            objects_on_canvas = self.canvas.find_all()
            positions = {}
            for obj_id in objects_on_canvas:
                obj_type = self.canvas.type(obj_id)
                coords = self.canvas.coords(obj_id)
                positions[obj_id] = {'type': obj_type, 'coords': coords}
            with open(filename, 'wb') as file:
                pickle.dump(positions, file)
            print(f"Saved to {filename}")

    def load(self):
        filename = askopenfilename()
        if filename is not None:
            try:
                with open(filename, 'rb') as file:
                    positions = pickle.load(file)
                self.canvas.delete('all')
                for obj_id, obj_data in positions.items():
                    obj_type = obj_data['type']
                    coords = obj_data['coords']
                    if obj_type == 'line':
                        self.canvas.create_line(*coords, width=3)
                    elif obj_type == 'rectangle':
                        self.canvas.create_rectangle(*coords, width=3)
                    elif obj_type == 'oval':
                        self.canvas.create_oval(*coords, width=3)
                print(f"Loaded from {filename}")
            except FileNotFoundError:
                print("File not found.")
            except Exception as e:
                print(f"Error loading file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()