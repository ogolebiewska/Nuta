import tkinter as tk
import matplotlib. pyplot as plot
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# from PIL import Image, ImageTk
from pygame import mixer
from scipy import signal
from scipy.io import wavfile
import numpy, pylab, time
from math import pi
import matplotlib.pyplot as plt
from numpy.fft import rfft
from numpy import argmax, log
from scipy.signal.windows import blackmanharris


class App():

    def __init__(self, master):
        master.minsize(900, 400)
        master.title("JAKĄ NUTĘ GRA INSTRUMENT?")
        self.window(master)
        self.plots(master)
        mixer.init()

    def wybierz_plik(self):
        ftypes = [("wave files", "*.wav")]
        self.filename = tk.filedialog.askopenfilename(initialdir="/", filetypes=ftypes, title="Wybierz plik")

    def play_sound(self):
        try:
            print(self.filename)
            mixer.music.load(self.filename)
            mixer.music.play()
        except NameError:
            tk.messagebox.showerror("Nie znaleziono pliku")

    def pause_sound(self):
        mixer.music.stop()

    def window(self, master):

        self.openButton = tk.Button(text="Wybierz plik", command=self.wybierz_plik)
        self.openButton.grid(row=0, column=1, padx=20)

        self.playButton = tk.Button(text="Graj", command=self.play_sound)
        self.playButton.grid(row=0, column=2, padx=20)

        self.pauseButton = tk.Button(text="Stop", command=self.pause_sound)
        self.pauseButton.grid(row=0, column=4, padx=20)

        self.noteButton = tk.Button(text="Rozpoznaj dźwięk", command=self.t_wykres)
        self.noteButton.grid(row=0, column=5, padx=20)

    def nuta(self, samplingFrequency, signalData):

        windowed = signalData * blackmanharris(len(signalData))
        f = rfft(windowed)
        i = argmax(abs(f))
        a = samplingFrequency * i / len(windowed)
        print(a)
        note = ("Nie mozna rozpoznać.")
        if (a >= 390 and a < 403.5) or (a >= 762 and a < 790):
            note = "Nuta - G"
        elif a >= 403.5 and a < 427.5:
            note = ("Nuta - G#")
        elif a >= 427.5 and a < 451.5:
            note = ("Nuta - A")
        elif a >= 451.5 and a < 479.5:
            note = ("Nuta - A#")
        elif a >= 479.5 and a < 508:
            note = ("Nuta - B")
        elif a >= 508 and a < 538.5:
            note = ("Nuta - C")
        elif a >= 538.5 and a < 570.5:
            note = ("Nuta - C#")
        elif a >= 570.5 and a < 604.5:
            note = ("Nuta - D")
        elif a >= 604.5 and a < 640.5:
            note = ("Nuta - D#")
        elif a >= 640.5 and a < 678.5:
            note = ("Nuta - E")
        elif a >= 678.5 and a < 719:
            note = ("Nuta - F")
        elif a >= 719 and a < 762:
            note = ("Nuta - F#")

        tk.messagebox.showinfo("NUTA", note)

    def t_wykres(self):
        samplingFrequency, signalData = wavfile.read(self.filename)

        if len(signalData.shape) == 2:
            signalData = signalData[:, 0]
        fs = samplingFrequency
        fragment = signalData[:2048]
        fragment = fragment / np.max(np.abs(fragment))
        widmo = 20 * np.log10(np.abs(np.fft.rfft(fragment * np.hamming(2048))) / 1024)
        f = np.fft.rfftfreq(2048, 1 / fs)
        f = f / 1000
        self.wamplituda.clear()
        self.wamplituda.grid(True)
        self.wamplituda.set_xlim(xmin=0)
        self.wamplituda.plot(f, widmo)
        self.wamplituda.set_xlim(xmin=0, xmax=4)
        self.wamplituda.set_ylim(ymin=-90, ymax=0)

        self.waveform_canvas.draw()
        windowed = signalData * blackmanharris(len(signalData))
        f = rfft(windowed)
        i = argmax(abs(f))
        a = samplingFrequency * i / len(windowed)
        print(a)
        self.nuta(samplingFrequency, signalData)

    def plots(self, master):

        x = np.zeros(100)
        x1 = np.zeros((100, 2))
        y = [0] * 100
        self.wamp = Figure(figsize=(5, 3), dpi=100)
        self.wamplituda = self.wamp.add_subplot(111)
        self.wamplituda.grid(True)
        self.wamplituda.axhline()
        self.wamplituda.set_xlim(xmin=0, xmax=4)
        self.wamplituda.set_ylim(ymin=-90, ymax=0)
        self.wamplituda.plot(x, y)

        self.waveforms_frame = tk.Frame(master, borderwidth=3)
        self.waveforms_frame.grid(row=0, column=3)

        title_label_2 = tk.Label(self.waveforms_frame, text="Amplituda Widma")
        title_label_2.pack()

        self.waveform_canvas = FigureCanvasTkAgg(self.wamp, master=self.waveforms_frame)
        self.waveform_canvas.draw()
        self.waveform_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


if __name__ == "__main__":
    root = tk.Tk()
    my_app = App(root)
    root.mainloop()