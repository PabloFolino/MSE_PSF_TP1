#!python3
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.animation import FuncAnimation
import os
import io
from numpy.core.function_base import add_newdoc
import serial

# Variables globales
contador=50              # Se usa para iterar tantas veces

STREAM_FILE=("/dev/ttyUSB1","serial")       # Puerto por default
#STREAM_FILE=("log.bin","file")

header = { "pre": b"*header*", "id": 0, "N": 128, "fs": 10000, "maxIndex":0, "minIndex":0, "maxValue":0, "minValue":0, "rms":0, "pos":b"end*" }
fig    = plt.figure ( 1 )

adcAxe = fig.add_subplot ( 2,1,1                            )
adcLn, = plt.plot        ( [],[],'r-',linewidth=4           )
minValueLn, = plt.plot   ( [],[],'g-',linewidth=2,alpha=0.3 )
maxValueLn, = plt.plot   ( [],[],'y-',linewidth=2,alpha=0.3 )
rmsLn, = plt.plot        ( [],[],'b-',linewidth=2,alpha=0.3 )
minIndexLn, = plt.plot   ( [],[],'go',linewidth=6,alpha=0.8 )
maxIndexLn, = plt.plot   ( [],[],'yo',linewidth=6,alpha=0.8 )
adcAxe.grid              ( True                             )
adcAxe.set_ylim          ( -2 ,2                            )


fftAxe = fig.add_subplot ( 2,1,2                  )
fftLn, = plt.plot        ( [],[],'b-',linewidth=4 )
fftAxe.grid              ( True                   )
fftAxe.set_ylim          ( 0 ,0.25                )

def findHeader(f,h):
    data=bytearray(b'12345678')
    while data!=h["pre"]:
        data+=f.read(1)
        if len(data)>len(h["pre"]):
            del data[0]
    h["id"]       = readInt4File(f,4)
    h["N" ]       = readInt4File(f)
    h["fs"]       = readInt4File(f)
    h["maxIndex"] = readInt4File(f,4)
    h["minIndex"] = readInt4File(f,4)
    h["maxValue"] = (readInt4File(f,sign = True)*1.65)/(2**6*512)
    h["minValue"] = (readInt4File(f,sign = True)*1.65)/(2**6*512)
    h["rms"]      = (readInt4File(f,sign = True)*1.65)/(2**6*512)
    data=bytearray(b'1234')
    while data!=h["pos"]:
        data+=f.read(1)
        if len(data)>len(h["pos"]):
            del data[0]
    print(h)
    return h["id"],h["N"],h["fs"],h["minValue"],h["maxValue"],h["rms"],h["minIndex"],h["maxIndex"]

def readInt4File(f,size=2,sign=False):
    raw=f.read(1)
    while( len(raw) < size):
        raw+=f.read(1)
    return (int.from_bytes(raw,"little",signed=sign))

def flushStream(f,h):
    if(STREAM_FILE[1]=="serial"): #pregunto si estoy usando la bibioteca pyserial o un file
        f.flushInput()
    else:
        f.seek ( 2*h["N"],io.SEEK_END)

def readSamples(adc,N,trigger=False,th=0):
    state="waitLow" if trigger else "sampling"
    i=0
    for t in range(N):
        sample = (readInt4File(streamFile,sign = True)*1.65)/(2**6*512)
        # state,i= {
        #         "waitLow" : lambda sample,i: ("waitHigh",0) if sample<th else ("waitLow" ,0),
        #         "waitHigh": lambda sample,i: ("sampling",0) if sample>th else ("waitHigh",0),
        #         "sampling": lambda sample,i: ("sampling",i+1)
        #         }[state](sample,i)
        adc[t]=sample
    return

