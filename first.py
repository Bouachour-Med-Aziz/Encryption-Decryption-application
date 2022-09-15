from base64 import b64decode, b64encode
import zipfile,re
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import timeit
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding,rsa
from pathlib import Path
import json
import os
import io
import numpy as np
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
check_num=0
state=False
mode=False
pathset=os.path.expanduser('~/Documents/settingfile.json')
fichier=[]
time=[]
save={}
checkboxs=['-1-','-2-','-3-','-4-','-5-','-6-','-7-']
dict_default = {"setting":{"1":'15',"2":"Calibri","3":"LightGrey1"}}

def word_reader(name):
    docx=zipfile.ZipFile(name)
    content=docx.read('word/document.xml').decode('utf-8')
    cleaned = re.sub('<(.|\n)*?>','',content)
    return cleaned

def load_key(content):
    private_key = load_pem_private_key(content, None)
    return private_key

def save_pr_key(pr):
    how=pr.private_bytes(encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption())
    return how


def str_to_byte(ob):
    st=ob.encode('utf-8')
    st=b64decode(st)
    return st

def txt_reader(name):
    if Path(name).is_file():
            try:
                with open(name, "rt", encoding='utf-8') as f:
                    text = f.read()
            except Exception as e:
                print("Error: ", e)
    return text

def create_bar_graph(x, y):
    plt.figure(figsize =(5, 4))
    var=plt.bar(x, y, color='red', width=0.4)
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
                [sg.T('Font Family:'),sg.Combo(["Arial", "Baskerville", "Calibri", "Cambria", "Courier New","Georgia", "Goudy Old Style", "Microsoft Sans Serif", "Verdana"], default_value=y[1], key='-FONTFAMILY-')],
                [sg.Text("Theme:"),sg.Combo(["Black", "BlueMono", "BrightColors", "Dark", "DarkBlack", "GrayGrayGray","LightBlue", "SystemDefaultForReal", "Purple", "SystemDefault","LightGrey1"], default_value=y[2], key='-THEME-')],
                [sg.Button("Save Current Settings", s=20),sg.Button('Cancel',key='-cancel-',size=10,button_color='red'),sg.Button('Confirm',key='-confirme-',size=10,button_color='green')]]
    return sg.Window('Settings Window',set_layout,modal=True)

def setting_window1(x):
    z=x[:]
    window2 =setting_create(x)
    while True:
        event, values = window2.read()
        if event ==sg.WINDOW_CLOSED or event=='-cancel-' :
            z=x[:]
            break
        if event == '-confirme-':
            break
        counter = int(values['-fontsize-'])
        if event == '-UP-':
            counter+=1
            if counter>25:
                counter=25
        else:
            if event=='-DOWN-':
                counter-=1
                if counter<15:
                    counter=15
        window2['-fontsize-'].update(counter)
        if event == "Save Current Settings":
            if z[0]==values['-fontsize-'] and z[1]==values['-FONTFAMILY-'] and z[2]==values['-THEME-']:
                sg.popup_no_titlebar("Setting already exists")
            else:
                z=[values['-fontsize-'],values['-FONTFAMILY-'],values['-THEME-']]
                sg.popup_no_titlebar('Setting saved')
    window2.close()
    return z

