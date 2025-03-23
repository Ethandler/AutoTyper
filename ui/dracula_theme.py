"""
ui/dracula_theme.py
Applies a Dracula-like color scheme to your Tkinter widgets.
"""

import tkinter as tk
from tkinter import ttk

def apply_dracula_theme(root):
    # Dracula palette
    BG_COLOR = "#282A36"
    FG_COLOR = "#F8F8F2"
    ACCENT_COLOR = "#6272A4"
    BTN_ACTIVE = "#FF79C6"
    ENTRY_BG = "#44475A"

    style = ttk.Style(root)
    style.theme_use('clam')

    # Root background
    root.configure(bg=BG_COLOR)

    # Button styling
    style.configure(
        'TButton',
        background=ACCENT_COLOR,
        foreground=FG_COLOR,
        font=('Segoe UI', 11),
        padding=6,
        relief='flat'
    )
    style.map('TButton', background=[('active', BTN_ACTIVE)])

    # Label styling
    style.configure(
        'TLabel',
        background=BG_COLOR,
        foreground=FG_COLOR,
        font=('Segoe UI', 11)
    )

    # Entry styling
    style.configure(
        'TEntry',
        fieldbackground=ENTRY_BG,
        foreground=FG_COLOR,
        font=('Segoe UI', 11)
    )

    # Frame styling
    style.configure('TFrame', background=BG_COLOR)

    # Progressbar styling
    style.configure(
        'Horizontal.TProgressbar',
        troughcolor=ENTRY_BG,
        background=BTN_ACTIVE,
        thickness=12
    )
