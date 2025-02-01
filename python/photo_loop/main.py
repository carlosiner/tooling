import os
import sys
import random  
from itertools import cycle
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, simpledialog

class PhotoLoopApp:
    """
    A class to visualize images in full screen from folders in a loop.
    """
    def __init__(self, folder_path=None, delay=5, shuffle=True):
        """
        Initialize the PhotoLoopApp.

        :param folder_path: Path to the folder containing images.
        :param delay: Delay between images in seconds.
        :param shuffle: Shuffle the images (default: True).
        """
        self.delay = delay*1000
        self.folder_path = folder_path
        self.image_files = self.get_image_files()
        if shuffle:
            # Shuffle the image files
            random.shuffle(self.image_files)  
        self.image_cycle = cycle(self.image_files)
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)
        self.window.configure(background='black')
        self.label = tk.Label(self.window, highlightthickness=0)
        self.label.pack()
        # Bind the Escape key to exit the full screen mode
        self.window.bind("<Escape>", self.exit_fullscreen)
        self.show_next_image()



    def get_image_files(self):
        """
        Get a list of image files in the folder and subfolders.

        :return: List of image file paths.
        """
        image_files = []
        for window, dirs, files in os.walk(self.folder_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    image_files.append(os.path.join(window, file))
        return image_files

    def show_next_image(self):
        """
        Display the next image in the cycle.
        """
        image_path = next(self.image_cycle)
        try:
            image = Image.open(image_path)
        except Exception as e:
            print(f"Error: {e}")
            self.show_next_image()
            return
        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo
        self.window.after(self.delay, self.show_next_image)

    def exit_fullscreen(self, event=None):
        """
        Exit the full screen mode and quit the application.

        :param event: Event object (optional).
        """
        self.window.attributes('-fullscreen', False)
        self.window.quit()

    def run(self):
        """
        Run the Tkinter main loop.
        """
        self.window.mainloop()

def get_user_input():
    """
    Get user input for delay and shuffle parameters.
    """
    delay = simpledialog.askinteger("Input", "Enter delay between images (seconds):", minvalue=1, maxvalue=60, initialvalue=5)
    shuffle = simpledialog.askstring("Input", "Shuffle images? (y/n):", initialvalue='y').lower() == 'y'
    
    return delay, shuffle

def select_folder():
    """
    Open a folder selection dialog and return the selected folder path.

    :return: Selected folder path.
    """
    folder_path = filedialog.askdirectory(title="Select Folder")
    if not folder_path:
        sys.exit("No folder selected. Exiting.")
    return folder_path

if __name__ == "__main__":
    print("Start")

    delay,shuffle = get_user_input()
    print("\n Delay: " + str(delay) + " Shuffle? : "+str(shuffle))
    # Argument: Folder path if not provided, open a folder selection dialog
    folder_path = sys.argv[1] if len(sys.argv) > 1 else None
    if not folder_path:
        folder_path = select_folder()
    print("\n Folder selected: "+str(folder_path))

    app = PhotoLoopApp(folder_path, delay, shuffle)
    app.run()
