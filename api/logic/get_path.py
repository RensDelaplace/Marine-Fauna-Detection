# wxPython GUI toolkit for wx, maybe we can use PyQt5 instead
import wx
import os
# currently only used in home.py


# https://stackoverflow.com/questions/25087169/python-easygui-cant-select-file
def get_path():
    """
    Function Description:
        This function opens a file dialog window using wxPython library, allowing the user to select one or multiple files.
        It specifically targets .mp4 video files. If the user selects file(s), it returns the path(s) of the selected file(s).
        If no file is selected or the dialog is canceled, it returns None.

    Parameters:
        None

    Returns:
        path (str or list): Path of the selected file(s) if any, otherwise None.

    Usage:
        Call this function to prompt the user to select one or multiple .mp4 video files using a file dialog window.

    Dependencies:
        This function requires the wxPython library to be installed.
    """
    app = wx.App()
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
    dialog = wx.FileDialog(None, "Open", wildcard="Videos (*.mp4)|*.mp4|Images (*.png;*.jpg)|*.png;*.jpg", style=style)


    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPaths()
    else:
        path = None
    dialog.Destroy()
    return path


def get_directory():
    """
    Returns:
        path (str): Path of the selected directory if any, otherwise None.

    Usage:
        Call this function to prompt the user to select a directory using a directory dialog window.
    """
    app = wx.App()
    dialog = wx.DirDialog(None, "Choose a directory", style=wx.DD_DEFAULT_STYLE)

    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(script_dir))
def get_model_directory():
    """
    Returns:
        path (str): Path of the selected directory if any, otherwise None.

    Usage:
        Call this function to prompt the user to select a directory using a directory dialog window.
    """
    app = wx.App()

    default_dir = os.path.join(project_dir, "models")  # Replace this with the path to the directory you want to use
    dialog = wx.DirDialog(None, "Choose a directory", defaultPath=default_dir, style=wx.DD_DEFAULT_STYLE)

    path = None
    while path is None:
        if dialog.ShowModal() == wx.ID_OK:
            selected_path = dialog.GetPath()
            path = selected_path

            # if os.path.commonpath([selected_path, default_dir]) == default_dir:
            #     path = selected_path
            # else:
            #     wx.MessageBox('Please select a directory within the allowed directory', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            break

    dialog.Destroy()
    return path