def main_window(w):
    sg.set_options(font=(w[1],w[0]))
    sg.theme(w[2])
    menu_def=[['File',['Save','Save as','---','Exit']],
          ['Settings',['Views']],
          ['Credits',['About...']],
          ['Help',['About..']]]
    frame1=[[sg.Text('Input File:',justification='r'),sg.Push(),sg.Input(key='-In-'),sg.FileBrowse(file_types=(("Text File","*.txt*"),("Word Files", "*.docx*"),))],
     [sg.Text('Output Folder:',justification='r'),sg.Input(key='-out-'),sg.FolderBrowse()]]
    frame2=[[sg.Radio("Encryption",'Gp1',key='-choix1-',default=True,enable_events=True),sg.Radio("Decryption",'Gp1',key='-choix2-',enable_events=True)]]
    subframe1=[[sg.Checkbox('TripleDES',key='-1-',enable_events=True),sg.Checkbox('AES',key='-4-',enable_events=True)],
           [sg.Checkbox('Camellia',key='-2-',enable_events=True),sg.Checkbox('CAST5',key='-5-',enable_events=True)],
           [sg.Checkbox('SM4',key='-3-',enable_events=True),sg.Checkbox('SEED',key='-6-',enable_events=True)]]
    subframe2=[[sg.Checkbox('RSA',key='-7-',enable_events=True)]]
    frame3=[[sg.Button('Select all algorithms',key='-all-',s=(19,1))],
        [sg.Frame('Symmetric algorithms',subframe1,border_width=0)],
        [sg.Frame('Asymmetric algorithms',subframe2,border_width=0)]]
    frame4=[[sg.Input(key='-key-')]]
    frame5=[[sg.Input(key='-iv-')]]
    frame6=[[sg.Input(key='-pr-'),sg.FileBrowse(file_types=(("Text File","*.txt*"),))]]
    mini_column=[[sg.Frame('Key',frame4)],
                 [sg.Frame('Iv',frame5)],
                 [sg.Frame('Private key',frame6)]]
    col1=[
      [sg.Frame('Desired File',frame1)],
      [sg.pin(sg.Listbox(s=(70,5),key='-inputs-',values=[],visible=False,select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)),sg.Push(),sg.pin(sg.Column([[sg.FilesBrowse(file_types=(("Text File","*.txt*"),("Word Files", "*.docx*"),),key='-files-',button_text='ADD',target='-link-')],[sg.B('Delete',button_color='red',key='-delete-')],[sg.B('Multi Mode',key='-mode-')]],visible=False,key='-ad-')),sg.Input(key='-link-',visible=False,enable_events=True),sg.Button('Multiple Files',key='-trigger-')],
      [sg.Frame('Operations',frame2)],
      [sg.Column([[sg.Frame('Available Algorithms',frame3)]]),sg.VSeparator(),sg.Column(mini_column)],
     [sg.B('Display File',key='-display-'),sg.B('Reset',key='-reset-'),sg.Push(),sg.B('Exit',key='-exit-',size=10,button_color='red'),sg.B('Run',key='-run-',size=10,button_color='green')]]
    layout =[[sg.MenubarCustom(menu_def,key='-menu-',tearoff=False)],
         [sg.Column(col1),sg.VSeparator(),sg.Column([[sg.Canvas(key='-canvas1-',size=(60,60),pad=10)],
                                                     [sg.Canvas(key='-canvas2-',size=(60,60),pad=10)]])]]
    return sg.Window('Time-Out',layout,finalize=True,grab_anywhere=True)

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
 
