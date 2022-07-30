import PySimpleGUI as sg

layout = [[sg.Button('Save')]]
window = sg.Window('Window Title', 
                   layout,
                   default_element_size=(12, 1),
                   resizable=True)  # this is the change

while True:
    event, values = window.read()
    if event == 'Save':
        print('clicked save')

    if event == sg.WIN_MAXIMIZED:  # I just made this up, and it does not work. :)
        window.maximize()

    if event == sg.WIN_CLOSED:
        break
