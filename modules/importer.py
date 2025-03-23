"""
modules/importer.py
Import text from .txt files or export typed content to .txt.
"""

def import_from_txt(file_path):
    """Return the contents of a .txt file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def export_to_txt(file_path, text):
    """Save 'text' to a .txt file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)
