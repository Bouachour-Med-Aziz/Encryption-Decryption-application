import zipfile,re
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import timeit
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from pathlib import Path
import json
import os
import io
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
check_num=0
state=False
pathset=os.path.expanduser('~/Documents/settingfile.json')

checkboxs=['-1-','-2-','-3-','-4-','-5-','-6-','-7-','-8-','-9-','-10-','-11-','-12-']
available=['TripleDES','Camellia','SM4','AES','CASTS','SEED']
dict_default = {"setting":{"1":'15',"2":"Calibri","3":"LightGrey1"}}
def word_reader(name):
    docx=zipfile.ZipFile(name)
    content=docx.read('word/document.xml').decode('utf-8')
    cleaned = re.sub('<(.|\n)*?>','',content)
    return cleaned



def txt_reader(name):
    if Path(name).is_file():
            try:
                with open(name, "rt", encoding='utf-8') as f:
                    text = f.read()
            except Exception as e:
                print("Error: ", e)
    return text

def create_bar_graph(year, unemployment_rate):
    plt.figure(figsize =(5, 4))
    var=plt.bar(year, unemployment_rate, color='red', width=0.4)
    plt.title('Time Vs Algorithms', fontsize=16)
    return (plt.gcf(), var,plt)
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure[0], canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()
    return figure_canvas_agg

def button_text(p):
    if p==False:
        return 'Select all algorithms'
    return 'Deselect all algorithms'
def plot_draw(z=[],n=[]):
    fig =plt.figure(figsize=(5,4))
    fig.add_subplot(111).plot(z,n)
    return fig
def plot_draw2(fig,canvas):
    figure_canvas_agg = FigureCanvasTkAgg(fig,canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()
    return figure_canvas_agg
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

    frame1=[[sg.Text('Input File:',justification='r'),sg.Push(),sg.Input(key='-In-'),sg.FilesBrowse(file_types=(("Text File","*.txt*"),("Word Files", "*.docx*"),))],
     [sg.Text('Output Folder:',justification='r'),sg.Input(key='-out-'),sg.FolderBrowse()]]
    frame2=[[sg.Radio("Encryption",'Gp1',key='-choix1-',default=True),sg.Radio("Decryption",'Gp1',key='-choix2-')]]
    subframe1=[[sg.Checkbox('TripleDES',key='-1-',enable_events=True),sg.Checkbox('AES',key='-4-',enable_events=True)],
           [sg.Checkbox('Camellia',key='-2-',enable_events=True),sg.Checkbox('CASTS',key='-5-',enable_events=True)],
           [sg.Checkbox('SM4',key='-3-',enable_events=True),sg.Checkbox('SEED',key='-6-',enable_events=True)]]
    subframe2=[[sg.Checkbox('Algo 1',key='-7-',enable_events=True),sg.Checkbox('Algo 1',key='-10-',enable_events=True)],
           [sg.Checkbox('Algo 2',key='-8-',enable_events=True),sg.Checkbox('Algo 1',key='-11-',enable_events=True)],
           [sg.Checkbox('Algo 3',key='-9-',enable_events=True),sg.Checkbox('Algo 1',key='-12-',enable_events=True)]]
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
      [sg.Multiline(size=(30,5),visible=False,justification='l',key='-inputs-'),sg.Push(),sg.Button('Multiple Files',key='-trigger-')],
      [sg.Frame('Operations',frame2)],
      [sg.Column([[sg.Frame('Available Algorithms',frame3)]]),sg.VSeparator(),sg.Column(mini_column)],
     [sg.B('Display File',key='-display-'),sg.B('Reset',key='-reset-'),sg.Push(),sg.B('Exit',key='-exit-',size=10,button_color='red'),sg.B('Run',key='-run-',size=10,button_color='green')]]
    layout =[[sg.Menu(menu_def,key='-menu-')],
         [sg.Column(col1),sg.VSeparator(),sg.Column([[sg.Canvas(key='-canvas1-',size=(60,60),pad=10)],
                                                     [sg.Canvas(key='-canvas2-',size=(60,60),pad=10)]])]]
    return sg.Window('Time-Out',layout,finalize=True)

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
 
