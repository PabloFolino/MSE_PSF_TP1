# Autos : Pablo D. Folino
# Ejercitación de señales senoidales, cuadradas y triangulares

from typing import Any
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft.helper import fftshift
import scipy.signal as sc
from scipy.fftpack import fft,fftfreq 
from matplotlib.animation import FuncAnimation
import time
import os

#Valores a probar
N   =  8     # Número de muestras 
fs  =  8     # frecuencia de muestreo en Hz
ts  =  1/fs
f   =  1        # frecuencia de la señal a realizar la transformada
fase = 0        # fase de la señal en radianes
amp = 1.0        # ampitud de la señal
X=[]            # Vector complejo en donde se guardan los valores 
                # de la transformada discreta de Fourier
F=[]
faux=0          # Frecuencia de la 2da señal a transformar


# Funciones 
def valores():
    global N,fs,fase,amp
    os.system("clear")
    print("Los valores actuales son:")
    print("La cantidad de muestras es N={}".format(N))
    print("La amplitud de la señal es={}".format(amp))  
    print("La fase de la señal en radianes es={}*Pi radianes".format(fase)) 
    print("La frecuencia de fs={}Hz, y el ts={}seg".format(fs,1/fs)) 
    consulta=input("Desea cambiar los valores S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        valor=input("Ingrese el número de muestras N =")
        if valor.isdigit():
            N=int(valor)
        valor=input("Ingrese la amplitud de la señal entre 0 a 100% =")
        if valor.isdigit():
            amp=float(valor)/100        
        valor=input("Ingrese la fase en grados( enteros) entre 0 a 360 =")
        if valor.isdigit():
            fase=float(valor)*np.pi/180      
        valor=input("Ingrese la frecuencia Hz de sampling fs =")
        if valor.isdigit():
            fs=int(valor)        
            print("El tiempo de sampleo es ts={}".format(1/fs))
        input("Presiona cualquier tecla para continuar")
        os.system("clear")
     
def tdf_manual(funcion,N,fs):
    temp=[]
    # Genero X de N posiciones
    df=0                        # delta de frecuencia
    for i in range(N):
        X.append(complex(0))           # donde se guarda TDF los números complejos
        F.append((-fs/2)+df*(fs/N))    # donde se guarda la frecuencia
        df+=1
    # Barro por frecuencia in range(int(-fs/2),int(fs/2-(fs/N))):
    for frec in range(0,N,1):
        for k in range(0,N,1):
            X[frec]+=funcion[k]*(np.exp(-1j*2*np.pi*F[frec]*k/fs))
    return X,F

# Se usa para acomodar el orden de las listas que entrega numpy.fft
def rotar(lista):
    for n1 in range(0,int(len(lista)/2)):
        temp=lista[len(lista)-1]
        for n2 in range(len(lista)-1,0,-1):
            lista[n2]=lista[n2-1]
        lista[0]=temp
    return lista

# Transformada Rápida de Fourier
def  tdf(funcion,N,ts):
    X_fft=fft(funcion)
    X_fft=rotar(X_fft)
    F_fft=fftfreq(len(funcion),ts)
    F_fft=rotar(F_fft)
    return  X_fft,F_fft

def graficar(encabezado,funcion,n,X,F,X_fft,F_fft):
    fig = plt.figure(1)
    plt.suptitle(encabezado)
    plt.subplots_adjust(left=0.08, bottom=0.08, right=0.98, top=0.9, wspace=0.4, hspace=0.8)
    
    s1 = fig.add_subplot(4,1,1)
    plt.title("Señal")
    plt.xlabel("Tiempo(s)")
    plt.ylabel("Amplitud")
    s1.grid(True)
    s1.plot(n,funcion,'ro')
    s1.plot(n,funcion,'b-')
    
    s2 = fig.add_subplot(4,2,3)
    plt.title("Transformada Manual")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("|Amplitud FFT|")
    s2.grid(True)
    plt.xlim(-fs/2,fs/2-fs/N)
    s2.plot(F,np.abs(X),"g")

    s3 = fig.add_subplot(4,2,5)
    plt.title("Transformada Manual")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Real-Imag. de FFT|")
    s3.grid(True)
    plt.xlim(-fs/2,fs/2-fs/N)
    s3.plot(F,np.real(X),"b-")
    s3.plot(F,np.imag(X),"r-")

    s4 = fig.add_subplot(4,2,7)
    plt.title("Angulo calculado en forma Manual")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Angulos")
    plt.ylim(-185,185)
    s4.grid(True)
    s4.plot(F,np.angle(X)*180/np.pi,'bo-')

    s5 = fig.add_subplot(4,2,4)
    plt.title("Transformada usando el módulo scipy")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Amplitud FFT ")
    s5.grid(True)
    plt.xlim(-fs/2,fs/2-fs/N)
    s5.plot(F_fft,np.abs(X_fft),"g")

    s6 = fig.add_subplot(4,2,6)
    plt.title("Transformada usando el módulo scipy")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Real-Imag. de FFT|")
    s6.grid(True)
    plt.xlim(-fs/2,fs/2-fs/N)
    s6.plot(F_fft,np.real(X_fft),"b-")
    s6.plot(F_fft,np.imag(X_fft),"r-")

    s7 = fig.add_subplot(4,2,8)
    plt.title("Angulo usando el módulo scipy")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Angulos")
    plt.ylim(-185,185)
    s7.grid(True)
    s7.plot(F_fft,np.angle(X_fft)*180/np.pi,'bo-')
    
    #plt.get_current_fig_manager().window.showMaximized() #para QT5
    plt.show()

def graficar2(encabezado,funcion,n,X_fft,F_fft):
    fig = plt.figure(1)
    plt.suptitle(encabezado)
    plt.subplots_adjust(left=0.08, bottom=0.08, right=0.98, top=0.9, wspace=0.4, hspace=0.8)
    
    s1 = fig.add_subplot(4,1,1)
    plt.title("Señal")
    plt.xlabel("Tiempo(s)")
    plt.ylabel("Amplitud")
    s1.grid(True)
    s1.plot(n,funcion,'ro')
    s1.plot(n,funcion,'b-')
    
    s5 = fig.add_subplot(4,1,2)
    plt.title("Transformada usando el módulo scipy")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("| Amplitud FFT | ")
    s5.grid(True)
    plt.xlim(-fs/2,fs/2-fs/N)
    s5.plot(F_fft,np.abs(X_fft),"g")

    s6 = fig.add_subplot(4,1,3)
    plt.title("Transformada usando el módulo scipy")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Real-Imag. de FFT")
    s6.grid(True)
    plt.xlim(-fs/2,fs/2-fs/N)
    s6.plot(F_fft,np.real(X_fft),"b-")
    s6.plot(F_fft,np.imag(X_fft),"r-")

    s7 = fig.add_subplot(4,1,4)
    plt.title("Angulo usando el módulo scipy")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Angulos")
    plt.ylim(-185,185)
    s7.grid(True)
    s7.plot(F_fft,np.angle(X_fft)*180/np.pi,'bo-')
    
    plt.get_current_fig_manager().window.showMaximized() #para QT5
    plt.show()

# Función senoidal
# Parámetros:
#       fs      --> fecuencia de sampleo
#       f       --> frecuencia de la señal de entrada
#       amp     --> amplitud del señal de 0 a 1.
#       muestras--> cantidad de veces que se repite la señal
#       fase    --> fase de la señal en radianes
# Devuelve:
#       f1      --> vector de señal de la señal 
#       n       --> vector de tienpos de sampling 
def senoidal(fs,f,amp,muestras,fase):
    n = np.arange(0, muestras, 1)/fs        # Intervalo de tiempo en segundos
    f1=amp*np.sin(2*np.pi*f*n+fase)         # Definimos el Vector de Frecuencias
    return f1,n


# Función cuadrada
# Parámetros:
#       fs      --> fecuencia de sampleo
#       f       --> frecuencia de la señal de entrada
#       amp     --> amplitud del señal de 0 a 1.
#       muestras--> cantidad de veces que se repite la señal
# Devuelve:
#       f1      --> vector de señal de la señal 
#       n       --> vector de tienpos de sampling      
def cuadrada(fs,f,amp,muestras,fase):
    n = np.arange(0, muestras, 1)/fs            # Intervalo de tiempo en segundos
    f1 =amp*sc.square(2*np.pi*n*f+fase)         # Definimos una onda
    return f1,n

# Parámetros:
#       fs      --> fecuencia de sampleo
#       f       --> frecuencia de la señal de entrada
#       amp     --> amplitud del señal de 0 a 1.
#       muestras--> cantidad de veces que se repite la señal
# Devuelve:
#       f1      --> vector de señal de la señal 
#       n       --> vector de tienpos de sampling
def triangular(fs,f,amp,muestras,fase):
    n = np.arange(0, muestras, 1)/fs            # Intervalo de tiempo en segundos
    f1 =amp*sc.sawtooth(2*np.pi*f*n+fase,1)     # Definimos una onda
    return f1,n

def fft_senoidal():
    global f,X,F
    print("La frecuencia de la señal es de f={}Hz".format(f)) 
    consulta=input("Desea cambiar los valores S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        f=int(input("Ingrese la nueva frecuencia en Hz = "))
    # Definimos una onda  
    f1,n=senoidal(fs,f,amp,N,fase)             
    # Calculo la transformada discreta de Fourier
    X,F=tdf_manual(f1,N,fs)                 # Transformada Discreta de Fourier--> manual
    X_fft,F_fft=tdf(f1,N,1/fs)              # Transformada Discreta de Fourier-->usando scipy
    # Se grafica para probar las señales
    encabezado="Senoidal -->"+" frecuencia="+str(f)+"Hz"+"  N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
    graficar(encabezado,f1,n,X,F,X_fft,F_fft)

def fft_senoidal2():
    global f, X,F,N,fs,fase,faux

    # Valores iniciales
    fs=1000
    N=1000
    
    menu1="""
    Elija una opción:
    Nota: 
        1) f1 y f2 tiene la misma amplitud.
        2) El valor de fs, amplitud, fase y N lo dan las 
         condiciones generales del programa.
        3) La fase modifica la f1, y la f2 siempre posee 
         fase=0.
        4) Los valores iniciales son fs=1000 y N=1000 para
         las opciones [1],[2] y [5]

    [1] f1=0,1*fs y f2=1,1*fs
    [2] f1="0,49*fs y f2=0,51*fs
    [3] f1=5hz y f2=9hz con N=20 y fs=20Hz
    [4] f1=5hz y f2=12hz con N=20 y fs=20Hz
    [5] Ingrese f1 y f2

    [8] Seteo de frecuencia de la señal de entrada, número de muestras, frecuencia 
    de sampling
    [9] Salir al menú principal
    """
    
    while(True):
        os.system("clear")
        print(menu1)
        opcion=input("Elija una opción: ")

        if opcion== '1':
            # Definimos una onda  
            f1,n=senoidal(fs,fs*0.1,amp,N,fase)
            f2,n=senoidal(fs,fs*1.1,amp,N,0) 
            f1=f1+f2            
            # Calculo la transformada discreta de Fourier
            #X,F=tdf_manual(f1,N,fs)                 # Transformada Discreta de Fourier--> manual
            X_fft,F_fft=tdf(f1,N,1/fs)              # Transformada Discreta de Fourier-->usando scipy
            # Se grafica para probar las señales
            encabezado="2 señales senoidales-->"+"   f1="+str(fs*0.1)+"Hz"+"    f2="+str(fs*1.1)+"Hz"+"   N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
            graficar2(encabezado,f1,n,X_fft,F_fft)

        elif opcion== '2':
            f1,n=senoidal(fs,fs*0.49,amp,N,fase)
            f2,n=senoidal(fs,fs*0.51,amp,N,0) 
            f1=f1+f2            
            # Calculo la transformada discreta de Fourier
            # X,F=tdf_manual(f1,N,fs)                 # Transformada Discreta de Fourier--> manual
            # X_fft=X
            # F_fft=F
            X_fft,F_fft=tdf(f1,N,1/fs)              # Transformada Discreta de Fourier-->usando scipy
            # Se grafica para probar las señales
            encabezado="2 señales senoidales-->"+"   f1="+str(fs*0.49)+"Hz"+"    f2="+str(fs*0.51)+"Hz"+"   N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
            graficar2(encabezado,f1,n,X_fft,F_fft)

        elif opcion== '3':
            N=20
            fs=20
            f1,n=senoidal(fs,5,amp,N,fase)
            f2,n=senoidal(fs,9,amp,N,0) 
            f1=f1+f2            
            # Calculo la transformada discreta de Fourier
            #X,F=tdf_manual(f1,N,fs)                 # Transformada Discreta de Fourier--> manual
            X_fft,F_fft=tdf(f1,N,1/fs)              # Transformada Discreta de Fourier-->usando scipy
            # Se grafica para probar las señales
            encabezado="2 señales senoidales-->"+"   f1="+str(5)+"Hz"+"    f2="+str(9)+"Hz"+"   N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
            graficar2(encabezado,f1,n,X_fft,F_fft)

        elif opcion== '4':
            N=20
            fs=20
            f1,n=senoidal(fs,5,amp,N,fase)
            f2,n=senoidal(fs,12,amp,N,0) 
            f1=f1+f2            
            # Calculo la transformada discreta de Fourier
            #X,F=tdf_manual(f1,N,fs)                 # Transformada Discreta de Fourier--> manual
            X_fft,F_fft=tdf(f1,N,1/fs)              # Transformada Discreta de Fourier-->usando scipy
            # Se grafica para probar las señales
            encabezado="2 señales senoidales-->"+"   f1="+str(5)+"Hz"+"    f2="+str(12)+"Hz"+"   N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
            graficar2(encabezado,f1,n,X_fft,F_fft)

        elif opcion== '5':
            print("La frecuencias son f1={}Hz, y son f2={}Hz".format(f,faux)) 
            print("Nota: La frecuencia ingresada se divide por 10,  ")
            print("o sea si entra f1=120 el valor ingresado es 12Hz.")
            valor=input("Ingrese la f1 en Hz o ENTER para continuar =")
            if valor.isdigit():
                f=float(valor)/10
            valor=input("Ingrese la f2 en Hz o ENTER para continuar =")
            if valor.isdigit():
                faux=float(valor)/10

            f1,n=senoidal(fs,f,amp,N,fase)
            f2,n=senoidal(fs,faux,amp,N,0) 
            f1=f1+f2            
            # Calculo la transformada discreta de Fourier
            #X,F=tdf_manual(f1,N,fs)                 # Transformada Discreta de Fourier--> manual
            X_fft,F_fft=tdf(f1,N,1/fs)              # Transformada Discreta de Fourier-->usando scipy
            # Se grafica para probar las señales
            encabezado="2 señales senoidales-->"+"   f1="+str(f)+"Hz"+"    f2="+str(faux)+"Hz"+"   N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
            graficar2(encabezado,f1,n,X_fft,F_fft)

        elif opcion== '8':
            valores()
        
        elif opcion== '9':
            return 0


def fft_cuadrada():
    global f, X,F
    print("La frecuencia de la señal es de f={}Hz".format(f)) 
    consulta=input("Desea cambiar los valores S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        f=int(input("Ingrese la nueva frecuencia en Hz = "))
    # Definimos una onda  
    f1,n=cuadrada(fs,f,amp,N,fase)             
    # Calculo la transformada discreta de Fourier
    X,F=tdf_manual(f1,N,fs)                 # Transformada Discreta de Fourier--> manual
    X_fft,F_fft=tdf(f1,N,1/fs)              # Transformada Discreta de Fourier-->usando scipy
    # Se grafica para probar las señales
    encabezado="Cuadrada -->"+" frecuencia="+str(f)+"Hz"+"  N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
    graficar(encabezado,f1,n,X,F,X_fft,F_fft)

def fft_triangular():
    global f, X,F
    print("La frecuencia de la señal es de f={}Hz".format(f)) 
    consulta=input("Desea cambiar los valores S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        f=int(input("Ingrese la nueva frecuencia en Hz = "))
    # Definimos una onda  
    f1,n=triangular(fs,f,amp,N,fase)             
    # Calculo la transformada discreta de Fourier
    X,F=tdf_manual(f1,N,fs)                 # Transformada Discreta de Fourier--> manual
    X_fft,F_fft=tdf(f1,N,1/fs)              # Transformada Discreta de Fourier-->usando scipy
    # Se grafica para probar las señales
    encabezado="Triangular -->"+" frecuencia="+str(f)+"Hz"+"  N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
    graficar(encabezado,f1,n,X,F,X_fft,F_fft)

#================================================================
# Inicio del programa principal
#================================================================
menu="""
Programas de la transformada Discreta de Fourier
elija una opción:

[1] Transformada de una señal senoidal (fs,f,amp,muestras,fase)
[2] Transformada de  dos señales senoidales(TP1)
[3] Transformada de una señal cuadrada (fs,f,amp,muestras,fase)
[4] Transformada de una señal triangular (fs,f,amp,muestras,fase)

[6] Valores N=40, fase=0, f=1hz  y fs=20hz
[7] Valores por default N=8 fase=0, f=1hz  y fs=8hz
[8] Seteo de frecuencia de la señal de entrada, número de muestras, frecuencia 
de sampling
[9] Salir
"""

while(True):

    # Limpio las listas en donde se guarda la Fransformada de Fourier
    X=[]
    F=[]

    os.system("clear")
    print(menu)

    opcion=input("Elija una opción: ")

    if opcion== '1':
        fft_senoidal()
    elif opcion== '2':
        fft_senoidal2()
    elif opcion== '3':
        fft_cuadrada()
    elif opcion== '4':
        fft_triangular()
    elif opcion== '5':
        pass
    elif opcion== '6':
        N   =  40        # Número de muestras 
        fs  =  20        # frecuencia de muestreo en Hz
        ts  =  1/fs
        f   =  1        # frecuencia de la señal a realizar la transformada
        fase = 0        # fase de la señal en radianes
        amp = 1.0       # ampitud de la señal
    elif opcion== '7':
        N   =  8       # Número de muestras 
        fs  =  8      # frecuencia de muestreo en Hz
        ts  =  1/fs
        f   =  1       # frecuencia de la señal a realizar la transformada
        fase = 0        # fase de la señal en radianes
        amp = 1.0       # ampitud de la señal
    elif opcion== '8':
        valores()
    elif opcion== '9':
        os.system("clear")
        print("Gracias por usar el programa !!!")
        exit (0)
    else:
        print("No selecionó una opción válida\n\r")