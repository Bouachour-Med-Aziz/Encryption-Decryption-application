import json
import os
import io
import numpy as np
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
check_num=0
state=False
pathset=os.path.expanduser('~/Documents/settingfile.json')
checkboxs=['-1-','-2-','-3-','-4-','-5-','-6-']
theta = np.linspace(0, 2 * np.pi, 100)
x = 16 * ( np.sin(theta) ** 3 )
y = 13 * np.cos(theta) - 5* np.cos(2*theta) - 2 * np.cos(3*theta) - np.cos(4*theta)
year = [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010]
unemployment_rate = [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
dict_default = {"setting":{"1":'15',"2":"Calibri","3":"LightGrey1"}}
def create_bar_graph(year, unemployment_rate):
    plt.figure(figsize =(5, 4))
    plt.bar(year, unemployment_rate, color='red', width=0.4)
    plt.title('Unemployment Rate Vs Year', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Unemployment Rate', fontsize=14)
    return plt.gcf()
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def button_text(p):
    if p==False:
        return 'Select all algorithms'
    return 'Deselect all algorithms'
def plot_draw():
    fig =plt.figure(figsize=(5,4))
    fig.add_subplot(111).plot(x,y)
    figure_canvas_agg = FigureCanvasTkAgg(fig,window1['-canvas1-'].TKCanvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()

def setting_create(y):
    sg.set_options(font=(y[1],y[0]))
    sg.theme(y[2])
    set_layout=[[sg.T('SETTING')],
                [sg.T('Font Size:'),sg.Input(s=2,default_text=y[0],key='-fontsize-'),sg.Column([[sg.Button('▲', size=(1, 1), font='Any 7', border_width=0, button_color=(sg.theme_text_color(), sg.theme_background_color()), key='-UP-')],
            [sg.Button('▼', size=(1, 1), font='Any 7', border_width=0, button_color=(sg.theme_text_color(), sg.theme_background_color()), key='-DOWN-')]])],
                [sg.T('Font Family:'),sg.Combo(["Arial", "Baskerville", "Calibri", "Cambria", "Cambria", "Courier New","Georgia", "Goudy Old Style", "Microsoft Sans Serif", "Verdana"], default_value=y[1], key='-FONTFAMILY-')],
                [sg.Text("Theme:"),sg.Combo(["Black", "BlueMono", "BrightColors", "Dark", "DarkBlack", "GrayGrayGray","LightBlue", "SystemDefaultForReal", "Purple", "SystemDefault"], default_value=y[2], key='-THEME-')],
                [sg.Button("Save Current Settings", s=20),sg.Button('Cancel',key='-cancel-',size=10,button_color='red'),sg.Button('Confirme',key='-confirme-',size=10,button_color='green')]]
    return sg.Window('Settings Window',set_layout,modal=True)

def setting_window1(x):
    z=x[:]
    window2 =setting_create(x)
    while True:
        event, values = window2.read()
        if event ==sg.WINDOW_CLOSED or event=='-cancel-':
            z=x[:]
            break
        counter = int(values['-fontsize-'])
        if event == '-UP-':
            counter+=1
        else:
            if event=='-DOWN-':
                counter-=1
                if counter<10:
                    counter=10
        window2['-fontsize-'].update(counter)
        if event == "Save Current Settings":
            if z[0]==values['-fontsize-'] and z[1]==values['-FONTFAMILY-'] and z[2]==values['-THEME-']:
                sg.popup_no_titlebar("Setting already exists")
            else:
                z=[values['-fontsize-'],values['-FONTFAMILY-'],values['-THEME-']]
                sg.popup_no_titlebar('Setting saved')
                window2.close()
                window2 =setting_create(z)
        if event == '-confirme-':
            break
    window2.close()
    return z
def main_window(w):
    sg.set_options(font=(w[1],w[0]))
    sg.theme(w[2])
    menu_def=[['File',['Save','Save as','Copy key','---','Exit']],
          ['Settings',['Views']],
          ['Credits',['About...']],
          ['Help',['About..']]]

    frame1=[[sg.Text('Input File:',justification='r'),sg.Push(),sg.Input(key='-In-'),sg.FilesBrowse(file_types=(("Word Files", "*.docx*")),)],
     [sg.Text('Output Folder:',justification='r'),sg.Input(key='-out-'),sg.FolderBrowse()]]
    frame2=[[sg.Radio("Encryption",'Gp1',key='-choix1-'),sg.Radio("Decryption",'Gp1',key='-choix2-')]]
    subframe1=[[sg.Checkbox('Algo 1',key='-1-',enable_events=True)],
           [sg.Checkbox('Algo 2',key='-2-',enable_events=True)],
           [sg.Checkbox('Algo 3',key='-3-',enable_events=True)]]
    subframe2=[[sg.Checkbox('Algo 1',key='-4-',enable_events=True)],
           [sg.Checkbox('Algo 2',key='-5-',enable_events=True)],
           [sg.Checkbox('Algo 3',key='-6-',enable_events=True)]]
    frame3=[[sg.Button('Select all algorithms',key='-all-',s=(19,1))],
        [sg.Frame('Symmetric algorithms',subframe1,border_width=0)],
        [sg.Frame('Asymmetric algorithms',subframe2,border_width=0)]]
    frame4=[[sg.Input()]]
    frame5=[[sg.Input()]]
    frame6=[[sg.Input()]]
    mini_column=[[sg.Frame('Password',frame4)],
                 [sg.Frame('Public key',frame5)],
                 [sg.Frame('Private key',frame6)]]
    col1=[
      [sg.Frame('Desired File',frame1)],
      [sg.Multiline(size=(40,10),visible=False,justification='l',key='-inputs-'),sg.Push(),sg.Button('Multiple Files',key='-trigger-')],
      [sg.Frame('Operations',frame2)],
      [sg.Column([[sg.Frame('Available Algorithms',frame3)]]),sg.VSeparator(),sg.Column(mini_column)],
     [sg.B('Display Word File'),sg.B('Reset',key='-reset-'),sg.Push(),sg.B('Exit',key='-exit-',size=10,button_color='red'),sg.B('Run',key='-run-',size=10,button_color='green')]]
    layout =[[sg.Menu(menu_def,key='-menu-')],
         [sg.Column(col1),sg.VSeparator(),sg.Column([[sg.Canvas(key='-canvas1-',size=(50,50))],
                                                     [sg.Canvas(key='-canvas2-',size=(50,50))]])]]
    return sg.Window('Time-Out',layout,finalize=True).finalize()

def setting_checkup():
    if os.path.isfile(pathset) and os.access(pathset,os.R_OK):
        print ("File exists and is readable")
       
    else:
        print ("Either file is missing or is not readable, creating file...")
        with io.open(os.path.join(os.path.expanduser('~/Documents'),'settingfile.json'),'w') as f:
            f.write(json.dumps(dict_default))
    with open(pathset, 'r') as f:
        data=json.load(f)
    return list(data["setting"].values())
# fname='settingfile'
default=setting_checkup()
# print(default)
window1 = main_window(default)
window1.maximize()
plot_draw()
draw_figure(window1['-canvas2-'].TKCanvas, create_bar_graph(year, unemployment_rate))
while True:
    event, values=window1.read()
    if event == sg.WIN_CLOSED or event =='-exit-' :
        break
    if event =='-all-':
        state= not state
        for i in checkboxs:
                window1[i].update(state)
        window1['-all-'].update(button_text(state))
    if event in checkboxs:
        i=0
        while i <=len(checkboxs)-1:
            if values[checkboxs[i]]==True:
                break
            i+=1
        if i> len(checkboxs)-1:
            check_num=0
        else:
            check_num=1
        if check_num==1:
            state=True
        else: 
            if check_num==0:
                state=False  
        window1['-all-'].update(button_text(state))        
    if event == 'About..':
        sg.popup('This project have as purpose to help you to choose the best algorithm to encrypt/decrypt your file. We provide different types of algorithms which you can visuale in a graphic curve.',title='Help')
    if event == 'About...':
        sg.popup('Version : 1.0", "PySimpleGUI Version :', sg.version, 'This project is made by the efforts of :',  "* Moetez Bouhlel", "* Firas Necib", "* Mohamed Aziz Bouachour",
                     title='About the application')
    if event == '-reset-':
        window1['-choix1-'].update(False)
        window1['-choix2-'].update(False)
        state=False
        for i in checkboxs:
                window1[i].update(state)
        window1['-all-'].update(button_text(state))
    if event == '-trigger-':
        window1['-inputs-'].update(visible=True)
        window1['-trigger-'].update(visible=False)
    if event == 'Views':
        prev_default=default[:]
        default= setting_window1(default)
        if prev_default != default:
            with open(pathset, 'r') as f:
                data=json.load(f)
            with open(pathset, 'w') as f:
                data["setting"]["1"]=default[0]
                data["setting"]["2"]=default[1]
                data["setting"]["3"]=default[2]
                json.dump(data, f)
            window1.close()
            window1 = main_window(default)
            plot_draw()
            draw_figure(window1['-canvas2-'].TKCanvas, create_bar_graph(year, unemployment_rate))
            
window1.close()