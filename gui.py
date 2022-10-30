import os
from threading import Thread
from tkinter import *
from tkinter import Tk
from tkinter.font import BOLD
from tkinter import filedialog
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image

from compressor import compress
from decompressor import decompress

#-- GUI Color Palette and Globals Images
colors = ["light blue", "LightSteelBlue2", "CornflowerBlue", "SlateGray"]
imageList = {
    'unsjLogo_200x200': ['resources/logo_unsj.png',     200,    200,    None],
    'unsjLogo_165x165': ['resources/logo_unsj.png',     165,    165,    None],
    'folderImg_35x35':  ['resources/folder.png',        35,     35,     None],
}

def getImage(name):
    if name in imageList:
        if imageList[name][3] is None:
            imageList[name][3] = ImageTk.PhotoImage(Image.open(imageList[name][0]).resize((imageList[name][1],imageList[name][2])))
        return imageList[name][3]
    return None

#-- Compressor Graphical User Interface
def compressorGUI(root:Tk):
    root.withdraw()
    compressorWindow = Toplevel()
    compressorWindow.title('UNSJ-FCEFyN ~ Teoria de la informacion ~ Compresor ~ COMPRIMIR')
    compressorWindow.resizable(False,False)
    compressorWindow.iconbitmap('resources/logo_unsj.ico')
    compressorWindow.geometry('720x480')
    compressorWindow.config(bg = colors[0])

    def on_closing():
        compressorWindow.destroy()
        root.deiconify()       
    compressorWindow.protocol("WM_DELETE_WINDOW", on_closing)

    #-- UNSJ background image.
    unsjImage = Label(
        compressorWindow,
        image=getImage('unsjLogo_200x200'),
        background=colors[0],
        width=200,
        height=200
    )
    unsjImage.pack(fill='none',expand=False)
    unsjImage.place(x=260,y=10)

    #-- Source label.
    sourceDataFrame = Frame(
        compressorWindow,
        background='yellow',
        width=220,
        height=35
    )
    sourceDataFrame.pack(fill='none',expand=False)
    sourceDataFrame.place(x=25, y=190)
    sourceDataFrame.pack_propagate(False)

    sourceInfo = Label(
        sourceDataFrame,
        text=f'Archivo a comprimir:   ',
        background=colors[0],
        font=('Consolas','13', BOLD),
        fg='black',
        justify=LEFT
    )
    sourceInfo.pack(fill='both', expand=True)

    #-- Wrapper snippet [Source file path textbox]
    sourceFilePathTxtBoxFrame = Frame(
        compressorWindow,
        background=colors[1],
        width=635,
        height=35,
        borderwidth=2,
        relief="raised"
    )
    sourceFilePathTxtBoxFrame.pack(fill='none',expand=False)
    sourceFilePathTxtBoxFrame.place(x=25, y=225)
    sourceFilePathTxtBoxFrame.pack_propagate(False)

    #-- Source file path textbox
    sourceFilePathTxtBox = Text(
        sourceFilePathTxtBoxFrame,
        font=("Helvetica", 16)
    )
    sourceFilePathTxtBox.pack(fill='both', expand=True)
    source_file_path = ''
    sourceFilePathTxtBox.insert('1.0',source_file_path)
    
    #-- Select source path of the file to compress.
    def sourceFilePathSelectorCompress():
        sourceFilePathTxtBox.delete('1.0', END)
        source_file_path = filedialog.askopenfilename(title='abrir', initialdir=os.getcwd(), filetypes=[("Todos los Archivos", "*.*")])
        sourceFilePathTxtBox.insert('1.0',source_file_path)
    
    #-- Wrapper snippet [Button to select source filepath]
    sourceFilePathSelectorFrame = Frame(
        compressorWindow,
        background='green',
        width=35,
        height=35,
    )
    sourceFilePathSelectorFrame.pack(fill='none',expand=False)
    sourceFilePathSelectorFrame.place(x=660, y=225)
    sourceFilePathSelectorFrame.pack_propagate(False)
    
    #-- Button to select source filepath.
    sourceFilePathSelectorBtn = Button(
        sourceFilePathSelectorFrame,
        image=getImage('folderImg_35x35'),
        background=colors[0],
        border=0,
        command=sourceFilePathSelectorCompress
    )
    sourceFilePathSelectorBtn.pack(fill='both', expand=True)

    #-- Destination label.
    destinationDataFrame = Frame(
        compressorWindow,
        background='yellow',
        width=220,
        height=35
    )
    destinationDataFrame.pack(fill='none',expand=False)
    destinationDataFrame.place(x=25, y=275)
    destinationDataFrame.pack_propagate(False)

    destinationInfo = Label(
        destinationDataFrame,
        text=f'Directorio de destino: ',
        background=colors[0],
        font=('Consolas','13', BOLD),
        fg='black',
        justify=LEFT
    )
    destinationInfo.pack(fill='both', expand=True)

    #-- Wrapper snippet [Destination file path textbox]
    destinationFilePathTxtBoxFrame = Frame(
        compressorWindow,
        background=colors[1],
        width=635,
        height=35,
        borderwidth=2,
        relief="raised"
    )
    destinationFilePathTxtBoxFrame.pack(fill='none',expand=False)
    destinationFilePathTxtBoxFrame.place(x=25, y=310)
    destinationFilePathTxtBoxFrame.pack_propagate(False)

    #-- Destination file path textbox
    destinationFilePathTxtBox = Text(
        destinationFilePathTxtBoxFrame,
        font=("Helvetica", 16)
    )
    destinationFilePathTxtBox.pack(fill='both', expand=True)
    destination_file_path = ''
    destinationFilePathTxtBox.insert('1.0',destination_file_path)
    
    #-- Select destination path of the file to compress.
    def destinationFilePathSelectorCompress():
        destinationFilePathTxtBox.delete('1.0', END)
        destination_file_path = filePath = filedialog.askdirectory(title='abrir', initialdir=os.getcwd())
        destinationFilePathTxtBox.insert('1.0',destination_file_path)

    #-- Wrapper snippet [Button to select destination filepath]
    destinationFilePathSelectorFrame = Frame(
        compressorWindow,
        background='green',
        width=35,
        height=35,
    )
    destinationFilePathSelectorFrame.pack(fill='none',expand=False)
    destinationFilePathSelectorFrame.place(x=660, y=310)
    destinationFilePathSelectorFrame.pack_propagate(False)
    
    #-- Button to select destination filepath.
    destinationFilePathSelectorBtn = Button(
        destinationFilePathSelectorFrame,
        image=getImage('folderImg_35x35'),
        background=colors[0],
        border=0,
        command=destinationFilePathSelectorCompress
    )
    destinationFilePathSelectorBtn.pack(fill='both', expand=True)

    compressPercentTxt = StringVar()
    compressPercentTxt.set('0%')

    #-- Wrapper snippet [File Compression Progress Bar]
    compressProgressBarFrame = Frame(
        compressorWindow,
        background=colors[1],
        width=635,
        height=35,
        borderwidth=2,
        relief="raised"
    )
    compressProgressBarFrame.pack(fill='none',expand=False)
    compressProgressBarFrame.place(x=25, y=360)
    compressProgressBarFrame.pack_propagate(False)

    #-- File Compression Progress Bar
    compressProgressBar = Progressbar(
        compressProgressBarFrame,
        orient=HORIZONTAL
    )
    compressProgressBar.pack(fill='both', expand=True)
    
    #-- Wrapper snippet [File Compression Percent Label]
    compressPercentFrame = Frame(
        compressorWindow,
        background='green',
        width=50,
        height=35,
    )
    compressPercentFrame.pack(fill='none',expand=False)
    compressPercentFrame.place(x=660, y=360)
    compressPercentFrame.pack_propagate(False)

    #-- File Compression Percent Label.
    compressPercent = Label(
        compressPercentFrame,
        textvariable=compressPercentTxt,
        background=colors[0],
        font=('Consolas','13', BOLD),
        fg='black',
        justify=LEFT
    )
    compressPercent.pack(fill='both', expand=True)

    def getCompress():
        file_path_source = sourceFilePathTxtBox.get('1.0',END).replace('\n','')
        file_path_destination = destinationFilePathTxtBox.get('1.0',END).replace('\n','')
        try:
            errorLabel.config(text='')
            compressTask = Thread(target=compress,args=(file_path_source, file_path_destination, compressProgressBar, compressPercentTxt, compressBtn))
            compressTask.start()
        except:
            errorLabel.config(text='ERROR')
            compressBtn.config(state=NORMAL)

    #-- Wrapper snippet [compressBtn]
    compressFrame = Frame(
        compressorWindow,
        background=colors[2],
        width=170,
        height=33,
        borderwidth=2,
        relief="raised"
    )
    compressFrame.pack(fill='none',expand=False)
    compressFrame.place(x=275, y=410)
    compressFrame.pack_propagate(False)

    #-- Get compress.
    compressBtn = Button(
        compressFrame,
        background=colors[2],
        text='Comprimir',
        font=('Consolas','15', 'bold'),
        fg='black',
        justify=CENTER,
        command=getCompress
    )
    compressBtn.pack(fill='both', expand=True)

    errorFrame = Frame(
        compressorWindow,
        background=colors[1],
        width=110,
        height=33
    )
    errorFrame.pack(fill='none',expand=False)
    errorFrame.place(x=550,y=410)
    errorFrame.pack_propagate(False)
    
    errorLabel = Label(
        errorFrame,
        background=colors[1],
        text='',
        font=('Consolas','12',BOLD),
        fg='red'
    )
    errorLabel.pack(fill='both', expand=True)

