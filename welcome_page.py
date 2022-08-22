import PySimpleGUI as sg
from matplotlib.pyplot import margins
from numpy import expand_dims
import second_page

sg.theme_background_color("#DAE3F0")
sg.set_options(font=("Calibri",10))

first_column = [[sg.Text("\nWELCOME!",s=(10,4),background_color="#DAE3F0")],
              [sg.Text("Choose the best algorithm to \n crypt/decrypt your file !",s=(25,4),background_color="#DAE3F0",text_color="#15191D")],
              [sg.Button("LET'S GET STARTED", s=20)]
              ]

image = [[sg.Image(filename="welcome page.png",expand_x=True, expand_y=True)]]

layout = [[
    sg.Column(first_column,background_color="#DAE3F0",expand_x=True, expand_y=True,pad=(0,0))
    ,sg.VerticalSeparator(),sg.Column(image)
    ]
]

window1 = sg.Window("Application name", layout, resizable=True).finalize()
window1.Maximize()


while True:
    event, values = window1.read()
    if event == sg.WINDOW_CLOSED:
        break
    # if event == "Minimize":
    #     window1.Hide()
    if event == "LET'S GET STARTED":
        window1.close()
        second_page.main_window()
    window1.close()

