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

        self.init_labels_and_buttons(self.screen_height)

        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        self.start_x, self.start_y = None, None
        self.current_shape = None

        self.selected_shape = None  # To store the selected shape
        self.offset_x, self.offset_y = 0, 0  # To store the offset for moving the shape

    def start_draw(self, event):
        x, y = event.x, event.y
        # Check if there is a shape at the clicked position
        shapes = self.canvas.find_overlapping(x-1, y-1, x+1, y+1)
        if shapes:
            self.selected_shape = shapes[-1]  # Get the top-most shape
            self.offset_x = x - self.canvas.coords(self.selected_shape)[0]
            self.offset_y = y - self.canvas.coords(self.selected_shape)[1]
        else:
            # Create a new shape if no shape is clicked
            self.start_x, self.start_y = x, y
            if self.draw_type.get() == "line":
                self.current_shape = self.canvas.create_line(x, y, x, y)
            elif self.draw_type.get() == "rectangle":
                self.current_shape = self.canvas.create_rectangle(x, y, x, y)
            elif self.draw_type.get() == "circle":
                self.current_shape = self.canvas.create_oval(x, y, x, y)

    def draw(self, event):
        x, y = event.x, event.y
        if self.selected_shape:
            # Move the selected shape
            self.canvas.coords(self.selected_shape, x - self.offset_x, y - self.offset_y, x - self.offset_x + self.canvas.coords(self.selected_shape)[2] - self.canvas.coords(self.selected_shape)[0], y - self.offset_y + self.canvas.coords(self.selected_shape)[3] - self.canvas.coords(self.selected_shape)[1])
        elif self.current_shape:
            # Update the size of the current shape
            if self.draw_type.get() == "circle":
                radius = max(abs(x - self.start_x), abs(y - self.start_y))
                self.canvas.coords(self.current_shape, self.start_x - radius, self.start_y - radius, self.start_x + radius, self.start_y + radius)
            else:
                self.canvas.coords(self.current_shape, self.start_x, self.start_y, x, y)

    def end_draw(self, event):
        self.selected_shape = None

    def draw_with_parameters(self):
        x = int(self.param_x.get())
        y = int(self.param_y.get())
        if self.draw_type.get() == "line" or self.draw_type.get() == "rectangle":
            width = int(self.param_width.get())
            height = int(self.param_height.get())
        elif self.draw_type.get() == "circle":
            radius = int(self.param_radius.get())

        if self.draw_type.get() == "line":
            self.canvas.create_line(x, y, x + width, y + height)
        elif self.draw_type.get() == "rectangle":
            self.canvas.create_rectangle(x, y, x + width, y + height)
        elif self.draw_type.get() == "circle":
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius)

    def init_labels_and_buttons(self, screen_height):
        # Create radio buttons
        self.selected_value = tk.StringVar()
        self.draw_type = tk.StringVar()
        self.draw_type.set("line")
        self.radio_line = tk.Radiobutton(root, text="Linia", variable=self.draw_type, value="line", command=self.on_radio_button_select)
        self.radio_rect = tk.Radiobutton(root, text="Prostokąt", variable=self.draw_type, value="rectangle", command=self.on_radio_button_select)
        self.radio_circle = tk.Radiobutton(root, text="Koło", variable=self.draw_type, value="circle", command=self.on_radio_button_select)
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
        self.param_x.place(x=425, y=screen_height-190)
        self.param_y.place(x=425, y=screen_height-170)
        # Button to trigger drawing with parameters
        self.draw_button = tk.Button(root, text="Draw with Parameters", command=self.draw_with_parameters)
        self.draw_button.place(x=425, y=screen_height-110)
        # Create labels to discribe inputs
        self.label_x = tk.Label(root, text="X:")
        self.label_y = tk.Label(root, text="Y:")
        self.label_width = tk.Label(root, text="Width:")
        self.label_height = tk.Label(root, text="Height:")
        self.label_radius = tk.Label(root, text="Radius:")
        # Set labels x and y position
        self.label_x.place(x=409, y=screen_height - 190)
        self.label_y.place(x=409, y=screen_height - 170)
        self.update_label(screen_height)

        # Save and load buttons
        self.save_button = tk.Button(root, text="Save", command=self.save)
        self.save_button.place(x=1025, y=screen_height - 170)
        self.load_button = tk.Button(root, text="Load", command=self.load)
        self.load_button.place(x=1025, y=screen_height - 140)

    def on_radio_button_select(self):
        self.selected_value.set(self.draw_type.get())
        self.update_label(self.screen_height)

    def update_label(self, screen_height):
        if self.draw_type.get() == 'line':
            self.label.config(text="Wybrano rysowanie linii")
            self.update_line_and_rectangle_label_and_input(screen_height)
        elif self.draw_type.get() == 'rectangle':
            self.label.config(text="Wybrano rysowanie prostokąta")
            self.update_line_and_rectangle_label_and_input(screen_height)
        elif self.draw_type.get() == 'circle':
            self.label.config(text="Wybrano rysowanie koła")
            self.update_circle_label_and_input(screen_height)
        else:
            self.label.config(text="Nie wybrano figury do rysowania")

    def update_line_and_rectangle_label_and_input(self, screen_height):
        self.label_width.config(text="Width:")
        self.label_height.config(text="Height:")
        self.label_width.place(x=384, y=screen_height - 150)
        self.label_height.place(x=380, y=screen_height - 130)
        self.param_width.place(x=425, y=screen_height-150)
        self.param_height.place(x=425, y=screen_height-130)
        self.label_radius.place_forget()
        self.param_radius.place_forget()

    def update_circle_label_and_input(self, screen_height):
        self.label_radius.config(text="Radius:")
        self.param_radius.place(x=425, y=screen_height - 150)
        self.label_radius.place(x=381, y=screen_height - 150)
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
                        self.canvas.create_line(*coords)
                    elif obj_type == 'rectangle':
                        self.canvas.create_rectangle(*coords)
                    elif obj_type == 'oval':
                        self.canvas.create_oval(*coords)
                print(f"Loaded from {filename}")
            except FileNotFoundError:
                print("File not found.")
            except Exception as e:
                print(f"Error loading file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()