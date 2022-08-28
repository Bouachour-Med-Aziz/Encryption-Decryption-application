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
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
check_num=0
state=False
pathset=os.path.expanduser('~/Documents/settingfile.json')
cipher_text=[]
final=[]
checkboxs=['-1-','-2-','-3-','-4-','-5-','-6-','-7-']
available=['TripleDES','Camellia','SM4','AES','CASTS','SEED','RSA']
dict_default = {"setting":{"1":'15',"2":"Calibri","3":"LightGrey1"}}
def word_reader(name):
    docx=zipfile.ZipFile(name)
    content=docx.read('word/document.xml').decode('utf-8')
    cleaned = re.sub('<(.|\n)*?>','',content)
    return cleaned
# def most_frequent(List):
#     counter = 0
#     num = List[0]
     
#     for i in List:
#         curr_frequency = List.count(i)
#         if(curr_frequency> counter):
#             counter = curr_frequency
#             num = i
 
#     return num
def load_key(content):
    private_key = load_pem_private_key(content, None)
    return private_key
def save_pr_key(pr):
    how=pr.private_bytes(encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption())
    return how
def save_pu_key(pu):
    how=pu.public_bytes(encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH)
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

    frame1=[[sg.Text('Input File:',justification='r'),sg.Push(),sg.Input(key='-In-'),sg.FileBrowse(file_types=(("Text File","*.txt*"),("Word Files", "*.docx*"),))],
     [sg.Text('Output Folder:',justification='r'),sg.Input(key='-out-'),sg.FolderBrowse()]]
    frame2=[[sg.Radio("Encryption",'Gp1',key='-choix1-',default=True),sg.Radio("Decryption",'Gp1',key='-choix2-')]]
    subframe1=[[sg.Checkbox('TripleDES',key='-1-',enable_events=True),sg.Checkbox('AES',key='-4-',enable_events=True)],
           [sg.Checkbox('Camellia',key='-2-',enable_events=True),sg.Checkbox('CASTS',key='-5-',enable_events=True)],
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
 
def encryption(alg,condition):
    filename=values['-In-']
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
                cipher_text.append(b64encode(ct0).decode('utf-8'))
                t0=timeit.repeat(stmt="ct0",repeat=10,number=1,globals=locals())
                results.append(sum(t0)/len(t0))
                final.append((b64encode(key).decode('utf-8'),b64encode(iv).decode('utf-8')))
            if condition !=True:
                cipher = Cipher(algorithms.TripleDES(str_to_byte(values['-key-'])), modes.CBC(str_to_byte(values['-iv-'])))
                decryptor = cipher.decryptor()
                w=decryptor.update(txt2) + decryptor.finalize()
                t0=timeit.repeat(stmt="w",repeat=10,number=1,globals=locals())
                results.append(sum(t0)/len(t0))
                cipher_text.append(w)
                
        case 1:
            if condition ==True :
                key = os.urandom(32)
                iv = os.urandom(16)
                cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
                encryptor = cipher.encryptor()
                ct1 = encryptor.update(txt) + encryptor.finalize()
                cipher_text.append(b64encode(ct1).decode('utf-8'))
                t1=timeit.repeat(stmt="ct1",repeat=10,number=1,globals=locals())
                results.append(sum(t1)/len(t1))
                final.append((b64encode(key).decode('utf-8'),b64encode(iv).decode('utf-8')))
            if condition !=True:
                cipher = Cipher(algorithms.Camellia(str_to_byte(values['-key-'])), modes.CBC(str_to_byte(values['-iv-'])))
                decryptor = cipher.decryptor()
                w=decryptor.update(txt2) + decryptor.finalize()
                t1=timeit.repeat(stmt="w",repeat=10,number=1,globals=locals())
                results.append(sum(t1)/len(t1))
                cipher_text.append(w)
        case 2:
            if condition ==True :
                key = os.urandom(16)
                iv = os.urandom(16)
                cipher = Cipher(algorithms.SM4(key), modes.CBC(iv))
                encryptor = cipher.encryptor()
                ct2 = encryptor.update(txt)
                cipher_text.append(b64encode(ct2).decode('utf-8'))
                t2=timeit.repeat(stmt="ct2",repeat=10,number=1,globals=locals())
                results.append(sum(t2)/len(t2))
                final.append((b64encode(key).decode('utf-8'),b64encode(iv).decode('utf-8')))
            if condition !=True:
                cipher = Cipher(algorithms.SM4(str_to_byte(values['-key-'])), modes.CBC(str_to_byte(values['-iv-'])))
                decryptor = cipher.decryptor()
                w=decryptor.update(txt2) + decryptor.finalize()
                t2=timeit.repeat(stmt="w",repeat=10,number=1,globals=locals())
                results.append(sum(t2)/len(t2))
                cipher_text.append(w)
        case 3:
            if condition ==True :
                key = os.urandom(32)
                iv = os.urandom(16)
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
                encryptor = cipher.encryptor()
                ct3 = encryptor.update(txt) + encryptor.finalize()
                cipher_text.append(b64encode(ct3).decode('utf-8'))
                t3=timeit.repeat(stmt="ct3",repeat=10,number=1,globals=locals())
                results.append(sum(t3)/len(t3))
                final.append((b64encode(key).decode('utf-8'),b64encode(iv).decode('utf-8')))
            if condition !=True:
                cipher = Cipher(algorithms.AES(str_to_byte(values['-key-'])), modes.CBC(str_to_byte(values['-iv-'])))
                decryptor = cipher.decryptor()
                w=decryptor.update(txt2) + decryptor.finalize()
                t3=timeit.repeat(stmt="w",repeat=10,number=1,globals=locals())
                results.append(sum(t3)/len(t3))
                cipher_text.append(w)
        case 4:
            if condition ==True :
                key = os.urandom(16)
                iv = os.urandom(8)
                cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
                encryptor = cipher.encryptor()
                ct4= encryptor.update(txt) + encryptor.finalize()
                cipher_text.append(b64encode(ct4).decode('utf-8'))
                t4=timeit.repeat(stmt="ct4",repeat=10,number=1,globals=locals())
                results.append(sum(t4)/len(t4))
                final.append((b64encode(key).decode('utf-8'),b64encode(iv).decode('utf-8')))
            if condition !=True:
                cipher = Cipher(algorithms.CAST5(str_to_byte(values['-key-'])), modes.CBC(str_to_byte(values['-iv-'])))
                decryptor = cipher.decryptor()
                w=decryptor.update(txt2) + decryptor.finalize()
                t4=timeit.repeat(stmt="w",repeat=10,number=1,globals=locals())
                results.append(sum(t4)/len(t4))
                cipher_text.append(w)
        case 5:
            if condition ==True :
                key = os.urandom(16)
                iv = os.urandom(16)
                cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
                encryptor = cipher.encryptor()
                ct5 = encryptor.update(txt) + encryptor.finalize()
                cipher_text.append(b64encode(ct5).decode('utf-8'))
                t5=timeit.repeat(stmt="ct5",repeat=10,number=1,globals=locals())
                results.append(sum(t5)/len(t5))
                final.append((b64encode(key).decode('utf-8'),b64encode(iv).decode('utf-8')))
            if condition !=True:
                cipher = Cipher(algorithms.SEED(str_to_byte(values['-key-'])), modes.CBC(str_to_byte(values['-iv-'])))
                decryptor = cipher.decryptor()
                w=decryptor.update(txt2) + decryptor.finalize()
                t5=timeit.repeat(stmt="w",repeat=10,number=1,globals=locals())
                results.append(sum(t5)/len(t5))
                cipher_text.append(w)
        case 6:
            if condition ==True :
                private_key = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=2048,)
                pem=save_pr_key(private_key)
                final.append(b64encode(pem).decode('utf-8'))
                public_key = private_key.public_key()
                ciphertext = public_key.encrypt(txt,padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None))
                t6=timeit.repeat(stmt="ciphertext",repeat=10,number=1,globals=locals())
                results.append(sum(t6)/len(t6))
                cipher_text.append(b64encode(ciphertext).decode('utf-8'))
            else:
                plaintext = pr_key.decrypt(
                txt2,
            padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None))
                t6=timeit.repeat(stmt="plaintext",repeat=10,number=1,globals=locals())
                results.append(sum(t6)/len(t6))
                cipher_text.append(plaintext)
               
        
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
    if event =='Save':
        if values['-choix1-']==True:
            file=Path(values['-out-']+'/New encrypted file.txt')
            file2=Path(values['-out-']+'/key file.txt')
            if current[results.index(min(results))]!='RSA':
                file.write_text(f'{cipher_text[results.index(min(results))]}\nAlgo Name:{current[results.index(min(results))]}\nkey:{final[results.index(min(results))][0]}\nIV:{final[results.index(min(results))][1]}')
            else:
                file.write_text(f'{cipher_text[results.index(min(results))]}')
                file2.write_text(f'{final[results.index(min(results))]}')
        else:
            file=Path(values['-out-']+'/New decrypted file.txt')
            file.write_text(f'{cipher_text[0].decode().strip()}')
    if event =='Save as':
        file_path=sg.popup_get_file('Save as',no_window=True,save_as=True,file_types=(("Text File","*.txt*"),))+'.txt'
        file=Path(file_path)
        file2=Path('/'.join(file_path.split("/")[:-1]) +'/key file.txt')
        if values['-choix1-']==True:
            if current[results.index(min(results))]!='RSA':
                file.write_text(f'{cipher_text[results.index(min(results))]}\nAlgo Name:{current[results.index(min(results))]}\nkey:{final[results.index(min(results))][0]}\nIV:{final[results.index(min(results))][1]}')
            else:
                file.write_text(f'{cipher_text[results.index(min(results))]}')
                file2.write_text(f'{final[results.index(min(results))]}')
        else:
            file.write_text(f'{cipher_text[0].decode().strip()}')
    if event == '-display-':
        os.startfile(values['-In-'])

            
        
    
    if event == '-run-' :
        current=[]
        results=[]
        cipher_text=[]
        final=[]
        if values[checkboxs[0]] == True :
            current.append(available[0])
            encryption(0,values['-choix1-'])
        if values[checkboxs[1]] == True :
            current.append(available[1])
            encryption(1,values['-choix1-'])
        if values[checkboxs[2]] == True :
            current.append(available[2])
            encryption(2,values['-choix1-'])
        if values[checkboxs[3]] == True :
            current.append(available[3])
            encryption(3,values['-choix1-'])
        if values[checkboxs[4]] == True :
            current.append(available[4])
            encryption(4,values['-choix1-'])
        if values[checkboxs[5]] == True :
            current.append(available[5])
            encryption(5,values['-choix1-'])
        if values[checkboxs[6]] == True :
            current.append(available[6])
            encryption(6,values['-choix1-'])
    
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
        # sg.popup_no_buttons(f"Best Time:{min(results)} by {current[results.index(min(results))]}\nWorst Time:{max(results)} by {current[results.index(max(results))]}\nAverage Time: {sum(results)/len(results)}",title="")
        
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