from tkinter import *
import os
import sys
current_dir = os.getcwd()
sys.path.append(current_dir)
import tkinter.messagebox as messageBox
from tkinter import font, filedialog, ttk
from . import shared_data
import viewmodels.courses as courCT
import viewmodels.classes as clsCT
import viewmodels.addInfo_ctrl as addCT
import ttkbootstrap as tb
from PIL import Image, ImageTk
import datetime, json


def studentHome():

  studData = shared_data.studInfo

  image_dir_path = "views/Images/courImgs"

  # Check if the image directory exists
  dir_path = os.path.join(current_dir, image_dir_path)

  def set_cls(opt):

    global cls_id

    for row in classes:

      if row[1] == opt:
        cls_id = row[0]
        break

    # Destroy the Info dialog if it has been set
    try:
      myFrame.destroy()
      btn.destroy()

    except NameError:
      pass

    finally:
      set_courses("change")

  def addInfo(Cname):

    def saveImage():

      if not os.path.exists(dir_path):
        os.makedirs(dir_path)

      try:

        file_name = os.path.basename(file_path)
        ext = file_name.split('.')[-1]
        cur_time = datetime.datetime.now().time()
        new_name = str(cur_time) + '.'+ ext

        # Modify the new name to be without special characters
        new_name = new_name.replace(":", '')
        dest_file = os.path.join(dir_path, new_name)

        # Copy the image file to the destination directory with the new file name
        with open(file_path, 'rb') as f:
          m = f.read()
        with open(dest_file, 'wb') as q:
          q.write(m)

        return True, new_name

      except Exception as e:
        return False, e


    def open_image():
      global file_path

      # Open file dialog to select an image file
      file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp *.svg *.avif *.gif *.ico")])

      # Check if a file was selected
      if file_path:
        # Load the image using PIL
        image = Image.open(file_path)

        # Resize the image to fit within a specific width and height
        image.thumbnail((150, 150))

        # Convert the image to Tkinter-compatible format
        photo = ImageTk.PhotoImage(image)

        # Update the image label with the new image
        image_label.config(image=photo)
        image_label.photo = photo

    
    def saveData():

      stat, file_name = saveImage()
      if not stat:
       file_name = ""
      
      stats, msg = addCT.add_course_details(cur_date.entry.get(), desc_text.get("1.0", END).strip(), file_name, cour_id)

      if(stats):
        messageBox.showinfo("Success", msg)
        info_dialog.destroy()
        display_info(Cname)

      else:
        messageBox.showerror("Error!!", msg)


    info_dialog = Toplevel(root)
    info_dialog.transient(root)
    info_dialog.grab_set()

    # Place the dialog at the center of the parent
    par_x = root.winfo_rootx()
    par_y = root.winfo_rooty()
    x = par_x + 275
    y = par_y + 100
    info_dialog.geometry(f"550x600+{x}+{y}")

    info_label = Label(info_dialog, text="Enter Course Details", font=('Comic Sans MS', 14, 'bold'), bg="white")
    info_label.place(relx=0.3, rely=0.025)

    # Date entry
    date_label = Label(info_dialog, text="Enter Date:")
    date_label.place(relx=0.05, rely=0.11)

    cur_date = tb.DateEntry(info_dialog, bootstyle="RoyalBlue1")
    cur_date.place(relx=0.05, rely=0.15)

    # The description area
    desc_label = Label(info_dialog, text="Enter Description:")
    desc_label.place(relx=0.05, rely=0.25)

    desc_text = Text(info_dialog, height=8, width=70)
    desc_text.place(relx=0.05, rely=0.3)

    # Image upload
    upload_button = Button(info_dialog, text="Upload Image", command=open_image)
    upload_button.place(relx=0.05, rely=0.55)

    # Create a label to display the image preview
    image_label = Label(info_dialog)
    image_label.place(relx=0.05, rely=0.6)

    # Add btn
    add_btn = Button(info_dialog, text="Add", pady=6, padx=8, bg="RoyalBlue1", fg="white", bd=0, command=saveData)
    add_btn.place(relx=0.05, rely=0.9)  
    

  def display_info(sub):

    global myFrame, btn, cour_id

    myFrame = Frame(root, bg="white", width="700", height="600", bd=0)
    myFrame.place(relx=0.32, rely=0.12)

    title = Label(myFrame, text = sub, font=('Comic Sans MS', 12), bg="white")
    title.place(relx=0.35, rely=0)
     
    # Get the dimensions of the title, so we can centralize in the frame
    title.update_idletasks()
    myFrame.update()
    title_width = title.winfo_width()
    wid = (myFrame.winfo_width() - title_width) / 15

    title.place(x=wid, rely=0.03)

    myCanvas = Canvas(myFrame, scrollregion=(0,0, 1400, 1000))
    myCanvas.place(relx=0, rely=0.1, relwidth=1.0, relheight=1.0)

    infoFrame = Frame(myCanvas, bd=1)
    infoFrame.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
    infoFrame.configure(background="white smoke")

    # Configure the scrollbar

    scroll_y = Scrollbar(myFrame, orient=VERTICAL, command=myCanvas.yview)
    scroll_y.place(relx=1, rely=0, relheight=1, anchor="ne")

    # myCanvas.create_window((0,0), window=infoFrame)
    myCanvas.configure(yscrollcommand=scroll_y.set)

    # Title header
    date_label = Label(infoFrame, text="Date", font=('Comic Sans MS', 12, 'bold'))
    date_label.place(relx=0.1, rely=0.01)
  
    desc_label = Label(infoFrame, text="Description", font=('Comic Sans MS', 12, 'bold'))
    desc_label.place(relx=0.38, rely=0.01)

    img_label = Label(infoFrame, text="Image", font=('Comic Sans MS', 12, 'bold'))
    img_label.place(relx=0.75, rely=0.01)

    # Grey line to separate the header
    sep_line = Frame(infoFrame, height=2)
    sep_line.configure(bg="gray63")
    sep_line.place(relx=0, rely=0.07, relwidth=1.0)

    # We display the information based on the class that has been selected
    # By default, the class is that of the student

     # Get the course_id
    for row in courses:
      if row[1] == sub:
        cour_id = row[0]
        break
    
    try:
      if cls_id:
        cond = f"course_id = {cour_id} AND class_id = {cls_id}"
        stat, data = addCT.get_course_details(cond)
        
    except NameError:
      cond = f"course_id = {cour_id} AND class_id = {studData['class_id']}"
      stat, data = addCT.get_course_details(cond)

    if not stat:
      messageBox.showerror("Error", 'Error occured when loading data')
      myFrame.destroy()
      return  
    
    try:

      data = json.loads(data[0][1])
      

      if data:

        y = 0.08
        for row in data:
          x = 0.05
          for key in row:
            if key == 'img' and row[key] != "":
              x += 0.2
              img_path = dir_path + f"/{row[key]}"

              try:
                image_tk = Image.open(img_path)
                image_tk.thumbnail((200, 100))

                image_tk = ImageTk.PhotoImage(image_tk)

                item = Label(infoFrame)
                item.config(image=image_tk)
                item.photo = image_tk
                
                item.place(relx=x, rely=y)

              except Exception as e:
                print("Error printing image", e)

            elif key == 'desc':
              x -=0.12
              item = Label(infoFrame, text = row[key], width=35, height=5, bd=1, anchor="center", wraplength=230)
              item.config(bg="white smoke")
              item.place(relx=x, rely=y)

            else:
              item = Label(infoFrame, text = row[key], height=5, width=15)
              item.config(bg="white smoke")
              item.place(relx=x, rely=y)

            x += 0.3
          
          y += 0.2

    except TypeError:
      pass
      
    # Trying to display the add record button just for the delegates of the respective classes
    if studData['role_id'] == 1:

      try:
        if cls_id != studData['class_id']:
          return
        
        else:
          btn = Button(root, text="Add Record", pady=6, padx=8, bg="RoyalBlue1", fg="white", bd=0, command=lambda : addInfo(sub))
          btn.place(relx=0.6, rely=0.9)  
         
      except NameError:
        btn = Button(root, text="Add Record", pady=6, padx=8, bg="RoyalBlue1", fg="white", bd=0, command=lambda : addInfo(sub))
        btn.place(relx=0.6, rely=0.9)  


  # main  GUI 
      
  root = Tk()

  # Centralize the root widget
  screen_wid = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()

  r_width = 1100
  r_height = 800

  x = (screen_wid - r_width) // 2
  y = (screen_height - r_height) // 2

  root.geometry(f"{r_width}x{r_height}+{x}+{y}")
  root.title("IAI logBook")
  root.resizable(False, False)
  root.configure(bg="white")

  
  # icon
  icon_img = current_dir + '/icon.ico'
  root.iconbitmap(icon_img)

  # Customize the font family
  custom_font = font.Font(family="Comic Sans MS", size=11)
  root.option_add("*Font", custom_font)

  studName = studData['name'] + "(Delegate)" if studData["role_id"] == 1 else studData["name"]
  homeLabel = Label(root, text=studName, font=('Comic Sans MS', 18, 'bold'), bg="white")
  
  root.update()
  homeLabel.update()

  hm_w = homeLabel.winfo_width()
  r_w = (root.winfo_width() - hm_w) / 2.5

  homeLabel.place(x=r_w, rely=0.03)

  # Choose class

  cls_label = Label(root, text="Choose Class:", bg="white")
  cls_label.place(relx=0.01, rely=0.15)

  def set_classes():
    global classes
    status, classes = clsCT.load()

    if(status):
      clsOptions = [row[1] for row in classes]
      
    else:
      messageBox.showerror("Error", "Error loading class options")

    for cls in classes:
      if cls[0] == studData['class_id']:
        cur_class = cls[1]
        break

    cls_opt = StringVar()
    cls_opt.set(cur_class)

    clsOption_menu = OptionMenu(root, cls_opt, *clsOptions, command=lambda opt=cls_opt : set_cls(opt))
    clsOption_menu.configure(background="RoyalBlue1", fg="white", bd=0, padx=10, pady=6)
    clsOption_menu.place(relx=0.015, rely=0.185)

  set_classes()
  # Choose course

  course_label = Label(root, text="Select Course:", bg="white")
  course_label.place(relx=0.011, rely=0.35)

  # Check if class has been selected
  def set_courses(tester = None):
    global option_menu, courses

    try:
      cond = f"course_id in (SELECT course_id FROM class_courses WHERE class_id = {cls_id})"
      status, courses = courCT.load(cond) 
      
    except Exception as e:
      cond = f"course_id in (SELECT course_id FROM class_courses WHERE class_id = {studData['class_id']})"
      status, courses = courCT.load(cond) 

    finally:

      if(status):
        options = [row[1] for row in courses]

        sel_opt = StringVar()
        sel_opt.set("None")

        if tester:
          option_menu.destroy()

        option_menu = OptionMenu(root, sel_opt, *options, command=lambda opt=sel_opt: display_info(opt))
        option_menu.configure(background="RoyalBlue1", fg="white", bd=0, padx=10, pady=6)
        option_menu.place(relx=0.01, rely=0.385)

      else:
        messageBox.showerror("Error", courses)

  set_courses()

  
  root.mainloop()