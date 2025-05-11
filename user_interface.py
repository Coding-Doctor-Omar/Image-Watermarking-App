import tkinter.ttk as ttk
from tkinter import Tk, PhotoImage, Canvas, Label, Entry, Button, Scale, colorchooser, filedialog, StringVar, messagebox
from PIL import Image, ImageTk
from image_processor import ImageProcessor

fonts = {
    "Arial": "data/fonts/arial.ttf",
    "Arial Bold": "data/fonts/arialbd.ttf",
    "Arial Bold Italic": "data/fonts/arialbi.ttf",
    "Arial Italic": "data/fonts/ariali.ttf",
    "Arial Narrow": "data/fonts/ARIALN.TTF",
    "Arial Narrow Bold": "data/fonts/ARIALNB.TTF",
    "Arial Narrow Bold Italic": "data/fonts/ARIALNBI.TTF",
    "Arial Narrow Italic": "data/fonts/ARIALNI.TTF",
    "Arial Black": "data/fonts/arialblk.ttf",
    "Brush Script MT Italic": "data/fonts/BRUSHSCI.TTF",
    "Georgia": "data/fonts/georgia.ttf",
    "Georgia Bold": "data/fonts/georgiab.ttf",
    "Georgia Italic": "data/fonts/georgiai.ttf",
    "Georgia Bold Italic": "data/fonts/georgiaz.ttf",
    "Tahoma": "data/fonts/tahoma.ttf",
    "Tahoma Bold": "data/fonts/tahomabd.ttf",
    "Times New Roman": "data/fonts/times.ttf",
    "Times New Roman Bold": "data/fonts/timesbd.ttf",
    "Times New Roman Bold Italic": "data/fonts/timesbi.ttf",
    "Times New Roman Italic": "data/fonts/timesi.ttf",
    "Verdana": "data/fonts/verdana.ttf",
    "Verdana Bold": "data/fonts/verdanab.ttf",
    "Verdana Italic": "data/fonts/verdanai.ttf",
    "Verdana Bold Italic": "data/fonts/verdanaz.ttf",
}

