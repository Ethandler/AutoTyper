"""
modules/typer.py
Core typing logic with:
- 5-second delay before typing starts
- Optionally introduce typos based on profile
- Tracks WPM and mistakes
"""

import pyautogui
import time
import random
import threading

_stop_requested = False

def request_stop():
    """Request to stop typing gracefully."""
    global _stop_requested
    _stop_requested = True

def start_typing_thread(text, profile, on_finished, on_progress_update):
    """
    Launch the typing process in a background thread.
    Returns the Thread object if needed.
    """
    thread = threading.Thread(
        target=simulate_typing,
        args=(text, profile, on_finished, on_progress_update),
        daemon=True
    )
    thread.start()
    return thread

def simulate_typing(text, profile, on_finished, on_progress_update):
    """
    Simulate typing:
    1. 5-second delay before typing.
    2. Use profile settings for typing speed & typos.
    3. Update progress and call 'on_finished' with final WPM & mistakes.
    """
    global _stop_requested
    _stop_requested = False

    # 5-second delay
    time.sleep(5)

    # Unpack profile settings
    typing_delay_range = profile.get("typing_delay_range", (0.004, 0.018))
    typo_probability = profile.get("typo_probability", 0.03)
    correction_delay_range = profile.get("typo_correction_delay_range", (0.004, 0.010))
    retype_delay_range = profile.get("typo_retype_delay_range", (0.047, 0.098))

    total_chars = len(text)
    typed_chars = 0
    mistakes = 0

    start_time = time.time()

    for char in text:
        if _stop_requested:
            break

        # Possibly introduce a typo
        if char.strip() and random.random() < typo_probability:
            # Type a wrong char
            wrong_char = get_wrong_character(char)
            pyautogui.write(wrong_char)
            mistakes += 1
            time.sleep(random.uniform(*correction_delay_range))
            # Backspace
            pyautogui.press('backspace')
            time.sleep(random.uniform(*retype_delay_range))
            # Now type correct char
            pyautogui.write(char)
        else:
            pyautogui.write(char)

        typed_chars += 1

        # Update progress
        percentage = (typed_chars / total_chars) * 100
        on_progress_update(percentage)

        # Random delay between chars
        time.sleep(random.uniform(*typing_delay_range))

    elapsed_time = time.time() - start_time
    final_wpm = calculate_wpm(typed_chars, elapsed_time)
    on_finished(final_wpm, mistakes)

def get_wrong_character(correct_char):
    """Return a random incorrect character for simulating typos."""
    import string
    if correct_char.isalpha():
        letters = string.ascii_lowercase.replace(correct_char.lower(), '')
        return random.choice(letters)
    elif correct_char.isdigit():
        digits = string.digits.replace(correct_char, '')
        return random.choice(digits)
    else:
        return random.choice(string.punctuation)

def calculate_wpm(typed_chars, elapsed_time):
    """Calculate WPM (5 chars = 1 word)."""
    words_typed = typed_chars / 5.0
    minutes = elapsed_time / 60.0
    return round(words_typed / minutes, 2) if minutes > 0 else 0
