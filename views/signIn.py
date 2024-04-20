import sys
import os
current_dir = os.getcwd()
sys.path.append(current_dir)
from tkinter import *
import tkinter.messagebox as messageBox
import viewmodels.courses as courCT
import viewmodels.classes as clsCT
import viewmodels.students as studCT
from . import shared_data
from PIL import Image, ImageTk
from tkinter import filedialog, font

# Functions

def SignIn():

  def on_enter(event):
    if nameEntry.get() == 'Enter Full Names':
      nameEntry.delete(0,END)

  def checkValues():
    
    if nameEntry.get() == "" or nameEntry.get() == 'Enter Full Names':
      messageBox.showerror('Name error', "Name entry required")
      return
    elif sel_opt.get() == 'None':
      messageBox.showerror("Class", "Class required")
    else:
      name = nameEntry.get().lower()
      opt = sel_opt.get()

      for op in allOptions:
        if op[1] == opt:
          id = op[0]
          break
      condition =  f"class_id = {id} AND name = '{name}'"
      status, names = studCT.load(condition)

      if(status):
        if(names):
          row = names[0]

          keys = ['id', 'name', 'dob', 'gender', 'Tel', 'role_id', 'class_id']

          shared_data.studInfo = {key: value for key, value in zip(keys, row)}
      
          window.destroy()
        else:
          messageBox.showerror('Error', f"student {name} doesn't exist in {opt}")
      else:
        messageBox.showinfo('Data', names)

          
  # GUI part

  window = Tk()

  # Centralize the root window
  srn_wid = window.winfo_screenwidth()
  srn_hgt = window.winfo_screenheight()
  win_wid = 600
  win_hgt = 600

  x = (srn_wid - win_wid) // 2
  y = (srn_hgt - win_hgt) // 2

  window.geometry(f"{win_wid}x{win_hgt}+{x}+{y}")
  window.title("IAI logBook")

  window.resizable(False, False)
  
  icon_img = current_dir + '/icon.ico'
  # icon
  window.iconbitmap(icon_img)

  # Customize the font family
  custom_font = font.Font(family="Comic Sans MS", size=11)
  window.option_add("*Font", custom_font)

  # image
  img_path = current_dir + '/views/Images/tagging photo.png'
  image = Image.open(img_path) 

  img_size = (100, 100)
  image = image.resize(img_size, Image.Resampling.LANCZOS)

  image_tk = ImageTk.PhotoImage(image)

  label = Label(window, image=image_tk)
  label.place(relx=0.4, rely=0.025)

  myFrame = Frame(window, bg="#fff", width="400", height="300")
  myFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

  loginLabel = Label(myFrame, text="Welcome Back", font=('Comic Sans MS', 18, 'bold'), bg="#fff")
  loginLabel.place(relx=0.3, rely=0.1)

  nameEntry = Entry(myFrame, width=45, font= 10, bg="#fff", bd=0)
  nameEntry.configure(font=('Comic Sans MS', 11))
  nameEntry.place(relx=0.1, rely=0.3)
  nameEntry.insert(3, 'Enter Full Names')
  nameEntry.bind('<FocusIn>', on_enter)

  nameFrame = Frame(myFrame, width=320, height=1.5, bg="RoyalBlue1")
  nameFrame.place(relx=0.09, rely=0.38)

  status, allOptions = clsCT.load()

  if(status):
    options = [row[1] for row in allOptions]
  else:
    messageBox.showerror("Error", allOptions)

  sel_opt = StringVar()
  sel_opt.set('None')

  sel_input = OptionMenu(myFrame, sel_opt, *options)
  sel_input.place(relx=0.36, rely=0.49)  

  classLabel = Label(myFrame, text="Choose class:", bg="#fff")
  classLabel.place(relx=0.1, rely=0.5)

  loginBtn = Button(myFrame, bg="RoyalBlue1", height=2, width=17, font=('Helvetica', 12, 'bold'), fg="alice blue", text="Login", bd=0, command = checkValues)
  loginBtn.place(relx=0.25, rely=0.7)

  window.mainloop()