class UI:
    def __init__(self):
        self.image_preview = None
        self.image = None
        self.processed_image = None
        self.text = None
        self.font = "Brush Script MT Italic"
        self.color = "#FF0000"
        self.size = 10
        self.opacity = 120
        self.rotation = 0
        self.position = "Center"

        self.window = Tk()
        self.window.title("Mark-It (Image Watermarking App)")

        icon = PhotoImage(file="data/images/water-droplet-icon.png")
        self.window.iconphoto(False, icon)

        self.image_preview_label = Label(self.window, text="Image Preview", font=("Arial", 16, "bold"))
        self.image_preview_label.grid(row=0, column=0, padx=10)

        self.preview_section = Canvas(self.window, width=500, height=500, bg="gray", relief="sunken", bd=2)
        self.preview_section.create_text(250, 250, text="UPLOAD IMAGE HERE", fill="white", anchor="center",
                                    font=("Arial", 12, "normal"))
        self.preview_section.grid(row=1, column=0, rowspan=10, padx=10, pady=5)

        self.upload_button = Button(self.window, text="Upload Image", font=("Arial", 13, "normal"), bg="lightgray", padx=10,
                               relief="groove", command=self.upload_image)
        self.upload_button.grid(row=11, column=0, pady=5)

        self.controls_title = Label(self.window, text="Watermark Customization", font=("Arial", 16, "bold"))
        self.controls_title.grid(row=1, column=1, padx=10, sticky="w")

        self.text_label = Label(self.window, text="Text:", font=("Arial", 11, "normal"))
        self.text_label.grid(row=2, column=1, padx=10, sticky="w")

        self.text_var = StringVar()
        self.text_var.trace_add("write", self.text_update)
        self.text_input = Entry(self.window, width=32, font=("Times New Roman", 11, "normal"), textvariable=self.text_var)
        self.text_input.grid(row=2, column=1, padx=10, sticky="e")

        self.font_label = Label(self.window, text="Font:", font=("Arial", 11, "normal"))
        self.font_label.grid(row=3, column=1, padx=10, sticky="w")

        self.font_choices = ttk.Combobox(self.window, width=34)
        self.font_choices["values"] = (
            "Arial",
            "Arial Bold",
            "Arial Bold Italic",
            "Arial Italic",
            "Arial Narrow",
            "Arial Narrow Bold",
            "Arial Narrow Bold Italic",
            "Arial Narrow Italic",
            "Arial Black",
            "Brush Script MT Italic",
            "Georgia",
            "Georgia Bold",
            "Georgia Italic",
            "Georgia Bold Italic",
            "Tahoma",
            "Tahoma Bold",
            "Times New Roman",
            "Times New Roman Bold",
            "Times New Roman Bold Italic",
            "Times New Roman Italic",
            "Verdana",
            "Verdana Bold",
            "Verdana Italic",
            "Verdana Bold Italic",
        )
        self.font_choices.current(9)
        self.font_choices.grid(row=3, column=1, padx=10, sticky="e")
        self.font_choices.bind("<<ComboboxSelected>>", self.font_update)

        self.color_label = Label(self.window, text="Color:", font=("Arial", 11, "normal"))
        self.color_label.grid(row=4, column=1, padx=10, sticky="w")

        self.color_button = Button(self.window, text=" ", bg="#FF0000", padx=105, relief="groove", command=self.pick_color)
        self.color_button.grid(row=4, column=1, padx=10, sticky="e")

        self.size_label = Label(self.window, text="Size:", font=("Arial", 11, "normal"))
        self.size_label.grid(row=5, column=1, padx=10, sticky="w")

        self.size_slider = Scale(self.window, from_=1, to=20, orient="horizontal", length=218, width=20)
        self.size_slider.set(10)
        self.size_slider.config(command=self.size_update)
        self.size_slider.grid(row=5, column=1, padx=10, sticky="e")

        self.opacity_label = Label(self.window, text="Opacity:", font=("Arial", 11, "normal"))
        self.opacity_label.grid(row=6, column=1, padx=10, sticky="w")

        self.opacity_slider = Scale(self.window, from_=0, to=255, orient="horizontal", length=200, width=20)
        self.opacity_slider.set(120)
        self.opacity_slider.config(command=self.opacity_update)
        self.opacity_slider.grid(row=6, column=1, padx=10, sticky="e")

        self.rotation_label = Label(self.window, text="Rotation:", font=("Arial", 11, "normal"))
        self.rotation_label.grid(row=7, column=1, padx=10, sticky="w")

        self.rotation_slider = Scale(self.window, from_=-180, to=180, orient="horizontal", length=200, width=20, command=self.rotation_update)
        self.rotation_slider.grid(row=7, column=1, padx=10, sticky="e")

        self.position_label = Label(self.window, text="Position:", font=("Arial", 11, "normal"))
        self.position_label.grid(row=8, column=1, padx=10, sticky="w")

        self.position_choices = ttk.Combobox(self.window, width=30)
        self.position_choices["values"] = (
            "Center",
            "Top Left",
            "Top",
            "Top Right",
            "Left",
            "Right",
            "Bottom Left",
            "Bottom",
            "Bottom Right",
        )
        self.position_choices.current(0)
        self.position_choices.grid(row=8, column=1, padx=10, sticky="e")
        self.position_choices.bind("<<ComboboxSelected>>", self.position_update)

        self.save_image = Button(self.window, text="Save Image", font=("Arial", 13, "normal"), bg="lightgray", padx=81,
                            relief="groove", command=self.save_image)
        self.save_image.grid(row=9, column=1)

        self.window.update_idletasks()
        self.window.maxsize(self.window.winfo_width(), self.window.winfo_height())


        self.window.mainloop()



    def pick_color(self):
        color = colorchooser.askcolor(title="Choose a color")[1]

        if color:
            self.color_button.config(bg=color)
            self.color = color
            self.color_update(self.color)

    def upload_image(self):
        image_path = filedialog.askopenfilename(title="Upload Your Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.png *.bmp *.gif *.tif *.tiff *.webp *.ppm *.pgm")])

        self.image = Image.open(image_path)

        image_width, image_height = self.image.size

        if image_width >= image_height:
            target_width = self.preview_section.winfo_width()
            target_height = (target_width * image_height) / image_width
        else:
            target_height = self.preview_section.winfo_height()
            target_width = (target_height * image_width) / image_height

        resized_image = self.image.resize((int(target_width), int(target_height)), Image.Resampling.LANCZOS)

        image_tk = ImageTk.PhotoImage(resized_image)
        self.image_preview = image_tk

        self.preview_section.delete("all")
        self.preview_section.create_image(250, 250, image=self.image_preview, anchor="center")

        self.text_input.focus()


    def create_watermark(self):
        if self.image:
            processor = ImageProcessor(image=self.image)

            processor.add_watermark(
                image=self.image,
                text=self.text,
                font_type=fonts[self.font],
                color=self.color,
                font_size=int(self.size),
                opacity=int(self.opacity),
                rotation=float(self.rotation),
                position=self.position,
            )

            self.processed_image = processor.processed_img

            image_width, image_height = self.processed_image.size

            if image_width >= image_height:
                target_width = self.preview_section.winfo_width()
                target_height = (target_width * image_height) / image_width
            else:
                target_height = self.preview_section.winfo_height()
                target_width = (target_height * image_width) / image_height

            resized_image = self.processed_image.resize((int(target_width), int(target_height)), Image.Resampling.LANCZOS)

            image_tk = ImageTk.PhotoImage(resized_image)
            self.image_preview = image_tk

            self.preview_section.delete("all")
            self.preview_section.create_image(250, 250, image=self.image_preview, anchor="center")

    def save_image(self):
        if self.image:
            save_path = filedialog.asksaveasfilename(title="Save Image As", defaultextension=".jpg", filetypes=[("Image File", "*.jpg")])

            if self.processed_image:
                processor = ImageProcessor(image=self.processed_image)
            else:
                processor = ImageProcessor(image=self.image)

            processor.save_final_image(path=save_path)
            messagebox.showinfo(title="Save Complete", message="Image Saved Successfully!")
        else:
            messagebox.showinfo(title="Error", message="No Image To Save.")


    def rotation_update(self, rotation):
        self.rotation = rotation
        self.create_watermark()

    def color_update(self, color):
        self.color = color
        self.create_watermark()

    def size_update(self, size):
        self.size = size
        self.create_watermark()

    def opacity_update(self, opacity):
        self.opacity = opacity
        self.create_watermark()

    def text_update(self, *args):
        self.text = self.text_var.get()
        self.create_watermark()

    def font_update(self, event):
        self.font = self.font_choices.get()
        self.create_watermark()

    def position_update(self, event):
        self.position = self.position_choices.get()
        self.create_watermark()


