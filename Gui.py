import tkinter as tk
from Trakers import start_keyboard_listener, start_mouse_tracking

def create_gui():
    """Create the main GUI window."""
    root = tk.Tk()
    root.geometry("400x400")
    
    start_button = tk.Button(root, text="Start")
    start_button.pack(pady=10)

    mouse_button = tk.Button(root, text="Track Mouse", command=start_mouse_tracking)
    mouse_button.pack(pady=10)

    keyboard_button = tk.Button(root, text="Keyboard", command=start_keyboard_listener)
    keyboard_button.pack(pady=10)
    
    root.mainloop()