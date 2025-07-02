"""
tk.messagebox
-------------

This module provides a simple and convenient interface to the native
message box dialogues available in Tk 4.2 and newer. These dialogues are
useful for displaying information, warnings, errors, and asking various
types of questions to the user.

Developed by Fredrik Lundh, May 1997.
Refactored and improved for clarity and modern Python practices.

Usage:
------
Import the functions directly:
    from tkinter.messagebox import showinfo, showwarning, showerror, \
        askquestion, askokcancel, askyesno, askyesnocancel, askretrycancel

Then call them with a title and message:
    showinfo("Information", "This is an informational message.")
    result = askyesno("Confirmation", "Do you want to proceed?")

Options:
--------
All functions accept the following keyword arguments (all are optional and have
sensible default values):

- `default`: Specifies which button should be the default (e.g., 'ok', 'yes').
             Must be one of the reply codes (e.g., `messagebox.OK`, `messagebox.YES`).
- `icon`:    Determines the icon to display (e.g., 'info', 'warning', 'error', 'question').
             Typically set by the convenience functions, but can be overridden.
- `message`: The primary message text to display in the dialogue.
- `parent`:  Specifies the parent window for the dialogue, causing it to appear
             on top of the parent and blocking interaction with it.
- `title`:   The title text for the dialogue window's title bar.
- `type`:    Defines the set of buttons to display (e.g., 'ok', 'okcancel', 'yesno').
             Typically set by the convenience functions.

Reply Codes:
------------
The `ask*` functions return string constants representing the user's choice:

- `ABORT`
- `RETRY`
- ``
- `OK`
- `CANCEL`
- `YES`
- `NO`
"""

from tkinter.commondialog import Dialog

# Public API functions exposed by this module
__all__ = [
    "showinfo", "showwarning", "showerror",
    "askquestion", "askokcancel", "askyesno",
    "askyesnocancel", "askretrycancel"
]

# --- Constants for Icons, Types, and Replies ---

# Icons
# These strings correspond to the icons Tkinter can display in message boxes.
ERROR = "error"
INFO = "info"
QUESTION = "question"
WARNING = "warning"

# Types (Button Configurations)
# These strings define the button sets available for message boxes.
ABORTRETRYIGNORE = "abortretryignore"
OK = "ok"
OKCANCEL = "okcancel"
RETRYCANCEL = "retrycancel"
YESNO = "yesno"
YESNOCANCEL = "yesnocancel"

# Replies (Return Values)
# These strings represent the possible responses from the message box.
# Note: 'OK' is redefined here to be distinct from the 'OK' type above.
# This is a common pattern in Tkinter's messagebox module.
ABORT = "abort"
RETRY = "retry"
IGNORE = "ignore"
OK = "ok"  # User clicked OK
CANCEL = "cancel"
YES = "yes"
NO = "no"

# --- Message Box Class ---

class _MessageBox(Dialog):
    """
    Internal class representing a Tkinter message box.
    Inherits from tkinter.commondialog.Dialog and uses the 'tk_messageBox' command.
    Users should typically use the convenience functions rather than instantiating this directly.
    """
    command = "tk_messageBox"

# --- Convenience Functions ---

def _show(title: str | None = None, message: str | None = None,
          _icon: str | None = None, _type: str | None = None,
          **options) -> str | bool | None:
    """
    Internal helper function to display a message box.

    It handles the mapping of `title`, `message`, `_icon`, and `_type`
    to the `options` dictionary before calling the underlying Tkinter message box.
    It also normalizes the return value from Tkinter to a string constant.

    Args:
        title (str, optional): The title of the message box window. Defaults to None.
        message (str, optional): The message text to display. Defaults to None.
        _icon (str, optional): The icon type (e.g., "info", "warning"). Defaults to None.
        _type (str, optional): The button configuration (e.g., "ok", "yesno"). Defaults to None.
        **options: Additional keyword arguments passed directly to the Tkinter message box.

    Returns:
        str | bool | None: The user's response as a string constant (e.g., "yes", "no", "ok"),
                           a boolean for some types (True for YES/OK, False for NO/CANCEL),
                           or None for CANCEL in `askyesnocancel`.
    """
    if _icon and "icon" not in options:
        options["icon"] = _icon
    if _type and "type" not in options:
        options["type"] = _type
    if title:
        options["title"] = title
    if message:
        options["message"] = message

    res = _MessageBox(**options).show()

    # Normalize the return value from Tkinter.
    # Tkinter can return booleans, Tcl_Obj, or strings depending on the Tcl/Tk version.
    if isinstance(res, bool):
        # For yes/no types, Tcl sometimes returns a boolean.
        return YES if res else NO
    elif res is None:
        # If Tkinter returns None for a cancel, we preserve it for askyesnocancel.
        return None
    else:
        # Otherwise, convert to string and return the constant.
        return str(res)


