"""
main.py
Main Tkinter UI that orchestrates everything:
- 5-second pre-typing delay (handled in typer.py).
- Scheduling popup with multiple scheduling options (scheduler.py).
- Show WPM Graph in a separate window (matplotlib).
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys, os, time

# Ensure Python can find the "modules" folder
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Imports from modules
from modules import typer, scheduler
from modules import profiles, analytics, importer, shortcuts, sounds

# Optional plotting for the graph window
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
root.title("AutoTyper – Dracula Edition")
root.geometry("900x600")

# If you have a dracula_theme.py, apply it if not comment it out.
from ui.dracula_theme import apply_dracula_theme
apply_dracula_theme(root)

# -------------------- UI ELEMENTS --------------------
text_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Segoe UI", 12),
    bg="#44475A",
    fg="#F8F8F2",
    insertbackground="#F8F8F2"
)
text_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(fill=tk.X, padx=15, pady=5)

status_label = ttk.Label(root, text="Ready")
status_label.pack(pady=10)

typing_thread = None
is_typing = False

# -------------------- CALLBACKS --------------------
def on_progress_update(percentage):
    """Callback from typer.py to update progress bar."""
    progress_var.set(percentage)

def on_typing_finished(final_wpm, mistakes):
    """Callback from typer.py when typing completes."""
    global is_typing
    is_typing = False
    status_label.config(text=f"Finished! WPM: {final_wpm} | Mistakes: {mistakes}")

def start_typing():
    """Start typing in a separate thread."""
    global typing_thread, is_typing
    if is_typing:
        messagebox.showinfo("Info", "Already typing!")
        return

    raw_text = text_area.get("1.0", tk.END).strip()
    if not raw_text:
        messagebox.showwarning("Warning", "No text provided.")
        return

    # Example profile dictionary if you don't have profiles.py:
    profile = {
        "typing_delay_range": (0.01, 0.02),
        "typo_probability": 0.05,
        "typo_correction_delay_range": (0.005, 0.01),
        "typo_retype_delay_range": (0.05, 0.1)
    }

    is_typing = True
    status_label.config(text="Typing started...")

    # Start typing in a background thread
    typing_thread = typer.start_typing_thread(
        text=raw_text,
        profile=profile,
        on_finished=on_typing_finished,
        on_progress_update=on_progress_update
    )

def stop_typing():
    """Request to stop typing."""
    typer.request_stop()
    status_label.config(text="Stop requested...")

# -------------------- SCHEDULING --------------------
def open_schedule_popup():
    """Open a small window for scheduling options."""
    sched_win = tk.Toplevel(root)
    sched_win.title("Schedule Typing")
    sched_win.geometry("300x200")

    tk.Label(sched_win, text="Schedule Options:").pack(pady=5)

    # 1) Schedule after X seconds
    def schedule_in_seconds():
        try:
            secs = int(sec_entry.get())
        except ValueError:
            secs = 5
        scheduler.schedule_typing_in_delay(secs, start_typing)
        sched_win.destroy()
        status_label.config(text=f"Typing scheduled in {secs} seconds...")

    sec_entry = tk.Entry(sched_win)
    sec_entry.insert(0, "5")  # Default
    sec_entry.pack()
    ttk.Button(sched_win, text="Schedule in Seconds", command=schedule_in_seconds).pack(pady=2)

    # 2) Schedule after X minutes
    def schedule_in_mins():
        try:
            mins = int(min_entry.get())
        except ValueError:
            mins = 1
        scheduler.schedule_typing_in_minutes(mins, start_typing)
        sched_win.destroy()
        status_label.config(text=f"Typing scheduled in {mins} minutes...")

    min_entry = tk.Entry(sched_win)
    min_entry.insert(0, "1")
    min_entry.pack()
    ttk.Button(sched_win, text="Schedule in Minutes", command=schedule_in_mins).pack(pady=2)

    # 3) Schedule at HH:MM (24-hour format)
    def schedule_specific_time():
        time_str = time_entry.get().strip()
        if not time_str:
            time_str = "12:00"  # Default fallback
        scheduler.schedule_typing_at_specific_time(time_str, start_typing)
        sched_win.destroy()
        status_label.config(text=f"Typing scheduled at {time_str}...")

    time_entry = tk.Entry(sched_win)
    time_entry.insert(0, "12:00")
    time_entry.pack()
    ttk.Button(sched_win, text="Schedule at Time", command=schedule_specific_time).pack(pady=2)

# -------------------- WPM GRAPH WINDOW --------------------
graph_window = None

def show_wpm_graph():
    """Open a separate window to display a line graph for WPM tracking."""
    global graph_window
    if graph_window is not None:
        graph_window.destroy()

    graph_window = tk.Toplevel(root)
    graph_window.title("Live WPM Graph")
    graph_window.geometry("600x400")

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.set_title("Real-Time WPM Tracking")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("WPM")

    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Example static data for demonstration
    def update_graph():
        ax.cla()
        ax.set_title("Real-Time WPM Tracking")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("WPM")

        times = [0, 1, 2, 3, 4, 5]
        wpms = [20, 25, 30, 40, 42, 50]
        ax.plot(times, wpms, marker='o', color='cyan')

        canvas.draw()
        graph_window.after(1000, update_graph)

    update_graph()

# -------------------- CONTROL BUTTONS --------------------
control_frame = ttk.Frame(root)
control_frame.pack(pady=5)

start_button = ttk.Button(control_frame, text="Start Typing", command=start_typing)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = ttk.Button(control_frame, text="Stop Typing", command=stop_typing)
stop_button.pack(side=tk.LEFT, padx=5)

schedule_button = ttk.Button(control_frame, text="Schedule", command=open_schedule_popup)
schedule_button.pack(side=tk.LEFT, padx=5)

graph_button = ttk.Button(control_frame, text="Show WPM Graph", command=show_wpm_graph)
graph_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