def encryption(alg):
    filename=values['-In-']
    if filename.split(".")[-1]=="txt":
        txt=txt_reader(filename)
    elif filename.split(".")[-1]=="docx":
        txt=word_reader(filename)
    if alg in range(6):
        x=16-len(txt)%16
        if len(txt)%16 != 0 :
            for i in range(x):
                txt = txt + ' '
    
    txt = txt.encode()
    match alg :
        case 0:
            key = os.urandom(16)
            iv = os.urandom(8)
            cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            ct0 = encryptor.update(txt) + encryptor.finalize()
            t0=timeit.timeit(stmt="ct0",globals=locals())
            results.append(t0)
            # decryptor = cipher.decryptor()
            # decryptor.update(ct) + decryptor.finalize()
        case 1:
            key = os.urandom(32)
            iv = os.urandom(16)
            cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            ct1 = encryptor.update(txt) + encryptor.finalize()
            t1=timeit.timeit(stmt="ct1",globals=locals())
            results.append(t1)
            # decryptor = cipher.decryptor()
            # decryptor.update(ct) + decryptor.finalize()
        case 2:
            key = os.urandom(16)
            iv = os.urandom(16)
            algorithm = algorithms.SM4(key)
            cipher = Cipher(algorithm, modes.CBC(iv))
            encryptor = cipher.encryptor()
            ct2 = encryptor.update(txt)
            t2=timeit.timeit(stmt="ct2",globals=locals())
            results.append(t2)
            # decryptor = cipher.decryptor()
            # decryptor.update(ct) + decryptor.finalize()
        case 3:
            key = os.urandom(32)
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            ct3 = encryptor.update(txt) + encryptor.finalize()
            t3=timeit.timeit(stmt="ct3",globals=locals())
            results.append(t3)
            # decryptor = cipher.decryptor()
            # decryptor.update(ct) + decryptor.finalize()
        case 4:
            key = os.urandom(16)
            iv = os.urandom(8)
            cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            ct4= encryptor.update(txt) + encryptor.finalize()
            t4=timeit.timeit(stmt="ct4",globals=locals())
            results.append(t4)
            # decryptor = cipher.decryptor()
            # decryptor.update(ct) + decryptor.finalize()
        case 5:
            key = os.urandom(16)
            iv = os.urandom(16)
            cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            ct5 = encryptor.update(txt) + encryptor.finalize()
            t5=timeit.timeit(stmt="ct5",globals=locals())
            results.append(t5)
            # decryptor = cipher.decryptor()
            # decryptor.update(ct) + decryptor.finalize()
        case 6:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,)
            public_key = private_key.public_key()         
            ciphertext = public_key.encrypt(txt,padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None))
            
default=setting_checkup()
window1 = main_window(default)
Fig22=plot_draw()
akg=plot_draw2(Fig22,window1['-canvas1-'].TKCanvas)
Fig23=create_bar_graph([],[])
akg2=draw_figure(window1['-canvas2-'].TKCanvas,Fig23)
while True:
    event, values=window1.read()
    if event == sg.WIN_CLOSED or event =='-exit-' or event == 'Exit':
        break
    if event =='Save as':
        sg.popup()
    if event == '-display-':
        os.startfile(values['-In-'])
        
    
    if event == '-run-' and values['-choix1-']:
        current=[]
        results=[]
        if values[checkboxs[0]] == True :
            current.append(available[0])
            encryption(0)
        if values[checkboxs[1]] == True :
            current.append(available[1])
            encryption(1)
        if values[checkboxs[2]] == True :
            current.append(available[2])
            encryption(2)
        if values[checkboxs[3]] == True :
            current.append(available[3])
            encryption(3)
        if values[checkboxs[4]] == True :
            current.append(available[4])
            encryption(4)
        if values[checkboxs[5]] == True :
            current.append(available[5])
            encryption(5)
        if values[checkboxs[6]] == True :
            current.append(available[6])
            encryption(6)
    
        # axes=Fig22.axes
        # axes[0].plot([0,2,4],[1,3,5])
        # akg.draw()
        # akg.get_tk_widget().pack()
        Fig23[2].cla()
        Fig23[2].bar(current,results, color='red', width=0.4)
        plt.title('Time Vs Algorithms', fontsize=16)
        Fig23[2].xticks(current)
        Fig23[2].yticks(results)
        akg2.draw()
        akg2.get_tk_widget().pack()
        sg.popup_no_buttons(f"Best Time:{min(results)} by {current[results.index(min(results))]}\nWorst Time:{max(results)} by {current[results.index(max(results))]}\nAverage Time: {sum(results)/len(results)}",title="")
        
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
        window1['-choix1-'].update(True)
        window1['-choix2-'].update(False)
        window1['-In-'].update('')
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
            Fig22=plot_draw()
            akg=plot_draw2(Fig22,window1['-canvas1-'].TKCanvas)
            Fig23=create_bar_graph([],[])
            akg2=draw_figure(window1['-canvas2-'].TKCanvas,Fig23)
            
window1.close()