import PySimpleGUI as sg
import second_page

sg.theme_background_color("#DAE3F0")
font = ("Arial", 40)

first_column = [[sg.Text("WELCOME!",text_color="#2A325A",background_color="#DAE3F0",pad=((0,0),(0,200)),expand_x=True,justification="c")],
              [sg.Text("Choose the best algo to crypt / decrypt your file!",pad=((0,0),(0,100)),font=100,text_color="#2A325A",background_color="#DAE3F0")],
              [sg.Push(background_color="#DAE3F0"),sg.Button("LET'S GET STARTED"),sg.Push(background_color="#DAE3F0")]
              ]

image = [[sg.Image(filename="welcome page.png")]]

layout = [
    [sg.Column(first_column),
    sg.Column(image,size=(700,600))]
]


window1 = sg.Window("Application name", layout)

while True:
    event, values = window1.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == "LET'S GET STARTED":
        window1.close()
        second_page.main_window()
    window1.close()