def showinfo(title: str | None = None, message: str | None = None, **options) -> str:
    """
    Displays an informational message box.

    Args:
        title (str, optional): The title of the message box.
        message (str, optional): The message content.
        **options: Additional options for the message box (e.g., parent).

    Returns:
        str: Always returns `OK`.
    """
    return _show(title, message, INFO, OK, **options)


def showwarning(title: str | None = None, message: str | None = None, **options) -> str:
    """
    Displays a warning message box.

    Args:
        title (str, optional): The title of the message box.
        message (str, optional): The message content.
        **options: Additional options for the message box (e.g., parent).

    Returns:
        str: Always returns `OK`.
    """
    return _show(title, message, WARNING, OK, **options)


def showerror(title: str | None = None, message: str | None = None, **options) -> str:
    """
    Displays an error message box.

    Args:
        title (str, optional): The title of the message box.
        message (str, optional): The message content.
        **options: Additional options for the message box (e.g., parent).

    Returns:
        str: Always returns `OK`.
    """
    return _show(title, message, ERROR, OK, **options)


def askquestion(title: str | None = None, message: str | None = None, **options) -> str:
    """
    Asks a question, presenting 'Yes' and 'No' buttons.

    Args:
        title (str, optional): The title of the message box.
        message (str, optional): The question to ask.
        **options: Additional options for the message box (e.g., parent).

    Returns:
        str: Returns `YES` or `NO`.
    """
    return _show(title, message, QUESTION, YESNO, **options)


def askokcancel(title: str | None = None, message: str | None = None, **options) -> bool:
    """
    Asks for confirmation, presenting 'OK' and 'Cancel' buttons.

    Args:
        title (str, optional): The title of the message box.
        message (str, optional): The message asking for confirmation.
        **options: Additional options for the message box (e.g., parent).

    Returns:
        bool: Returns `True` if 'OK' is clicked, `False` if 'Cancel' is clicked.
    """
    s = _show(title, message, QUESTION, OKCANCEL, **options)
    return s == OK


def askyesno(title: str | None = None, message: str | None = None, **options) -> bool:
    """
    Asks a yes/no question.

    Args:
        title (str, optional): The title of the message box.
        message (str, optional): The question to ask.
        **options: Additional options for the message box (e.g., parent).

    Returns:
        bool: Returns `True` if 'Yes' is clicked, `False` if 'No' is clicked.
    """
    s = _show(title, message, QUESTION, YESNO, **options)
    return s == YES


def askyesnocancel(title: str | None = None, message: str | None = None, **options) -> bool | None:
    """
    Asks a yes/no/cancel question.

    Args:
        title (str, optional): The title of the message box.
        message (str, optional): The question to ask.
        **options: Additional options for the message box (e.g., parent).

    Returns:
        bool | None: Returns `True` for 'Yes', `False` for 'No', and `None` for 'Cancel'.
    """
    s = _show(title, message, QUESTION, YESNOCANCEL, **options)
    # The _show function already normalizes to string constants or None.
    if s == CANCEL:
        return None
    return s == YES


def askretrycancel(title: str | None = None, message: str | None = None, **options) -> bool:
    """
    Asks if an operation should be retried, presenting 'Retry' and 'Cancel' buttons.

    Args:
        title (str, optional): The title of the message box.
        message (str, optional): The message asking to retry.
        **options: Additional options for the message box (e.g., parent).

    Returns:
        bool: Returns `True` if 'Retry' is clicked, `False` if 'Cancel' is clicked.
    """
    s = _show(title, message, WARNING, RETRYCANCEL, **options)
    return s == RETRY

---
# Test Stuff
# This block demonstrates the usage of the message box functions.

if __name__ == "__main__":
    print("--- Tkinter Message Box Test ---")
    print("info:", showinfo("Spam", "Egg Information"))
    print("warning:", showwarning("Spam", "Egg Warning"))
    print("error:", showerror("Spam", "Egg Alert"))
    print("question:", askquestion("Spam", "Question?"))
    print("proceed (OK/Cancel):", askokcancel("Spam", "Proceed?"))
    print("got it (Yes/No):", askyesno("Spam", "Got it?"))
    print("want it (Yes/No/Cancel):", askyesnocancel("Spam", "Want it?"))
    print("try again (Retry/Cancel):", askretrycancel("Spam", "Try again?"))
    print("--- Test Complete ---")