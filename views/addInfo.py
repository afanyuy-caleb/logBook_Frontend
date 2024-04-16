from tkinter import *
import ttkbootstrap as tb
import tkinter.messagebox as messageBox
 


cond = f"course_name = '{Cname}'"
status, c_info = courCT.load(cond)

if(status):
  print(status, c_info)
else:
  messageBox.showerror("Error", "Read data error")

window = Tk()
window.geometry("400x400")
window.title(f"{Cname} Details")

# Date entry
cur_date = tb.DateEntry(window, bootstyle="RoyalBlue1")
cur_date.pack()

# btn = Button(window, text="Close", command=window.destroy)
# btn.pack()

window.mainloop()
