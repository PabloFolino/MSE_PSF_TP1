import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sc
import simpleaudio as sa

# Candida de veces que se repite la señal
CANTIDAD=10

f    = 6000
fs   = 44100
sec  = 1                # Cuantos segundos se quiere reproducir
B    = 5000
t    = np.arange(0,sec,1/fs)

#note = (2**15-1)*np.sin(2 * np.pi * B/2*(t/sec) *t)  #sweept

#steps=10
#note=np.array([])
#for i in range(steps):
#   note=np.append(note,[(2**15-1)*np.sin(2 * np.pi * B*(i/steps) *t)])

#note = (2**15-1)*np.sin(2 * np.pi * B * t)             # Señal senoidal a reproducir
#note = (2**15-1)*sc.sawtooth(2 * np.pi * f * t)         # Señal triangular a reproducir
note = (2**15-1)*sc.square(2 * np.pi * f * t)          # Señal cuadrada a reproducir

# Grafica la señal
fig=plt.figure(1)
plt.plot(t,note)
##plt.plot(t[0:5*fs//f],note[:5*fs//f])
plt.show()

audio = note.astype(np.int16)             #tranforma la variable note a entero de 16bits y lo guarda en audio
for i in range(CANTIDAD):
    play_obj = sa.play_buffer(audio, 1, 2, fs)  # sale el audio
    play_obj.wait_done()                        # espera que termine la linea anterior

