from tkinter import*
import qrcode
from MyQR import myqr
import os
import re
import tkinter
import base64
from PIL import Image,ImageTk
from resizeimage import resizeimage
from tkinter import messagebox

class QR_Generator:
    def __init__(self,root):
        self.root=root
        self.root.geometry("900x600+200+50")
        self.root.title("*** QR Code Generator ***")
        self.root.resizable(False,False)

        self.background_image = ImageTk.PhotoImage(Image.open("gene.jpg").resize((900,600)))
        self.background_label = tkinter.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.head_icon = ImageTk.PhotoImage(Image.open("logo.png").resize((50, 50)))
        #title=Label(self.root,text="  QR Code Generator",compound="left", image=self.head_icon, font=("Times New Roman",40),bg='#053246',fg='white',anchor='w').place(x=0,y=0,relwidth=1)
        stud_title=Label(root,text="QR Code Generator", compound="left", image=self.head_icon,font=("Arial", 18, "bold"), fg="#fff", bg="#B91080", padx=20, border=5,relief="groove").place(x=442,y=95,relwidth=0.375,relheight=0.1)

        #-----Student Details---
        self.var_stud_code=StringVar()
        self.var_stud_name=StringVar()
        self.var_Mobile=StringVar()
        self.var_program=StringVar()
        self.res1=BooleanVar()
        self.res2=BooleanVar()
        self.res3=BooleanVar()
        self.res4=BooleanVar()

        stud_Frame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        stud_Frame.place(x=120,y=160,width=300,height=330)
        stud_title=Label(stud_Frame,text="Student Details", font=("Arial", 16, "bold"), fg="#fff", bg="#2572C5", padx=20, border=5,relief="groove").place(x=0,y=0,relwidth=1,relheight=0.16)

        lbl_stud_code=Label(stud_Frame,text="Roll No", font=("Times New Roman",15,'bold'),bg='white').place(x=10,y=70)
        lbl_name=Label(stud_Frame,text="Name", font=("Times New Roman",15,'bold'),bg='white').place(x=10,y=110)
        lbl_Mobile=Label(stud_Frame,text="Mobile No.", font=("Times New Roman",15,'bold'),bg='white').place(x=10,y=150)
        lbl_program=Label(stud_Frame,text="Program", font=("Times New Roman",15,'bold'),bg='white').place(x=10,y=190)

        txt_stud_code=Entry(stud_Frame, font=("Times New Roman",14 ),textvariable=self.var_stud_code,bg='lightyellow')
        txt_stud_code.place(x=115,y=70,width=175)
        txt_stud_code.bind("<FocusOut>", self.validate_stud_code)

        txt_name=Entry(stud_Frame, font=("Times New Roman",14 ),textvariable=self.var_stud_name,bg='lightyellow')
        txt_name.place(x=115,y=110,width=175)
        txt_name.bind("<FocusOut>", self.validate_stud_name)

        txt_Mobile=Entry(stud_Frame, font=("Times New Roman",15 ),textvariable=self.var_Mobile,bg='lightyellow')
        txt_Mobile.place(x=115,y=150,width=175)
        txt_Mobile.bind("<FocusOut>", self.validate_mobile)

        txt_program=Entry(stud_Frame, font=("Times New Roman",15 ),textvariable=self.var_program,bg='lightyellow')
        txt_program.place(x=115,y=190,width=175)
        txt_program.bind("<FocusOut>", self.validate_program)

        btn_generator=Button(stud_Frame,text="QR Generate",command=self.generate,font=("Times New Roman",16,'bold'),bg='#2196f3',fg='white').place(x=20,y=250,width=140,height=30)
        btn_clear=Button(stud_Frame,text="Clear",command=self.clear,font=("Times New Roman",16,'bold'),bg='#607d8b',fg='white').place(x=180,y=250,width=85,height=30)

        self.msg=""
        self.lbl_msg=Label(stud_Frame,text=self.msg, font=("Times New Roman",17,"bold"),bg='white',fg='green')
        self.lbl_msg.place(x=5,y=290,relwidth=1)

        self.qr_code=Label(root,text="QR Code \nNot Available!",font=('Times New Roman',14),bg='#0355B6',fg='white',bd=1,relief=RIDGE)
        self.qr_code.place(x=555,y=205,width=110,height=110)

        self.back_frame = tkinter.Frame(self.root)
        self.back_frame.pack(pady=(470, 0), padx=(550, 0))
        self.back_button = tkinter.Button(self.back_frame, text="Back", font=("Arial", 14,"bold"), fg="#fff", bg="#B91080", padx=15, border=5,relief="groove", compound='left',command=self.close_scanner)
        self.back_button.pack(side=tkinter.LEFT, padx=0)

    def validate_stud_code(self,event):
        if not re.match(r'^[0-9]{2}$', event.widget.get()):
            messagebox.showerror("Error", "Invalid Student Roll Number!!!")
            self.res1=False
        else:
            self.res1=True
    
    def validate_stud_name(self,event):
        if not re.match(r'^[a-zA-Z\s]{2,}$', event.widget.get()):
            messagebox.showerror("Error", "Invalid Student Name!!!")
            self.res2=False
        else:
            self.res2=True

    def validate_mobile(self,event):
        if not re.match(r'^[7-9]\d{9}$', event.widget.get()):
            messagebox.showerror("Error", "Invalid Student Mobile Number!!!")
            self.res3=False
        else:
            self.res3=True

    def validate_program(self,event):
        if not re.match(r"^(CM|CO)[1-6][Ii]$", event.widget.get()):
            messagebox.showerror("Error", "Invalid Student Program!!!")
            self.res4=False
        else:
            self.res4=True
        
        
    def close_scanner(self):
        self.root.destroy()

    def clear(self):
        self.var_stud_code.set('')
        self.var_stud_name.set('')
        self.var_Mobile.set('')
        self.var_program.set('')
        self.msg=""
        self.lbl_msg.config(text=self.msg)
        self.qr_code.config(image='')

    def generate(self):
        if not(bool(self.res1) and bool(self.res2) and bool(self.res3) and bool(self.res4)):
            self.msg="Please enter all fields!!!"
            self.lbl_msg.config(text=self.msg,fg='red')
        else:
            qr_data=(f"Student ID:{self.var_stud_code.get()}\nStudent Name:{self.var_stud_name.get()}\nMobile No.:{self.var_Mobile.get()}\nProgram:{self.var_program.get()}")
            rollno=(f"{self.var_stud_code.get()}")
            data=qr_data.encode('utf-8')
            name=str(base64.b64encode(data).decode())
                
            version, level, qr_name = myqr.run(
            str(name),
            version = 1,
            level = 'H',
            colorized = True, 
            contrast = 1.0,
            brightness = 1.0,
            save_name = str("Stud_"+rollno+'.bmp'),
            save_dir = "E:/QR Code Scanner and Generator/Qr Generate/QR_Code"
            )

            image = Image.open("E:/QR Code Scanner and Generator/Qr Generate/QR_Code/Stud_"+str(self.var_stud_code.get()+'.bmp'))
            qr_code=resizeimage.resize_cover(image,[110,110])
            qr_code.save("E:/QR Code Scanner and Generator/Qr Generate/QR_Code/Stud_"+str(self.var_stud_code.get()+'.bmp'))
            self.im=ImageTk.PhotoImage(file="E:/QR Code Scanner and Generator/Qr Generate/QR_Code/Stud_"+str(self.var_stud_code.get()+'.bmp'))
            self.qr_code.config(image=self.im)

            #---- Update Notification ----
            self.msg="QR Generated Successfully!!!"
            self.lbl_msg.config(text=self.msg,fg='green')

root=Tk()
obj =QR_Generator(root)
root.mainloop()