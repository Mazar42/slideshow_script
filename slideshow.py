import os
import random
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Create a function to define the slideshow settings (amount of pictures and display time per picture)
def slide_show_settings():
    while True:
        user_duration_input = input("How long should each slide be displayed for? (in seconds) ")
        try:
            slide_duration = int(user_duration_input)
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        user_amount_input = input("How many pictures would you like to see? ")
        try:
            pictures_amount = int(user_amount_input)
            break
        except ValueError:
            print("Please enter a valid number.")
    
    return slide_duration, pictures_amount

# Create a function to define the folder where pictures are stored (user chooses directory)
def define_directory(root): 
    root.withdraw()  # Hide the root window
    selected_folder = filedialog.askdirectory(title="Select a Folder for your slideshow")

    if selected_folder and os.path.isdir(selected_folder):
        print("Selected folder:", selected_folder)
        return selected_folder
    else:
        print("Invalid or no folder selected.")
        return None

# Create a function to check that the directory contains pictures and store them in a variable for later use
def get_images_from_folder(folder):
    image_extension = ('.jpg', '.jpeg', '.png', '.gif')
    pictures_list = []

    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)

        if os.path.isfile(file_path) and file_name.lower().endswith(image_extension):
            pictures_list.append(file_path)

    if len(pictures_list) == 0:
        print("No image found in the selected folder.")
        return None

    print(f"Found {len(pictures_list)} image(s).")
    return pictures_list

# Create a function to shuffle the images
def shuffle_images(images):
    random.shuffle(images)

# Class to handle the slideshow
class SlideshowApp:
    def __init__(self, root, pictures_list, slide_duration):
        self.root = root
        self.root.title("Slideshow")

        self.pictures_list = pictures_list
        self.slide_duration = slide_duration * 1000  # Convert to milliseconds
        self.index = 0

        # Create a label for displaying images
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        self.tk_image = None
        self.show_image()

    def show_image(self):
        img = Image.open(self.pictures_list[self.index])
        img = img.resize((800, 600), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_image)

        self.index = (self.index + 1) % len(self.pictures_list)
        self.root.after(self.slide_duration, self.show_image)

# ** Main Script Logic **

# Step 1: Create the Tkinter root window (use the same instance throughout the program)
root = tk.Tk()
root.withdraw()  # Hide the window until the folder is selected

# Step 2: Get the folder and settings
selected_folder = define_directory(root)
if not selected_folder:
    print("Exiting program.")
    exit()

slide_duration, pictures_amount = slide_show_settings()

# Step 3: Get the images from the folder and shuffle them
pictures_list = get_images_from_folder(selected_folder)
if not pictures_list:
    print("No images to display. Exiting program.")
    exit()

# Limit the number of images if the user asks for more than available
if pictures_amount > len(pictures_list):
    print(f"Only {len(pictures_list)} images available, adjusting slideshow.")
    pictures_amount = len(pictures_list)

# Shuffle and select the number of pictures to show
shuffle_images(pictures_list)
pictures_list = pictures_list[:pictures_amount]

# Step 4: Start the slideshow
root.deiconify()  # Show the window again
app = SlideshowApp(root, pictures_list, slide_duration)
root.mainloop()
