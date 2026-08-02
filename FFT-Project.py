import numpy as np
from time import sleep
import scipy as sp
from matplotlib import pyplot as plt
import scipy.io.wavfile as spw
import math as m

# Converts an integer into a binary array
def binaryconverter(size,Input):
    buffer = []
    outputs = []
    n = 1

    for i in range(0,size):
        buffer.insert(0,n)
        n *= 2

    for i in range(0,size):
        if Input >= buffer[i]:
            Input -= buffer[i]
            outputs.append(1)
        else:
            outputs.append(0)

    return(outputs)

# Reverses order of binary array
def binflipper(binorig):
    binnew = []
    for i in range(len(binorig)):
        binnew.append(binorig[-i-1])
    return(binnew)

# Converts binary array back into an integer
def revbinaryconverter(bine):
    output = 0
    binary = 1
    for i in range(len(bine)):
        output += bine[-i-1]*binary
        binary *= 2
    return(output)

# Core FFTBinary Module
def CoreFFTBinary(Input,shift,index,preset):
    audio = Input
    if index == 0:
        newfilt = 0
    else:
        newfilt = 1
    numb = audio.size
    orig = audio.size // 2
    converter = np.zeros((numb,numb),dtype=np.complex128)
    constnumb = numb // 2
    e = 0
    for k in preset:
        numb = constnumb // k
        for c in range(0,k):
            e = 0
            p = 0
            for i in range(0,numb):
                converter[i+c*2*numb,e+c*2*numb] = 1
                converter[(i + numb)+c*2*numb, e+c*2*numb] = m.cos((2*m.pi*(k*i))/(2*constnumb)) + (m.sin((2*m.pi*(k*i))/(2*constnumb)))*1j + newfilt*(m.cos(index*((2*m.pi*(k*i))/(2*constnumb))/shift) + (m.sin(index*((2*m.pi*(k*i))/(2*constnumb)))/shift)*1j)
                e += 1
                p += 1
            e=numb
            p = 0
            for i in range(0,numb):
                converter[i+c*2*numb,e+c*2*numb] = 1
                converter[(i + numb)+c*2*numb, e+c*2*numb] = -((m.cos((2*m.pi*(k*i))/(2*constnumb)) + (m.sin((2*m.pi*(k*i))/(2*constnumb)))*1j) + newfilt*(m.cos(index*((2*m.pi*(k*i))/(2*constnumb))/shift) + (m.sin(index*((2*m.pi*(k*i))/(2*constnumb)))/shift)*1j))
                e += 1
                p += 1
        audio = np.dot(audio,converter)
        converter = np.zeros((audio.size,audio.size),dtype=np.complex128)

    return(audio)

# Input a 1D array of sound intensities (chronological)
# Ouputs a 1D array of frequency spectrums (from lowest to highest)
def calculations(input):
    ind1 = int(m.log(input.size,2) // 1)
    ind = int(2**int(m.log(input.size,2) // 1))
    presinput = np.array(input[0:ind])
    otherinput = np.array(input[ind:])
    npindex = np.arange(0,ind)
    size = ind
    input = otherinput
    preset = []
    for i in range(ind1):
        preset.insert(0,2**i)
    presinput = np.concatenate(([presinput],[npindex]))
    bitflippedinput = np.zeros(ind)
    for i in range(ind):
        column = presinput[:,i]
        a = revbinaryconverter(binflipper(binaryconverter(ind1,column[1])))
        bitflippedinput[a] = column[0]
    audio = CoreFFTBinary(bitflippedinput,1,0,preset)
    audio = audio / ind
    audiooutput = []
    for i in range(audio.size):
        a = np.abs(audio[i])
        audiooutput.append(a)

    return(audiooutput)

# Data processing and externals (intervals must be powers of 2)
def process(audiofile,intervals):
    wow, data = spw.read(audiofile)
    if int(data.ndim) > 1:
        track = 9999
        while track > data.shape[1]:
            track = int(input("This audio track has " + str(data.shape[1]) + " tracks. Choose track: "))
        data = np.array(data[:,(track-1)])
    else:
        data = np.array(data)
    times = data.size // intervals
    for i in range(0,times):
        ndata = data[0+i*intervals:intervals+i*intervals]
        results = np.array(calculations(ndata))
        print("interval "+str(0+i*intervals)+" to interval "+str(intervals+i*intervals)+" out of "+str(data.size)+" Total data points")
        x = np.arange(0,results.size//2)
        y = results[0:results.size//2]
        plt.plot(x,y)
        plt.show()

print("This is just a small project I worked on during my third Co-op Work Term. ")
print("It uses numpy and matplotlib to simulate an FFT, without using any prebuilt external ")
print("FFT modules. Please drag the wav file you wish to analyze into the same folder as this program")
print("MAKE SURE YOU HAVE NUMPY, MATPLOTLIB, AND SCIPY INSTALLED IN YOUR PYTHON ENVIRONMENT")
print("This FFT does calculations for points that are a power of 2, will not be accurate if you don't specify a power of two for the # between intervals")
print("")
sleep(3)
print("If a wavfilewarning occurs, ignore. The wav file contains extraneous metadata scipy doesn't support")
sleep(2)
print("")
intervals = int(input("The interval for each FFT, must be a power of 2 (might crash your computer if it's over 16k): "))
print("")
soundfile = str(input("Please type the full name of the .wav file you intend to use the FFT for: "))

process(soundfile,intervals)






