import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import base64
import time
import sys
import datetime
import xlwt 
from xlwt import Workbook
import tkinter as tk
from PIL import ImageTk, Image

class QRScanner:
    def __init__(self, master):
        self.master = master
        self.master.title("QR Code Scanner")
        self.master.geometry("700x467")
        self.master.resizable(False, False)

        # Set up the background image
        self.background_image = ImageTk.PhotoImage(Image.open("scan.jpg").resize((700,467)))
        self.background_label = tk.Label(self.master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.head_icon = ImageTk.PhotoImage(Image.open("logo.png").resize((50, 50)))
        self.heading_label = tk.Label(root, text="QR Code Scanner", compound="left", image=self.head_icon, font=("Arial", 16, "bold"), fg="#fff", bg="#B91080", padx=20, border=5,relief="groove")
        self.heading_label.place(x=64, y=80, relwidth=0.45, relheight=0.09)

        self.photo_img = ImageTk.PhotoImage(Image.open("card.png").resize((180,98)))
        self.img_label = tk.Label(self.master, image=self.photo_img)
        self.img_label.place(x=90, y=245)

        self.scanner_frame = tk.Frame(self.master)
        self.scanner_frame.pack(pady=(365, 0), padx=(0, 380))
        self.scanner_button = tk.Button(self.scanner_frame, text="ScanQR Now", font=("Arial", 14,"bold"), fg="#fff", bg="#007bff", relief="raised", borderwidth=3, compound='left',command=self.open_scanner)
        self.scanner_button.pack(side=tk.LEFT, padx=0)

        self.back_frame = tk.Frame(self.master)
        self.back_frame.pack(pady=(8, 0), padx=(0, 0))
        self.back_button = tk.Button(self.back_frame, text="Back", font=("Arial", 14,"bold"), fg="#fff", bg="#007bff", relief="raised", borderwidth=3, compound='left',command=self.close_scanner)
        self.back_button.pack(side=tk.LEFT, padx=0)
    
    def close_scanner(self):
        cv2.destroyAllWindows()
        self.master.destroy()

    def open_scanner(self):
        
        cap = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_PLAIN

        fob=open('attendence.txt','w+')

        names=[]
        codes=[]
        ids=[]
        def enterData(z):
            if z in names:
                pass
            else:
                ch1=z.split(":")
                ch2=ch1[2].split("\n")
                ch3=ch1[1].split("\n")
                
                ids.append(ch3[0])
                a=''.join(str(ch3[0]))
                fob.write(a+' : ')
                
                names.append(ch2[0])
                a=''.join(str(ch2[0]))
                fob.write(a+' : ')

                now = datetime.datetime.now()
                date_str = now.strftime("%d-%m-%Y %I:%M:%S %p")
                codes.append(date_str)
                fob.write(date_str+'\n')
            return names

        print('Reading...')
        def checkData(data):
            try:
                data=str(base64.b64decode(data).decode())
            except(Exception):
                print('Invalid QR Code!!!')
                return
           
            ch1=data.split(":")
            ch2=ch1[2].split("\n")
            ch3=ch1[1].split("\n")
            ch4=ch2[0].split(" ")

            if ch2[0] in names: 
                print(ch4[1]+' is Already Present')                    
            else:
                try:
                    image = Image.open("E:/QR Code Scanner and Generator/Qr Generate/QR_Code/Stud_"+ch3[0]+'.bmp')
                    decodedObjs = pyzbar.decode(image)
                    for o in decodedObjs:
                        data2=str(base64.b64decode(o.data).decode())

                    if data==data2:
                        print('\n'+str(len(names)+1)+'\n'+data)
                        enterData(data)
                        cv2.putText(frame, str(ch2[0]), (50, 50), font, 2,
                            (255, 0, 0), 3)
                except(Exception):
                    print("Invalid QR!!!No such record Present...")
                    cv2.putText(frame, str("Invalid QR!!!No such record Present..."), (50, 50), font, 2,
                                (255, 0, 0), 3)
        while True:
            _, frame = cap.read()
        
            decodedObjects = pyzbar.decode(frame)
            for obj in decodedObjects:
                checkData(obj.data)
                time.sleep(1)
            
            cv2.imshow("Frame", frame)

            if cv2.waitKey(1)& 0xFF == ord('s'):
                cv2.destroyAllWindows()
                self.master.destroy()
                break
            
        fob.close()

        d_date = datetime.datetime.now()
        reg_format_date = d_date.strftime("%d-%m-%Y %I-%M-%S %p")
        reg_format_date = reg_format_date.replace(':', '-')

        def writeExcel(ids,names,codes,reg_format_date):
            wb = xlwt.Workbook()            
            sheet1 = wb.add_sheet('Sheet 1')
            sheet1.col(0).width = 20 * 150
            sheet1.col(1).width = 21 * 275
            sheet1.col(2).width = 21 * 256

            header_format = xlwt.Style.easyxf('font: bold 1; pattern: pattern solid, fore_colour blue, back_colour white; align: horiz center;')
            
            sheet1.write(0, 0, 'Student ID', header_format)
            sheet1.write(0, 1, 'Name', header_format)
            sheet1.write(0, 2, 'Time', header_format)

            for i in range(0,len(names)): 
                sheet1.write(i+1, 0, ids[i], xlwt.Style.easyxf('align: horiz center;'))
                sheet1.write(i+1, 1, names[i])
                sheet1.write(i+1, 2, codes[i])
            wb.save(reg_format_date+'.xls')
        writeExcel(ids,names,codes,reg_format_date)        

if __name__ == '__main__':
    root = tk.Tk()
    app = QRScanner(root)
    root.mainloop()