#-- Decompressor Graphical User Interface
def decompressorGUI(root:Tk):
    root.withdraw()
    decompressorWindow = Toplevel()
    decompressorWindow.title('UNSJ-FCEFyN ~ Teoria de la informacion ~ Compresor ~ DESCOMPRIMIR')
    decompressorWindow.resizable(False,False)
    decompressorWindow.iconbitmap('resources/logo_unsj.ico')
    decompressorWindow.geometry('720x480')
    decompressorWindow.config(bg = colors[0])

    def on_closing():
        decompressorWindow.destroy()
        root.deiconify()       
    decompressorWindow.protocol("WM_DELETE_WINDOW", on_closing)

    #-- UNSJ background image.
    unsjImage = Label(
        decompressorWindow,
        image=getImage('unsjLogo_200x200'),
        background=colors[0],
        width=200,
        height=200
    )
    unsjImage.pack(fill='none',expand=False)
    unsjImage.place(x=260,y=10)

    #-- Source label.
    sourceDataFrame = Frame(
        decompressorWindow,
        background='yellow',
        width=220,
        height=35
    )
    sourceDataFrame.pack(fill='none',expand=False)
    sourceDataFrame.place(x=25, y=190)
    sourceDataFrame.pack_propagate(False)

    sourceInfo = Label(
        sourceDataFrame,
        text=f'Archivo a descomprimir:',
        background=colors[0],
        font=('Consolas','13', BOLD),
        fg='black',
        justify=LEFT
    )
    sourceInfo.pack(fill='both', expand=True)

    #-- Wrapper snippet [Source file path textbox]
    sourceFilePathTxtBoxFrame = Frame(
        decompressorWindow,
        background=colors[1],
        width=635,
        height=35,
        borderwidth=2,
        relief="raised"
    )
    sourceFilePathTxtBoxFrame.pack(fill='none',expand=False)
    sourceFilePathTxtBoxFrame.place(x=25, y=225)
    sourceFilePathTxtBoxFrame.pack_propagate(False)

    #-- Source file path textbox
    sourceFilePathTxtBox = Text(
        sourceFilePathTxtBoxFrame,
        font=("Helvetica", 16)
    )
    sourceFilePathTxtBox.pack(fill='both', expand=True)
    source_file_path = ''
    sourceFilePathTxtBox.insert('1.0',source_file_path)
    
    #-- Select source path of the file to descompress.
    def sourceFilePathSelectorDecompress():
        sourceFilePathTxtBox.delete('1.0', END)
        source_file_path = filedialog.askopenfilename(title='abrir', initialdir=os.getcwd(), filetypes=[("Solo archivos KHZ", "*.khz")])
        sourceFilePathTxtBox.insert('1.0',source_file_path)
    
    #-- Wrapper snippet [Button to select source filepath]
    sourceFilePathSelectorFrame = Frame(
        decompressorWindow,
        background='green',
        width=35,
        height=35,
    )
    sourceFilePathSelectorFrame.pack(fill='none',expand=False)
    sourceFilePathSelectorFrame.place(x=660, y=225)
    sourceFilePathSelectorFrame.pack_propagate(False)
    
    #-- Button to select source filepath.
    sourceFilePathSelectorBtn = Button(
        sourceFilePathSelectorFrame,
        image=getImage('folderImg_35x35'),
        background=colors[0],
        border=0,
        command=sourceFilePathSelectorDecompress
    )
    sourceFilePathSelectorBtn.pack(fill='both', expand=True)

    #-- Destination label.
    destinationDataFrame = Frame(
        decompressorWindow,
        background='yellow',
        width=220,
        height=35
    )
    destinationDataFrame.pack(fill='none',expand=False)
    destinationDataFrame.place(x=25, y=275)
    destinationDataFrame.pack_propagate(False)

    destinationInfo = Label(
        destinationDataFrame,
        text=f'Directorio de destino: ',
        background=colors[0],
        font=('Consolas','13', BOLD),
        fg='black',
        justify=LEFT
    )
    destinationInfo.pack(fill='both', expand=True)

    #-- Wrapper snippet [Destination file path textbox]
    destinationFilePathTxtBoxFrame = Frame(
        decompressorWindow,
        background=colors[1],
        width=635,
        height=35,
        borderwidth=2,
        relief="raised"
    )
    destinationFilePathTxtBoxFrame.pack(fill='none',expand=False)
    destinationFilePathTxtBoxFrame.place(x=25, y=310)
    destinationFilePathTxtBoxFrame.pack_propagate(False)

    #-- Destination file path textbox
    destinationFilePathTxtBox = Text(
        destinationFilePathTxtBoxFrame,
        font=("Helvetica", 16)
    )
    destinationFilePathTxtBox.pack(fill='both', expand=True)
    destination_file_path = ''
    destinationFilePathTxtBox.insert('1.0',destination_file_path)
    
    #-- Select destination path of the file to descompress.
    def destinationFilePathSelectorDecompress():
        destinationFilePathTxtBox.delete('1.0', END)
        destination_file_path = filePath = filedialog.askdirectory(title='abrir', initialdir=os.getcwd())
        destinationFilePathTxtBox.insert('1.0',destination_file_path)

    #-- Wrapper snippet [Button to select destination filepath]
    destinationFilePathSelectorFrame = Frame(
        decompressorWindow,
        background='green',
        width=35,
        height=35,
    )
    destinationFilePathSelectorFrame.pack(fill='none',expand=False)
    destinationFilePathSelectorFrame.place(x=660, y=310)
    destinationFilePathSelectorFrame.pack_propagate(False)
    
    #-- Button to select destination filepath.
    destinationFilePathSelectorBtn = Button(
        destinationFilePathSelectorFrame,
        image=getImage('folderImg_35x35'),
        background=colors[0],
        border=0,
        command=destinationFilePathSelectorDecompress
    )
    destinationFilePathSelectorBtn.pack(fill='both', expand=True)
    
    #-- Wrapper snippet [File Decompression Progress Bar]
    decompressProgressBarFrame = Frame(
        decompressorWindow,
        background=colors[1],
        width=635,
        height=35,
        borderwidth=2,
        relief="raised"
    )
    decompressProgressBarFrame.pack(fill='none',expand=False)
    decompressProgressBarFrame.place(x=25, y=360)
    decompressProgressBarFrame.pack_propagate(False)

    #-- File Decompression Progress Bar
    decompressProgressBar = Progressbar(
        decompressProgressBarFrame,
        orient=HORIZONTAL
    )
    decompressProgressBar.pack(fill='both', expand=True)

    #-- Wrapper snippet [File Decompression Percent Label]
    decompressPercentFrame = Frame(
        decompressorWindow,
        background='green',
        width=50,
        height=35,
    )
    decompressPercentFrame.pack(fill='none',expand=False)
    decompressPercentFrame.place(x=660, y=360)
    decompressPercentFrame.pack_propagate(False)
    
    decompressPercentTxt = StringVar()

    #-- File Decompression Percent Label.
    decompressPercent = Label(
        decompressPercentFrame,
        textvariable=decompressPercentTxt,
        background=colors[0],
        font=('Consolas','13', BOLD),
        fg='black',
        justify=LEFT
    )
    decompressPercent.pack(fill='both', expand=True)

    def getDecompress():
        file_path_source = sourceFilePathTxtBox.get('1.0',END).replace('\n','')
        file_path_destination = destinationFilePathTxtBox.get('1.0',END).replace('\n','')
        try:
            errorLabel.config(text='')
            compressTask = Thread(target=decompress,args=(file_path_source, file_path_destination, decompressProgressBar, decompressPercentTxt, decompressBtn))
            compressTask.start()
        except:
            errorLabel.config(text='ERROR')
            decompressBtn.config(state=NORMAL)

    #-- Wrapper snippet [decompressBtn]
    decompressFrame = Frame(
        decompressorWindow,
        background=colors[2],
        width=170,
        height=33,
        borderwidth=2,
        relief="raised"
    )
    decompressFrame.pack(fill='none',expand=False)
    decompressFrame.place(x=275, y=410)
    decompressFrame.pack_propagate(False)

    #-- Get decompress.
    decompressBtn = Button(
        decompressFrame,
        background=colors[2],
        text='Descomprimir',
        font=('Consolas','15', 'bold'),
        fg='black',
        justify=CENTER,
        command=getDecompress
    )
    decompressBtn.pack(fill='both', expand=True)

    errorFrame = Frame(
        decompressorWindow,
        background=colors[1],
        width=110,
        height=33
    )
    errorFrame.pack(fill='none',expand=False)
    errorFrame.place(x=550,y=410)
    errorFrame.pack_propagate(False)
    
    errorLabel = Label(
        errorFrame,
        background=colors[1],
        text='',
        font=('Consolas','12',BOLD),
        fg='red'
    )
    errorLabel.pack(fill='both', expand=True)