def update(t):
    global header
    flushStream ( streamFile,header )
    id,N,fs,minValue,maxValue,rms,minIndex,maxIndex=findHeader ( streamFile,header )
    adc   = np.zeros(N)
    time  = np.arange(0,N/fs,1/fs)
    readSamples(adc,N,True,-1.3)

    adcAxe.set_xlim     ( 0    ,N/fs              )
    adcLn.set_data      ( time ,adc               )
    minValueLn.set_data ( time,minValue           )
    maxValueLn.set_data ( time,maxValue           )
    rmsLn.set_data      ( time,rms                )
    minIndexLn.set_data ( time[minIndex],minValue )
    maxIndexLn.set_data ( time[maxIndex],maxValue )

    fft=np.abs ( 1/N*np.fft.fft(adc ))**2
    fftAxe.set_ylim ( 0 ,np.max(fft)+0.05)
    fftAxe.set_xlim ( 0 ,fs/2 )
    fftLn.set_data ( (fs/N )*fs*time ,fft)

    return adcLn, fftLn, minValueLn, maxValueLn, rmsLn, minIndexLn, maxIndexLn

def seteo():
    os.system("clear")
    print("El dispositivo del cual de se está leyendo los datos es:{}".format(str(STREAM_FILE[0])))
    consulta=input("Desea cambiar los valores S o N[Enter] :")
    return 0

def leer_serie():
    global header,adc
    # Abro el puerto serie
    streamFile = serial.Serial(port=STREAM_FILE[0],baudrate=460800,timeout=None)
    
    contador1=0
    while(contador1<contador):
        # Limpio el buffer de entrada
        streamFile .flushInput()                          
        #Encuentro el encabezado
        id,N,fs,minValue,maxValue,rms,minIndex,maxIndex=findHeader ( streamFile,header )
        adc   = np.zeros(N)
        time  = np.arange(0,N/fs,1/fs)
        readSamples(adc,N,True,-1.3)
        contador1+=1
    
    fig = plt.figure(1)
    plt.suptitle("Prueba de Gráfico")
    plt.subplots_adjust(left=0.08, bottom=0.08, right=0.98, top=0.9, wspace=0.4, hspace=0.8)

    fft=np.abs ( 1/N*np.fft.fft(adc))**2
    #fftLn.set_data ( (fs/N )*fs*time ,fft)

    
    # Gráfico de frecuencia
    s1 = fig.add_subplot(2,1,1)
    plt.title("Señal")
    plt.xlabel("Frecuencia(s)")
    plt.ylabel("Amplitud")
    plt.ylim ( 0 ,np.max(fft)+0.05)
    plt.xlim ( 0 ,fs/2 )
    s1.grid(True)
    s1.plot((fs/N )*fs*time ,fft,'ro')

     
    #plt.get_current_fig_manager().window.showMaximized() #para QT5
    plt.show()
    return 0

#================================================================
# Inicio del programa principal
#================================================================

#seleccionar si usar la biblioteca pyserial o leer desde un archivo log.bin
if(STREAM_FILE[1]=="serial"):
    streamFile = serial.Serial(port=STREAM_FILE[0],baudrate=460800,timeout=None)
else:
    streamFile=open(STREAM_FILE[0],"rb",0)

menu="""
Programas de recepción de datos por el puerto serie
elija una opción:

[1] Leer datos del puerto serie
[2] TBD
[3] TBD
[4] TBD

[6] TBD
[7] TBD
[8] Seteo del puerto serie
[9] Salir
"""

while(True):

    # Limpio las listas en donde se guarda la Fransformada de Fourier
    X=[]
    F=[]

    os.system("clear")
    print(menu)

    opcion=input("Elija una opción: ")

    if opcion == '1':
        leer_serie()
    elif opcion == '2':
        pass
    elif opcion == '3':
        pass
    elif opcion == '4':
        pass
    elif opcion == '5':
        pass
    elif opcion == '6':
        pass
    elif opcion == '7':
        pass
    elif opcion == '8':
        seteo()
    elif opcion== '9':
        streamFile.close()
        os.system("clear")
        print("Gracias por usar el programa !!!")
        exit (0)
    else:
        print("No selecionó una opción válida\n\r")











# ani=FuncAnimation(fig,update,1000,init_func=None,blit=False,interval=1,repeat=True)
# plt.draw()
# #plt.get_current_fig_manager().window.showMaximized() #para QT5
# plt.show()
# streamFile.close()
