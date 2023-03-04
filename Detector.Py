# Face detection GUI written by Th3K3y
# This code allows the user to import an image and analyze whether it contains a face or not.

import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

class FaceDetector:
    def __init__(self, master):
        self.master = master
        master.title("Face Detector")
        
        master.configure(bg='#404252')
        
        self.filename = ""
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        self.frame = tk.Frame(master, bg='#404252')
        self.frame.pack(pady=20)

        self.canvas = tk.Canvas(self.frame, width=400, height=400, bg='white', highlightthickness=0, bd=4, relief='groove')
        self.canvas.pack(pady=10)

        style = ttk.Style()
        style.configure('Custom.TButton', padding=10, relief='flat', background='#c1c1c1', foreground='#404252', font=('Segoe UI', 12))
        
        self.load_button = ttk.Button(master, text="Load Image", command=self.load_image, style='Custom.TButton')
        self.load_button.pack(pady=10)

        self.analyze_button = ttk.Button(master, text="Analyze", command=self.analyze_image, style='Custom.TButton')
        self.analyze_button.pack(pady=10)
        
        self.result_label = tk.Label(master, text="", bg='#404252', font=('Segoe UI', 12))
        self.result_label.pack()

    def load_image(self):
        self.filename = filedialog.askopenfilename(initialdir=".", title="Select Image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

        try:
            self.img = cv2.imread(self.filename)

            if self.img is None:
                messagebox.showerror("Error", "Invalid image file!")
                return

            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            self.photo = tk.PhotoImage(data=cv2.imencode('.png', self.img)[1].tostring())
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            self.center_on_face()

        except:
            messagebox.showerror("Error", "Failed to load image!")

    def analyze_image(self):
        if self.filename == "":
            messagebox.showerror("Error", "No image loaded!")
            return

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            messagebox.showinfo("Face Detection Result", "Face not detected!")
        else:
            messagebox.showinfo("Face Detection Result", "Face detected!")
            
    def center_on_face(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            center_x = x + w // 2
            center_y = y + h // 2
            x_shift = self.canvas.winfo_width() // 2 - center_x
            y_shift = self.canvas.winfo_height() // 2 - center_y

            self.canvas.move(tk.ALL, x_shift, y_shift)
            
        self.result_label.config(text="")

root = tk.Tk()
app = FaceDetector(root)
root.geometry("500x600")
root.resizable(width=False, height=False)
root.mainloop()