#-- Initial Graphical User Interface
def mainGUI():
    
    root = Tk()

    root.title('UNSJ-FCEFyN ~ Teoria de la informacion ~ Compresor')
    root.resizable(False,False)
    root.iconbitmap('resources/logo_unsj.ico')
    root.geometry('720x480')
    root.config(bg = colors[0])
    # root.wm_attributes('-alpha', 0.1)
    
    userType = BooleanVar()
    userType.set(False)

    unsjImage = Label(
        root,
        image=getImage('unsjLogo_200x200'),
        background=colors[0],
        width=200,
        height=200
    )
    unsjImage.pack(fill='none',expand=False)
    unsjImage.place(x=260,y=18)

    versionFrame = Frame(
        root,
        background=colors[1],
        width=720,
        height=20
    )
    versionFrame.pack(fill='none',expand=False)
    versionFrame.place(x=0,y=0)
    versionFrame.pack_propagate(False)
    
    versionLabel = Label(
        versionFrame,
        background=colors[1],
        text=" Version: 1.0 - Lento, pero eficaz. 🐌",
        font=('Consolas','12',BOLD),
        fg='red'
    )
    versionLabel.pack(fill='both', expand=True)

    #-- Defino Comprimir -----------------------------
    compressFrame = Frame(
        root,
        background=colors[1],
        width=272,
        height=154,
        borderwidth=2,
        relief="raised"
    )
    compressFrame.pack(fill='none',expand=False)
    compressFrame.place(x=50,y=240)
    compressFrame.pack_propagate(False)

    compressTitleFrame = Frame(
        compressFrame,
        background=colors[1],
        width=150,
        height=30
    )
    compressTitleFrame.pack(fill='none',expand=False)
    compressTitleFrame.place(x=16,y=7)
    compressTitleFrame.pack_propagate(False)
    
    compressTitleLabel = Label(
        compressTitleFrame,
        background=colors[1],
        text="Comprimir",
        font=('Consolas','15'),
        fg='black'
    )
    compressTitleLabel.pack(fill='both', expand=True)

    compressBtnFrame = Frame(
        compressFrame,
        background=colors[1],
        width=20,
        height=20
    )
    compressBtnFrame.pack(fill='none',expand=False)
    compressBtnFrame.place(x=232,y=12)
    compressBtnFrame.pack_propagate(False)

    compressRadioBtn = Radiobutton(
        compressBtnFrame,
        background=colors[1],
        variable=userType,
        value=False
    )
    compressRadioBtn.pack(fill='both', expand=True)

    compressDescriptionTxt =  """Iniciar el programa como\ncompresor.\n\nPermite comprimir archivos usando\nHuffman Estatico, Markov de\norden 1 y Borrows Wheelers."""
    compressDescriptionFrame = Frame(
        compressFrame,
        background=colors[1],
        width=238,
        height=100,
    )
    compressDescriptionFrame.pack(fill='none',expand=False)
    compressDescriptionFrame.place(x=16,y=50)
    compressDescriptionFrame.pack_propagate(False)

    compressDescriptionLabel = Label(
        compressDescriptionFrame,
        background=colors[1],
        text = compressDescriptionTxt,
        font=('Consolas','10'),
        fg='black',
        justify=LEFT
    )
    compressDescriptionLabel.pack(fill='both', expand=True)

    #-- Defino Descompresor -----------------------------
    decompressFrame = Frame(
        root,
        background=colors[1],
        width=272,
        height=154,
        borderwidth=2,
        relief="raised"
    )
    decompressFrame.pack(fill='none',expand=False)
    decompressFrame.place(x=400,y=240)
    decompressFrame.pack_propagate(False)

    decompressTitleFrame = Frame(
        decompressFrame,
        background=colors[1],
        width=150,
        height=30
    )
    decompressTitleFrame.pack(fill='none',expand=False)
    decompressTitleFrame.place(x=16,y=7)
    decompressTitleFrame.pack_propagate(False)
    
    decompressTitleLabel = Label(
        decompressTitleFrame,
        background=colors[1],
        text="Descomprimir",
        font=('Consolas','15'),
        fg='black'
    )
    decompressTitleLabel.pack(fill='both', expand=True)

    decompressBtnFrame = Frame(
        decompressFrame,
        background=colors[1],
        width=20,
        height=20
    )
    decompressBtnFrame.pack(fill='none',expand=False)
    decompressBtnFrame.place(x=232,y=12)
    decompressBtnFrame.pack_propagate(False)

    decompressRadioBtn = Radiobutton(
        decompressBtnFrame,
        background=colors[1],
        variable=userType,
        value=True
    )
    decompressRadioBtn.pack(fill='both', expand=True)

    decompressDescriptionTxt =  """Iniciar el programa como\ndescompresor.\n\nPermite descomprimir archivos khz\ncomprimidos anteriormente.\n"""
    decompressDescriptionFrame = Frame(
        decompressFrame,
        background=colors[1],
        width=238,
        height=100,
    )
    decompressDescriptionFrame.pack(fill='none',expand=False)
    decompressDescriptionFrame.place(x=16,y=50)
    decompressDescriptionFrame.pack_propagate(False)

    decompressDescriptionLabel = Label(
        decompressDescriptionFrame,
        background=colors[1],
        text = decompressDescriptionTxt,
        font=('Consolas','10'),
        fg='black',
        justify=LEFT
    )
    decompressDescriptionLabel.pack(fill='both', expand=True)

    #-- Defino Iniciar -----------------------------
    def start():
        if userType.get(): decompressorGUI(root)
        else: compressorGUI(root)

    startFrame = Frame(
        root,
        background=colors[2],
        width=100,
        height=33,
        borderwidth=2,
        relief="raised"
    )
    startFrame.pack(fill='none',expand=False)
    startFrame.place(x=314, y=409)
    startFrame.pack_propagate(False)

    startBtn = Button(
        startFrame,
        background=colors[2],
        text='Iniciar',
        font=('Consolas','15', 'bold'),
        fg='black',
        justify=CENTER,
        command=start
    )
    startBtn.pack(fill='both', expand=True)
    root.mainloop()
