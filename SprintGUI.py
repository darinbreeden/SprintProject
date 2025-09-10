import tkinter as tk
from tkinter import ttk

def on_checkbox_toggle():
    status = "checked" if check_var.get() else "unchecked"
    status_label.config(text=f"Checkbox is {status}")

def on_radio_select():
    choice = radio_var.get()
    status_label.config(text=f"Selected option: {choice}")

# Main window
root = tk.Tk()
root.title("Sprint 0 GUI Example")
root.geometry("400x300")

# Label (text)
title_label = ttk.Label(root, text="Demo GUI with Tkinter", font=("Arial", 14))
title_label.pack(pady=10)

# Canvas with lines
canvas = tk.Canvas(root, width=300, height=100, bg="white")
canvas.pack(pady=10)
canvas.create_line(20, 20, 280, 20, fill="blue", width=2)     # horizontal line
canvas.create_line(20, 20, 20, 80, fill="red", width=2)       # vertical line
canvas.create_line(20, 80, 280, 80, fill="green", width=2)    # horizontal line
canvas.create_line(280, 20, 280, 80, fill="black", width=2)   # vertical line

# Checkbox
check_var = tk.BooleanVar()
checkbox = ttk.Checkbutton(root, text="Enable feature", variable=check_var, command=on_checkbox_toggle)
checkbox.pack(pady=5)

# Radio buttons
radio_var = tk.StringVar(value="Option 1")
radio1 = ttk.Radiobutton(root, text="Option 1", value="Option 1", variable=radio_var, command=on_radio_select)
radio2 = ttk.Radiobutton(root, text="Option 2", value="Option 2", variable=radio_var, command=on_radio_select)
radio3 = ttk.Radiobutton(root, text="Option 3", value="Option 3", variable=radio_var, command=on_radio_select)
radio1.pack()
radio2.pack()
radio3.pack()

# Status label (for feedback)
status_label = ttk.Label(root, text="Interact with the checkbox or radio buttons")
status_label.pack(pady=10)

# Run the GUI loop
root.mainloop()
