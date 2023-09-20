import tkinter as tk
import subprocess
from PIL import ImageTk, Image

class QRCodeScannerGeneratorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("QR Code Scanner and Generator")
        self.master.geometry("800x600")
        self.master.resizable(False, False)

        self.background_image = ImageTk.PhotoImage(Image.open("best.jpg").resize((800,600)))
        self.background_label = tk.Label(self.master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.head_icon = ImageTk.PhotoImage(Image.open("logo.png").resize((50, 50)))
        self.heading_label = tk.Label(root, text="QR Code Scanner and Generator", compound="left", image=self.head_icon, font=("Arial", 24, "bold"), fg="#fff", bg="#2572C5", padx=20, border=5,relief="groove")
        self.heading_label.place(x=62, y=82, relwidth=0.845, relheight=0.1)

        self.scanner_frame = tk.Frame(self.master)
        self.scanner_frame.pack(pady=(300, 20), padx=(0, 325))
        self.scanner_icon = ImageTk.PhotoImage(Image.open("scanner.png").resize((40, 40)))
        self.scanner_button = tk.Button(self.scanner_frame, text="QR Code Scanner", font=("Arial", 16), fg="#fff", bg="#007bff", relief="raised", borderwidth=5, compound='left', image=self.scanner_icon, command=self.open_scanner)
        self.scanner_button.pack(side=tk.LEFT, padx=0)

        self.generator_frame = tk.Frame(self.master)
        self.generator_frame.pack(pady=(13, 50), padx=(0, 325))
        self.generator_icon = ImageTk.PhotoImage(Image.open("generator.png").resize((40, 40)))
        self.generator_button = tk.Button(self.generator_frame, text="QR Code Generator", font=("Arial", 16), fg="#fff", bg="#007bff", relief="raised", borderwidth=5, compound='left', image=self.generator_icon, command=self.open_generator)
        self.generator_button.pack(side=tk.LEFT, padx=0)

        self.back_frame = tk.Frame(self.master)
        self.back_frame.pack(pady=(30, 0), padx=(550, 0))
        self.back_button = tk.Button(self.back_frame, text="Close", font=("Arial", 14,"bold"), fg="#fff", bg="#2572C5", relief="raised", borderwidth=3, compound='left',command=self.close_scanner)
        self.back_button.pack(side=tk.LEFT, padx=0)

    def close_scanner(self):
        self.master.destroy()
        
    def open_scanner(self):
        subprocess.call(["python", "Qr_Scanner.py"])

    def open_generator(self):
        subprocess.call(["python", "Qr Generate/Qr_Generate.py"])

if __name__ == '__main__':
    root = tk.Tk()
    app = QRCodeScannerGeneratorGUI(root)
    root.mainloop()