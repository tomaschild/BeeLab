# -*- coding: utf-8 -*-
"""Copia de 1 - BeeLab.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WzN1TkG5rEaeYXy4AUJnIdx5ooozJYag
"""

#Autor: Tomás ALejandro Child Rojas

"""#**PRIMERA PARTE: LIBRERÍAS A UTILIZAR**"""

!pip install thinkx
!pip install pydub

import os
import wave
import pylab
import numpy
import scipy
import thinkdsp
import thinkplot
import numpy as np
import librosa as libsa
from scipy.io import wavfile
from scipy.fftpack import fft
from pydub import AudioSegment
import matplotlib.pyplot as plt
from pydub.utils import make_chunks
from scipy.signal import butter, lfilter
from __future__ import print_function, division

from google.colab import drive
drive.mount('/content/drive')

"""#**SEGUNDA PARTE: DEFINICIÓN DE FUNCIONES**
1) Carga de archivos
"""

# Función para cargar rutas de los archivos
# Argumentos:
#     pathdir: Ruta al directorio con las carpetas o archivos a leer

def read_files(pathdir):

  print("Loading files from: "+pathdir+"...")
  
  if os.path.exists(pathdir) == False:
    print("\tThe path doesn't exist...")
    return None, 1
  
  files = []
  
  for r, d, fs in os.walk(pathdir):
    if fs is not None:
      for f in fs: 
        files.append(pathdir+'/'+f)
  
  return files, 0

"""2) Sampleo de registros"""

# Función que divide cada archivo en muestras de N segundos
# Argumentos:
#     originPath: Ruta del directorio que contiene los archivos a ser muestreados.
#     files: Lista con las rutas de cada archivo.
#     targetPath: Ruta del directorio en el cual serán copiados las muestras.
#     sampleDuration: Duración de las muestras en milisegundos.

def sample_data(originPath,files,targetPath,sampleDuration):
  
  print("Sampling files...")
  
  for f in files:
    fn = f.lstrip(originPath)
    raw_register = AudioSegment.from_file(f, "wav")
    samples = make_chunks(raw_register, sampleDuration)

    for i, sample in enumerate(samples):
      sample_name = targetPath+"/"+fn.rstrip(".wav")+"-{0}.wav".format(i)
      sample.export(sample_name, format="wav")

"""3) Transformación a espectrogramas"""

#Funciones de

def get_wav_signal(filepath):

    sampFreq, signalData = wavfile.read(filepath)
    return sampFreq, signalData

def get_freq_spectrum(wf, freqlim):

    freq_spectrum = wf.make_spectrum()
    thinkplot.config(
      xlabel = "Frequency [Hz]",
      ylabel = "Amplitude [dB]",
      xlim = [-100,freqlim],
      legend=False)
    freq_spectrum.plot()
    plt.show()

def get_spectrogram(sampFreq, signalData, freqlim, target_path):

    plt.specgram(signalData[:,0],Fs=sampFreq)
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    freqlim = [0.0,freqlim]
    plt.ylim(freqlim)
    plt.axis('off')
    plt.savefig(target_path, bbox_inches="tight", facecolor="none", edgecolor="none")

def transform(originPath, targetPath, cutFreq):
    
    print("Loading samples from path: "+originPath+"...")
    
    if os.path.exists(originPath) == False:
      
      print("\tThe path doesn't exist...")
      return None, 1
    
    for r, d, files in os.walk(originPath):
      
      if files is not None:
        
        for f in files:
          fn = originPath+"/"+f
          tfn = targetPath+"/"+f.rstrip(".wav")+".png"
          sf, sd = get_wav_signal(fn)
          get_spectrogram(sf,sd,freqCut,tfn)

    print("Spectrograms exported successfully!")

"""#**TERCERA PARTE: EJEMPLO DE EJECUCIÓN**"""

PATH = "/content/drive/Shared drives/ibee-Data/BeeLab/1-Registros"
files, error = read_files(PATH)

DURATION = 5000
SAMPLESPATH = "/content/drive/Shared drives/ibee-Data/BeeLab/2-Muestras"
sample_data(PATH,files,SAMPLESPATH,DURATION)

SAMPLESPATH = "/content/drive/Shared drives/ibee-Data/BeeLab/5-MuestrasTest"
SPECTPATH = "/content/drive/Shared drives/ibee-Data/BeeLab/6-DatosTest"
CUTFREQ = 2000
transform(SAMPLESPATH, SPECTPATH, CUTFREQ)

SAMPLESPATH = "/content/drive/Shared drives/ibee-Data/BeeLab/2-Muestras"
SPECTPATH = "/content/drive/Shared drives/ibee-Data/BeeLab/3-Datos"
spectroFunc(SAMPLESPATH,SPECTPATH)