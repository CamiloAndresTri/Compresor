from Tkinter import *
import wave, struct
from tkFileDialog import askopenfilename
import matplotlib.pylab as plt

def main():
    def graficar(a,b):
        plt.plot(a)
        plt.plot(b)
        plt.show() 
    global audio, sample, width
    audio=[]
    def leerwav():
        global audio, sample, width
        audio=[]
        file1 = askopenfilename()
        wav = wave.open(file1, "rb")
        sample = wav.getframerate()
        width = wav.getsampwidth()
        Array = int(wav.getnframes())

        for i in range(0, Array):
            datos = wav.readframes(1)
            packed_value = struct.unpack('<h', datos)
            audio.append(int(packed_value[0]))
        wav.close()
        comp.config(state=NORMAL)
        gate.config(state=NORMAL)
        print max(audio)

    def writewav(a):
        ruta=newfile1.get()
        print max(a)
        w = wave.open(ruta, 'w')
        w.setparams((1, width, sample, 0, 'NONE', 'not compressed'))

        for i in range(0, len(a)):
            packed_value = struct.pack('<h', a[i])
            w.writeframes(packed_value)
        w.close()
    def com():
        attack=float(attack1.get())*(sample/1000.0)
        release=float(release1.get())*(sample/1000.0)
        wavearray = []
        #m = (10 ** ((-abs(float(ratio1.get())))) / (10 ** (1.0/ 20)))
        m=1.0/(float(ratio1.get()))
        T = (2.0 ** (width*8 - 1)) * (10.0 ** (-abs(float(tresh1.get())) / 20.0))
        r=0
        a=0
        c=2
        rc=2
        for i in range(0, len(audio)):
    
            if abs(audio[i]) > T:
                
                if audio[i]>0:
                    wavearray.append((m * audio[i] + T * (1.0 - m)))
                else:
                    wavearray.append((m * audio[i] - T * (1.0 - m)))
            else:
               wavearray.append(int(audio[i]))
        

        print max(wavearray)
        
        writewav(wavearray)
        graficar(wavearray,audio)
    def gat():
        wavearray=[]
        T = (2.0 ** (width*8 - 1)) * (10.0 ** (-abs(float(tresh1.get())) / 20.0))
        release=float(release1.get())*(sample/1000.0)
        g=0
        r=0
        for i in range(0,len(audio)):
            if audio[i]<T:
                if g==0:
                    if r>release:
                        g=1
                        wavearray.append(int(audio[i]))
                    else:
                        
                        wavearray.append((-1.0*r+release)*audio[i]/release)
                        r=r+1
                else:
                    
                    wavearray.append(0)
            else:
                r=0
                g=0
                wavearray.append(int(audio[i]))
        writewav(wavearray)
        graficar(wavearray,audio)
    
    ventana = Tk()
    ventana.title("Compresor")
    fr1 = Frame(ventana)
    fr1.pack(side=TOP)
    fr2 = Frame(ventana)
    fr2.pack(side=TOP)
    subfr1 = Frame(fr2)
    subfr1.pack(side=LEFT)
    subfr2 = Frame(fr2)
    subfr2.pack(side=LEFT)

    OpenButton1 = Button(fr1, padx=30, pady=2, text="Abrir Archivo", command=leerwav)
    OpenButton1.pack(side=TOP)


    newfile1 = Entry(subfr1, bd=5, insertwidth=1)
    newfile1.pack(side=BOTTOM, padx=15, pady=2)
    Label(subfr1, text="Ingrese el nombre del Archivo a generar:    ").pack(side=BOTTOM)
    Label(subfr1, text="Ratio:   x:1    ").pack(side=TOP)
    ratio1 = Entry(subfr1, bd=5, insertwidth=1)
    ratio1.pack(side=TOP, padx=10, pady=2)

    Label(subfr1, text="Attack (ms):    ").pack(side=TOP)
    attack1 = Entry(subfr1, bd=5, insertwidth=1)
    attack1.pack(side=TOP, padx=10, pady=2)

    Label(subfr1, text="Release (ms):    ").pack(side=TOP)
    release1 = Entry(subfr1, bd=5, insertwidth=1)
    release1.pack(side=TOP, padx=10, pady=2)

    Label(subfr1, text="Treshold (dB FS):    ").pack(side=TOP)
    tresh1 = Entry(subfr1, bd=5, insertwidth=1)
    tresh1.pack(side=TOP, padx=10, pady=2)

    comp = Button(subfr2, padx=30, pady=10, text="Compresor", command=com, state=DISABLED)
    comp.pack(side=TOP)

    gate = Button(subfr2, padx=30, pady=10, text="Noise Gate", command=gat, state=DISABLED)
    gate.pack(side=TOP)








    ventana.mainloop()



if __name__ == "__main__":
    main()