def encryption(alg,condition):
    for j in list(save.keys()):
        d0={}
        filename=j
        if filename.split(".")[-1]=="txt":
            txt=txt_reader(filename)
            if alg ==6 and condition==False:
                pr_key=txt_reader(values['-pr-'])
                pr_key=str_to_byte(pr_key)
                pr_key=load_key(pr_key)
        elif filename.split(".")[-1]=="docx":
            txt=word_reader(filename)
        if condition ==True:
            if alg in range(6):
                x=16-len(txt)%16
                if len(txt)%16 != 0 :
                    for i in range(x):
                        txt = txt + ' '
            txt = txt.encode()
        if condition ==False:
            if alg in range(6):
                txt=txt.split("\n")[0]
            txt2=str_to_byte(txt)
        match alg :
            case 0:
                if condition ==True :
                    key = os.urandom(16)
                    iv = os.urandom(8)
                    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
                    encryptor = cipher.encryptor()
                    ct0 = encryptor.update(txt) + encryptor.finalize()
                    t0=timeit.repeat(stmt="ct0",repeat=10,number=1,globals=locals())
                    d0['TripleDES']=[b64encode(ct0).decode('utf-8'),t0,sum(t0)/len(t0),(b64encode(key).decode('utf-8'),b64encode(iv).decode('utf-8'))]
                if condition !=True:
                    cipher = Cipher(algorithms.TripleDES(str_to_byte(values['-key-'])), modes.CBC(str_to_byte(values['-iv-'])))
                    decryptor = cipher.decryptor()
                    w=decryptor.update(txt2) + decryptor.finalize()
                    t0=timeit.repeat(stmt="w",repeat=10,number=1,globals=locals())
                    d0['TripleDES']=[w,t0,sum(t0)/len(t0)]
            case 1:
                if condition ==True :
                    key = os.urandom(32)
                    iv = os.urandom(16)
                    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
                    encryptor = cipher.encryptor()
                    ct1 = encryptor.update(txt) + encryptor.finalize()
                    t1=timeit.repeat(stmt="ct1",repeat=10,number=1,globals=locals())
                    d0['Camellia']=[b64encode(ct1).decode('utf-8'),t1,sum(t1)/len(t1),(b64encode(key).decode('utf-8'),b64encode(iv).decode('utf-8'))]
                if condition !=True:
                    cipher = Cipher(algorithms.Camellia(str_to_byte(values['-key-'])), modes.CBC(str_to_byte(values['-iv-'])))
                    decryptor = cipher.decryptor()
                    w=decryptor.update(txt2) + decryptor.finalize()
                    t1=timeit.repeat(stmt="w",repeat=10,number=1,globals=locals())
                    d0['Camellia']=[w,t1,sum(t1)/len(t1)]
            case 2:
                if condition ==True :
                    key = os.urandom(16)
                    iv = os.urandom(16)
                    cipher = Cipher(algorithms.SM4(key), modes.CBC(iv))
                    encryptor = cipher.encryptor()
                    ct2 = encryptor.update(txt)
                    t2=timeit.repeat(stmt="ct2",repeat=10,number=1,globals=locals())
                    d0['SM4']=[b64encode(ct2).decode('utf-8'),t2,sum(t2)/len(t2),(b64encode(key).decode('utf-8'),b64encode(iv).decode('utf-8'))]
                if condition !=True:
                    cipher = Cipher(algorithms.SM4(str_to_byte(values['-key-'])), modes.CBC(str_to_byte(values['-iv-'])))
                    decryptor = cipher.decryptor()
                    w=decryptor.update(txt2) + decryptor.finalize()
                    t2=timeit.repeat(stmt="w",repeat=10,number=1,globals=locals())
                    d0['SM4']=[w,t2,sum(t2)/len(t2)]
            case 3:
                if condition ==True :
                    key = os.urandom(32)
                    iv = os.urandom(16)
                    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
                    encryptor = cipher.encryptor()
                    ct3 = encryptor.update(txt) + encryptor.finalize()
                    t3=timeit.repeat(stmt="ct3",repeat=10,number=1,globals=locals())
                    d0['AES']=[b64encode(ct3).decode('utf-8'),t3,sum(t3)/len(t3),(b64encode(key).decode('utf-8'),b64encode(iv).decode('utf-8'))]
                if condition !=True:
                    cipher = Cipher(algorithms.AES(str_to_byte(values['-key-'])), modes.CBC(str_to_byte(values['-iv-'])))
                    decryptor = cipher.decryptor()
                    w=decryptor.update(txt2) + decryptor.finalize()
                    t3=timeit.repeat(stmt="w",repeat=10,number=1,globals=locals())
                    d0['AES']=[w,t3,sum(t3)/len(t3)]
            case 4:
                if condition ==True :
                    key = os.urandom(16)
                    iv = os.urandom(8)
                    cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
                    encryptor = cipher.encryptor()
                    ct4= encryptor.update(txt) + encryptor.finalize()
                    t4=timeit.repeat(stmt="ct4",repeat=10,number=1,globals=locals())
                    d0['CAST5']=[b64encode(ct4).decode('utf-8'),t4,sum(t4)/len(t4),(b64encode(key).decode('utf-8'),b64encode(iv).decode('utf-8'))]
                if condition !=True:
                    cipher = Cipher(algorithms.CAST5(str_to_byte(values['-key-'])), modes.CBC(str_to_byte(values['-iv-'])))
                    decryptor = cipher.decryptor()
                    w=decryptor.update(txt2) + decryptor.finalize()
                    t4=timeit.repeat(stmt="w",repeat=10,number=1,globals=locals())
                    d0['CAST5']=[w,t4,sum(t4)/len(t4)]
            case 5:
                if condition ==True :
                    key = os.urandom(16)
                    iv = os.urandom(16)
                    cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
                    encryptor = cipher.encryptor()
                    ct5 = encryptor.update(txt) + encryptor.finalize()
                    t5=timeit.repeat(stmt="ct5",repeat=10,number=1,globals=locals())
                    d0['SEED']=[b64encode(ct5).decode('utf-8'),t5,sum(t5)/len(t5),(b64encode(key).decode('utf-8'),b64encode(iv).decode('utf-8'))]
                if condition !=True:
                    cipher = Cipher(algorithms.SEED(str_to_byte(values['-key-'])), modes.CBC(str_to_byte(values['-iv-'])))
                    decryptor = cipher.decryptor()
                    w=decryptor.update(txt2) + decryptor.finalize()
                    t5=timeit.repeat(stmt="w",repeat=10,number=1,globals=locals())
                    d0['SEED']=[w,t5,sum(t5)/len(t5)]
            case 6:
                if condition ==True :
                    private_key = rsa.generate_private_key(
                        public_exponent=65537,
                        key_size=2048,)
                    pem=save_pr_key(private_key)
                    public_key = private_key.public_key()
                    ciphertext = public_key.encrypt(txt,padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None))
                    t6=timeit.repeat(stmt="ciphertext",repeat=10,number=1,globals=locals())
                    d0['RSA']=[b64encode(ciphertext).decode('utf-8'),t6,sum(t6)/len(t6),b64encode(pem).decode('utf-8')]
                else:
                    plaintext = pr_key.decrypt(
                    txt2,
                padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None))
                    t6=timeit.repeat(stmt="plaintext",repeat=10,number=1,globals=locals())
                    time.append(t6)
                    results.append(sum(t6)/len(t6))
                    d0['RSA']=[plaintext,t6,sum(t6)/len(t6)]
        n=save[j].copy()
        n.update(d0)
        save[j]=n     
 
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
    
    if event == '-mode-':
        save={}
        mode= not mode
        if mode == True:
            window1['-mode-'].update('Multi Mode')
        else:
            window1['-mode-'].update('Single Mode')
            
    if event =='Save':
        if save=={}:
            sg.popup_ok('Please encrypt/decrypt a file first ')
        else:
            if values['-out-']=='':
                sg.popup_ok('Please choose a folder')
            else:
                time=[]
                if values['-choix1-']==True:
                    if mode== False:
                        file=Path(values['-out-']+'/New encrypted file.txt')
                        file2=Path(values['-out-']+'/key file.txt')
                        for i in list(save[values['-In-']].keys()):
                            time.append(save[values['-In-']][i][2])
                        c=save[values['-In-']][list(save[values['-In-']].keys())[time.index(min(time))]]
                        c2=[list(save[values['-In-']].keys())[time.index(min(time))]] 
                        if c2[0]!='RSA':
                            file.write_text(f'{c[0]}\nAlgo Name:{c2[0]}\nkey:{c[3][0]}\nIV:{c[3][1]}')
                        else:
                            file.write_text(f'{c[0]}')
                            file2.write_text(f'{c[3]}')
                    else:
                        s=0
                        for i in list(save.keys()):
                            file=Path(values['-out-']+f'/New encrypted file{s}.txt')
                            file2=Path(values['-out-']+f'/key file{s}.txt')
                            s+=1
                            min=0
                            for j in list(save[i].keys()):
                                if min==0:
                                    min=save[i][j][2]
                                    algo=(i,j)
                                else:
                                    if save[i][j][2]<min:
                                        min=save[i][j][2]
                                        algo=(i,j)
                            if algo[1]!='RSA':
                                file.write_text(f'{save[algo[0]][algo[1]][0]}\nAlgo Name:{algo[1]}\nkey:{save[algo[0]][algo[1]][3][0]}\nIV:{save[algo[0]][algo[1]][3][1]}\nFile:{algo[0]}')
                            else:
                                file.write_text(f'{save[algo[0]][algo[1]][0]}')
                                file2.write_text(f'{save[algo[0]][algo[1]][3]}')
                else:
                    c=save[values['-In-']][list(save[values['-In-']].keys())[0]][0]
                    file=Path(values['-out-']+'/New decrypted file.txt')
                    file.write_text(f'{c.decode().strip()}')
                    
    if event =='Save as':
        if save=={}:
            sg.popup_ok('Please encrypt/decrypt a file first ')
        if  mode != False :
            sg.popup_ok('Please switch to Single Mode')
        else:
            time=[]
            for i in list(save[values['-In-']].keys()):
                    time.append(save[values['-In-']][i][2])
            c=save[values['-In-']][list(save[values['-In-']].keys())[time.index(min(time))]]
            c2=[list(save[values['-In-']].keys())[time.index(min(time))]] 
            file_path=sg.popup_get_file('Save as',no_window=True,save_as=True,file_types=(("Text File","*.txt*"),))+'.txt'
            file=Path(file_path)
            file2=Path('/'.join(file_path.split("/")[:-1]) +'/key file.txt')
            if values['-choix1-']==True:
                if c2[0]!='RSA':
                    file.write_text(f'{c[0]}\nAlgo Name:{c2[0]}\nkey:{c[3][0]}\nIV:{c[3][1]}')
                else:
                    file.write_text(f'{c[0]}')
                    file2.write_text(f'{c[3]}')
            else:
                c=save[values['-In-']][list(save[values['-In-']].keys())[0]][0]
                file.write_text(f'{c.decode().strip()}')

    if event == '-display-':
        if (values['-In-']=='' and mode==False):
            sg.popup_ok('Please choose a file')
        else:
            os.startfile(values['-In-'])

    if event == '-run-' :
        save={}
        if (values['-In-']=='' and mode==False) or (fichier==[] and mode==True):
            sg.popup_ok('Please choose a file')
        else:
            y=0
            for i in checkboxs:
                if values[i]==False:
                    y+=1
            if y==len(checkboxs):
                sg.popup_ok('Please choose an algorithm')
            else:
                if values['-choix1-']==False:
                    if y<len(checkboxs)-1:
                        sg.popup_ok('Please choose just one algorithm in decrypte mode')
                    else:
                        if values[checkboxs[-1]]==True and values['-pr-']=='':
                            sg.popup_ok('Please select the private key file')
                        elif (values['-key-']==''or values['-iv-']=='') and values[checkboxs[-1]]==False:
                            sg.popup_ok('Please put the key and the iv ')
                        else:
                            if mode == False:
                                save[values['-In-']]={}
                            if mode == True:
                                for i in fichier:
                                    save[i]={}
                            current=[]
                            results=[]
                            time=[]
                            if values[checkboxs[0]] == True :
                                encryption(0,values['-choix1-'])
                            if values[checkboxs[1]] == True :
                                encryption(1,values['-choix1-'])
                            if values[checkboxs[2]] == True :
                                encryption(2,values['-choix1-'])
                            if values[checkboxs[3]] == True :
                                encryption(3,values['-choix1-'])
                            if values[checkboxs[4]] == True :
                                encryption(4,values['-choix1-'])
                            if values[checkboxs[5]] == True :
                                encryption(5,values['-choix1-'])
                            if values[checkboxs[6]] == True :
                                encryption(6,values['-choix1-'])
                            if mode ==False:
                                res=[]
                                for i in list(save[values['-In-']].keys()):
                                    time.append(save[values['-In-']][i][2])
                                axes=Fig22.axes
                                axes[0].cla()
                                if values[checkboxs[-1]] != True :
                                    axes[0].plot(list(range(1,11)),save[values['-In-']][list(save[values['-In-']].keys())[time.index(min(time))]][1],marker='o',label=[list(save[values['-In-']].keys())[time.index(min(time))]][0])
                                else:
                                    axes[0].plot(list(range(1,11)),save[values['-In-']]['RSA'][1],marker='o',label='RSA')
                                axes[0].legend()   
                                akg.draw()
                                akg.get_tk_widget().pack()
                                Fig23[2].cla()
                                for j in list(save[values['-In-']].keys()):
                                    res.append(save[values['-In-']][j][2])
                                Fig23[2].bar(list(save[values['-In-']].keys()),res, color='red', width=0.4)
                                plt.title('Time Vs Algorithms', fontsize=16)
                                Fig23[2].xticks(list(save[values['-In-']].keys()))
                                Fig23[2].yticks(res)
                                akg2.draw()
                                akg2.get_tk_widget().pack()
                                if values['-choix1-']== True:
                                    sg.popup_no_buttons(f"Best Time:{min(time)} by {[list(save[values['-In-']].keys())[time.index(min(time))]][0]}\nWorst Time:{max(time)} by {[list(save[values['-In-']].keys())[time.index(max(time))]][0]}\nAverage Time: {sum(time)/len(time)}",title="")
                            else:
                                valve=0
                                algo=''
                                master_time=[]
                                axes=Fig22.axes
                                axes[0].cla()
                                for i in list(save.keys()):
                                    time=[]
                                    for j in list(save[i].keys()):
                                        if valve == 0:
                                            valve=save[i][j][2]
                                            algo=(i,j)
                                        else:
                                            if save[i][j][2]<valve:
                                                valve=save[i][j][2]
                                                algo=(i,j)
                                axes[0].plot(list(range(1,11)),save[algo[0]][algo[1]][1],marker='o',label=''.join(algo[0].split('/')[-1]).split('.')[0]+f'({algo[1]})')
                                axes[0].legend()
                                akg.draw()
                                akg.get_tk_widget().pack()
                                Fig23[2].cla()
                                sticks=[]
                                message='Best match:\n'
                                for i in list(save.keys()):
                                    current=list(save[i].keys())
                                    if sticks==[]:
                                        sticks=np.arange(len(current))
                                    else:
                                        sticks=[x+0.25 for x in sticks]
                                    res=[]
                                    for j in list(save[i].keys()):
                                        res.append(save[i][j][2])
                                    z=''.join(i.split('/')[-1]).split('.')[0]
                                    Fig23[2].bar(sticks,res, width=0.25,label=z)
                                    message+=f'File:{z},Time:{min(res)} by {current[res.index(min(res))]}\n'
                                Fig23[2].xticks([r + 0.25 for r in range(len(current))],
                                current)
                                Fig23[2].legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
                                ncol=3, fancybox=True, shadow=True)
                                plt.title('Time Vs Algorithms', fontsize=16,pad=10)
                                akg2.draw()
                                akg2.get_tk_widget().pack()
                                sg.popup_no_buttons(message,title="")
                else:
                    if mode == False:
                        save[values['-In-']]={}
                    if mode == True:
                        for i in fichier:
                            save[i]={}
                    current=[]
                    results=[]
                    time=[]
                    if values[checkboxs[0]] == True :
                        encryption(0,values['-choix1-'])
                    if values[checkboxs[1]] == True :
                        encryption(1,values['-choix1-'])
                    if values[checkboxs[2]] == True :
                        encryption(2,values['-choix1-'])
                    if values[checkboxs[3]] == True :
                        encryption(3,values['-choix1-'])
                    if values[checkboxs[4]] == True :
                        encryption(4,values['-choix1-'])
                    if values[checkboxs[5]] == True :
                        encryption(5,values['-choix1-'])
                    if values[checkboxs[6]] == True :
                        encryption(6,values['-choix1-'])
                    if mode ==False:
                        res=[]
                        for i in list(save[values['-In-']].keys()):
                            time.append(save[values['-In-']][i][2])
                        axes=Fig22.axes
                        axes[0].cla()
                        axes[0].plot(list(range(1,11)),save[values['-In-']][list(save[values['-In-']].keys())[time.index(min(time))]][1],marker='o',label=[list(save[values['-In-']].keys())[time.index(min(time))]][0])
                        axes[0].legend()   
                        akg.draw()
                        akg.get_tk_widget().pack()
                        Fig23[2].cla()
                        for j in list(save[values['-In-']].keys()):
                            res.append(save[values['-In-']][j][2])
                        Fig23[2].bar(list(save[values['-In-']].keys()),res, color='red', width=0.4)
                        plt.title('Time Vs Algorithms', fontsize=16)
                        Fig23[2].xticks(list(save[values['-In-']].keys()))
                        Fig23[2].yticks(res)
                        akg2.draw()
                        akg2.get_tk_widget().pack()
                        if values['-choix1-']== True:
                            sg.popup_no_buttons(f"Best Time:{min(time)} by {[list(save[values['-In-']].keys())[time.index(min(time))]][0]}\nWorst Time:{max(time)} by {[list(save[values['-In-']].keys())[time.index(max(time))]][0]}\nAverage Time: {sum(time)/len(time)}",title="")
                    else:
                        valve=0
                        algo=''
                        master_time=[]
                        axes=Fig22.axes
                        axes[0].cla()
                        for i in list(save.keys()):
                            time=[]
                            for j in list(save[i].keys()):
                                if valve == 0:
                                    valve=save[i][j][2]
                                    algo=(i,j)
                                else:
                                    if save[i][j][2]<valve:
                                        valve=save[i][j][2]
                                        algo=(i,j)
                        axes[0].plot(list(range(1,11)),save[algo[0]][algo[1]][1],marker='o',label=''.join(algo[0].split('/')[-1]).split('.')[0]+f'({algo[1]})')
                        axes[0].legend()
                        akg.draw()
                        akg.get_tk_widget().pack()
                        Fig23[2].cla()
                        sticks=[]
                        message='Best match:\n'
                        for i in list(save.keys()):
                            current=list(save[i].keys())
                            if sticks==[]:
                                sticks=np.arange(len(current))
                            else:
                                sticks=[x+0.25 for x in sticks]
                            res=[]
                            for j in list(save[i].keys()):
                                res.append(save[i][j][2])
                            z=''.join(i.split('/')[-1]).split('.')[0]
                            Fig23[2].bar(sticks,res, width=0.25,label=z)
                            message+=f'File:{z},Time:{min(res)} by {current[res.index(min(res))]}\n'
                        Fig23[2].xticks([r + 0.25 for r in range(len(current))],
                        current)
                        Fig23[2].legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
                        ncol=3, fancybox=True, shadow=True)
                        plt.title('Time Vs Algorithms', fontsize=16,pad=10)
                        akg2.draw()
                        akg2.get_tk_widget().pack()
                        sg.popup_no_buttons(message,title="")
                                
    if event=='-choix1-'or event=='-choix2-':
        for i in checkboxs:
            window1[i].update(False)
        state=False
        window1['-all-'].update(button_text(state))
        
    if event =='-all-':
        state= not state
        if values['-choix1-']==True:
            for i in checkboxs:
                window1[i].update(state)
        else:
            window1['-1-'].update(state)
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
        sg.popup('Version : 1.0"\n"PySimpleGUI Version :', sg.version, 'This project is made by the efforts of :',  "* Moetez Bouhlel", "* Firas Necib", "* Mohamed Aziz Bouachour",
                     title='About the application')
    
    if event == '-reset-':
        window1['-key-'].update('')
        window1['-iv-'].update('')
        window1['-pr-'].update('')
        window1['-out-'].update('')
        window1['-choix1-'].update(True)
        window1['-In-'].update('')
        window1['-inputs-'].update([])
        fichier=[]
        state=False
        for i in checkboxs:
                window1[i].update(state)
        window1['-all-'].update(button_text(state))
        
    if event == '-trigger-':
        mode=True
        window1['-inputs-'].update(visible=True)
        window1['-trigger-'].update(visible=False)
        window1['-ad-'].update(visible=True)
        fichier=[]
    
    if event == '-link-':
        if fichier!=values['-link-'].split(';'):
            for i in values['-link-'].split(';'):
                if i not in fichier:
                    fichier.append(i)
        window1['-inputs-'].update(fichier)
    
    if  event == '-delete-':
        for i in values['-inputs-']:
            fichier.remove(i)
        window1['-inputs-'].update(fichier)
    
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
            fichier=[]
            mode=False
            window1 = main_window(default)
            Fig22=plot_draw()
            akg=plot_draw2(Fig22,window1['-canvas1-'].TKCanvas)
            Fig23=create_bar_graph([],[])
            akg2=draw_figure(window1['-canvas2-'].TKCanvas,Fig23)
            
window1.close()