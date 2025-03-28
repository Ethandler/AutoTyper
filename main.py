import tkinter as tk
from tkinter import ttk, scrolledtext

# Window setup
root = tk.Tk()
root.title("AutoTyper Robot UI")
root.geometry("1000x600")
root.configure(bg="#282a36")  # Dracula background

# Main frames
left_frame = tk.Frame(root, width=150, bg="#44475a")
left_frame.pack(side=tk.LEFT, fill=tk.Y)

right_frame = tk.Frame(root, width=200, bg="#44475a")
right_frame.pack(side=tk.RIGHT, fill=tk.Y)

bottom_frame = tk.Frame(root, height=150, bg="#44475a")
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

center_frame = tk.Frame(root, bg="#6272a4")
center_frame.pack(expand=True, fill=tk.BOTH)

# Left buttons
start_btn = ttk.Button(left_frame, text="Start Typing")
start_btn.pack(pady=20)

stop_btn = ttk.Button(left_frame, text="Stop Typing")
stop_btn.pack(pady=20)

# Right frame WPM Stats and options
stats_label = ttk.Label(right_frame, text="WPM STATS LIVE", background="#44475a", foreground="#f8f8f2")
stats_label.pack(pady=10)

# God Mode toggle
god_mode_var = tk.BooleanVar()
god_mode_check = ttk.Checkbutton(right_frame, text="God Mode (No Mistakes)", variable=god_mode_var)
god_mode_check.pack(pady=5)

# Mistake toggle
mistake_var = tk.BooleanVar(value=True)
mistake_check = ttk.Checkbutton(right_frame, text="Mistakes On/Off", variable=mistake_var)
mistake_check.pack(pady=5)

# Speed adjustment slider
speed_label = ttk.Label(right_frame, text="Typing Speed", background="#44475a", foreground="#f8f8f2")
speed_label.pack(pady=5)
speed_slider = ttk.Scale(right_frame, from_=50, to=300, orient=tk.HORIZONTAL)
speed_slider.set(100)
speed_slider.pack(pady=5)

# Text entry with face behind
canvas = tk.Canvas(center_frame, bg="#6272a4", highlightthickness=0)
canvas.pack(expand=True, fill=tk.BOTH)

# Robot face (simple)
face = canvas.create_text(500, 150, text="(o_o)", font=("Segoe UI", 60), fill="#bd93f9")

# Transparent text area over face
text_area = scrolledtext.ScrolledText(center_frame, font=("Segoe UI", 14), bg="#6272a4", fg="#f8f8f2", insertbackground="#f8f8f2")
text_area.place(relwidth=1, relheight=1)

# Keyboard and finger placeholders (Bottom frame)
keyboard_label = ttk.Label(bottom_frame, text="[Visual Keyboard & Moving Fingers Here]", background="#44475a", foreground="#f8f8f2")
keyboard_label.pack(expand=True)

root.mainloop()
