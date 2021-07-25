# Autos : Pablo D. Folino
# Ejercitación de señales senoidales, cuadradas y triangulares

import numpy as np
import scipy.signal as sc
import simpleaudio as sa
import matplotlib.pyplot as plt

#Valores a probar
f   = 10
fs  =100
fase = 1
N   = 2
amp = 1

# Función senoidal
# Parámetros:
#       fs      --> fecuencia de sampleo
#       f       --> frecuencia de la señal de entrada
#       amp     --> amplitud del señal de 0 a 1.
#       muestras--> cantidad de veces que se repite la señal
#       fase    --> fase de la señal en radianes
# Devuelve:
#       t       --> vector de valores temporales
#       senal   --> vector de valores de la señal   
def senoidal(fs,f,amp,muestras,fase):
    if (fs<=f):
         return 0,0
    t=np.arange(0,muestras/f,1/fs)
    return t,(2**15-1)*amp*np.sin(2 * np.pi * f * t+fase)


# Función cuadrada
# Parámetros:
#       fs      --> fecuencia de sampleo
#       f       --> frecuencia de la señal de entrada
#       amp     --> amplitud del señal de 0 a 1.
#       muestras--> cantidad de veces que se repite la señal
# Devuelve:
#       t       --> vector de valores temporales
#       senal   --> vector de valores de la señal  
def cuadrada(fs,f,amp,muestras):
    if (fs<=f):
         return 0,0
    t=np.arange(0,muestras/f,1/fs)
    return t,(2**15-1)*amp*sc.square(2*np.pi*t*f)



# Función triangular
# Parámetros:
#       fs      --> fecuencia de sampleo
#       f       --> frecuencia de la señal de entrada
#       amp     --> amplitud del señal de 0 a 1.
#       muestras--> cantidad de veces que se repite la señal
# Devuelve:
#       t       --> vector de valores temporales
#       senal   --> vector de valores de la señal
def triangular(fs,f,amp,muestras):
    if (fs<=f):
         return 0,0
    t=np.arange(0,muestras/f,1/fs)
    return t,(2**15-1)*sc.sawtooth(2*np.pi*f*t,1)



# Se grafica para probar las señales
fig = plt.figure(1)

s1 = fig.add_subplot(2,2,1)
plt.title("Onda Senoidal")
plt.xlabel("time")
plt.ylabel("Amplitude")
t,senal=senoidal(fs,f,amp,N,fase)
s1.plot(t,senal,"r-o",label="con fase")
t,senal=senoidal(fs,f,0.5,N,0)          # pruebo al 50% de la amplitud
s1.plot(t, senal,"b-")
s1.legend()
s1.grid(True)

s2 = fig.add_subplot(2,2,2)
plt.title("Onda Cuadrada")
plt.xlabel("time")
plt.ylabel("Amplitude")
t,senal=cuadrada(fs,f,amp,N)
s2.plot(t,senal,"g-")
s2.grid(True)


s2 = fig.add_subplot(2,2,3)
plt.title("Onda triangular")
plt.xlabel("time")
plt.ylabel("Amplitude")
t,senal=triangular(fs,f,amp,N)
s2.plot(t,senal,"r-")
s2.grid(True)

plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()