from re import fullmatch
from turtle import color
import PySimpleGUI as sg
from numpy import False_, choose
import os

# ------ Menu Definition ------ #

menu_def1 = [["File", ["Command1", "Command2"]],
             ["Settings", ["View"]],["Credit", ["About.."]],["Help"],
             ]
menu_def = ['&File', ['&New File', '&Open...', 'Open &Module', '---', '!&Recent Files', 'C&lose']
            ], ['&Save', ['&Save File', 'Save &As', 'Save &Copy']], ['&Edit', ['&Cut', '&Copy', '&Paste']]


def is_valid_path(filepath):
    if os.path.isfile(filepath) and (filepath != ""):
        return True
    sg.popup_error("Filepath not correct")
    return False


def display_word_file(word_file_path):
    os.startfile(word_file_path)


def main_window():
    #  ------ GUI Definition ------- #
    layout = [[sg.Menu(menu_def1,key="menu", background_color='lightsteelblue', text_color='navy', disabled_text_color='yellow', pad=(10, 10))],
              [sg.Text("Input File:",s=15,justification="r",text_color="#cedef0"), sg.Input(key="-IN-"),
               sg.FileBrowse(file_types=(("Word Files", "*.docx*"),))],
              [sg.Text("Output Folder:",s=15,justification="r"), sg.Input(
                  key="-OUT-"), sg.FolderBrowse()],
              [sg.Text("Conversion type:"), sg.Radio("Encryption", "Grp1", key="choice1"),
               sg.Radio("Decryption", "Grp1", key="choice2")],
              [sg.Text("Choose at least one algorithm:",s=30,justification="r")],
              [sg.Button("Select all algorithms"),
               sg.Button("Deselect all algorithms")],
              [sg.Text("Symmetric algorithms:")],
              [[sg.Checkbox("Algo 1", key="checkbox1")], [sg.Checkbox("Algo 2", key="checkbox2")],
               [sg.Checkbox("Algo 3", key="checkbox3")]],
              [sg.Text("Asymmetric algorithms:")],
              [[sg.Checkbox("Algo 1", key="checkbox4")], [sg.Checkbox("Algo 2", key="checkbox5")],
               [sg.Checkbox("Algo 3", key="checkbox6")]],
              [sg.Exit(s=10,button_color="red" ), sg.Button("Display Word File"),
               sg.Button("Reset"), sg.Button("Run",s=8,button_color="green")],
              [sg.HorizontalSeparator()],
              ]

    window = sg.Window("Application name", layout, resizable=True).Finalize()
    window.Maximize()
    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        if event == "Display Word File":
            if is_valid_path(values["-IN-"]):
                display_word_file(values["-IN-"])
        if event == "Reset":
            window.Element("choice1").update(value=False)
            window.Element("choice2").update(value=False)
            window.Element("-IN-").update(value="")
            window.Element("-OUT-").update(value="")

            for x in "123456":
                window["checkbox"+x].update(value=False)

        if event == "Select all algorithms":
            for y in "123456":
                window["checkbox"+y].update(value=True)

        if event == "Deselect all algorithms":
            for y in "123456":
                window["checkbox"+y].update(value=False)
        
        if event == "Command1":
            print("Command1")
        if event == "About..":
            sg.popup('This project is ...')

    window.close()


if __name__ == "__main__":
    main_window()
    sg.set_options(font="Arial")