import tkinter as tk

def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

root = tk.Tk()
root.geometry("300x200")

# Create a scrollable text area
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Add some text to the scrollable frame
for i in range(50):
    tk.Label(scrollable_frame, text="This is label {}".format(i)).pack()

# Bind mouse wheel event to the canvas
canvas.bind_all("<MouseWheel>", on_mousewheel)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()
