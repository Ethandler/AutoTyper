# modules/profiles.py

import json
import os

PROFILE_DIR = "data/profiles"

def load_profile(profile_name):
    """
    Load a profile (JSON) from data/profiles/ folder.
    Example: load_profile("default.json")
    Returns a dict with typing settings.
    """
    profile_path = os.path.join(PROFILE_DIR, profile_name)
    if not os.path.isfile(profile_path):
        # Return a default profile if none found
        return default_profile()

    with open(profile_path, 'r') as f:
        data = json.load(f)
    return data

def save_profile(profile_name, profile_data):
    """
    Save a profile dict to data/profiles/ as JSON.
    """
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)

    profile_path = os.path.join(PROFILE_DIR, profile_name)
    with open(profile_path, 'w') as f:
        json.dump(profile_data, f, indent=2)

def default_profile():
    """
    Return a default profile with typical typing settings.
    """
    return {
        "typing_delay_range": [0.004, 0.018],
        "typo_probability": 0.03,
        "typo_correction_delay_range": [0.004, 0.010],
        "typo_retype_delay_range": [0.047, 0.098]
    }
