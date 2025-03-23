"""
modules/shortcuts.py
Register global or local hotkeys using the 'keyboard' library.
Requires: pip install keyboard
"""

import keyboard

def register_hotkeys(start_callback, stop_callback):
    """
    Register global hotkeys for controlling the typing process.
    Example:
      - Ctrl+Alt+S => Start
      - Ctrl+Alt+X => Stop
    """
    keyboard.add_hotkey('ctrl+alt+s', lambda: start_callback())
    keyboard.add_hotkey('ctrl+alt+x', lambda: stop_callback())

def unregister_hotkeys():
    """Unregister all previously added hotkeys."""
    keyboard.unhook_all_hotkeys()
