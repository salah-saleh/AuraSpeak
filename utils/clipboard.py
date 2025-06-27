import pyperclip             # For copying text to the system clipboard

def copy_to_clipboard(text):
    """
    Copy the given text to the system clipboard.
    """
    pyperclip.copy(text) 