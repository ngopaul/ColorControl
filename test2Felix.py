import alsaaudio, time, audioop
import aubio
import numpy as np
import matplotlib.pyplot as plt

samplerate = 16000 #8000
win_s = 2048
hop_s = win_s // 2
framesize = hop_s

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, device='hw:1')
#'sysdefault:CARD=1')
# ,alsaaudio.PCM_NONBLOCK,device='sysdefault:CARD=1') #cardindex=1)
inp.setchannels(1)
inp.setrate(samplerate)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE) #used to be S16 not float
inp.setperiodsize(framesize)
#inp.setperiodsize(1600)

#recorder = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, cardindex=1)
#recorder.setperiodsize(framesize)
#recorder.setrate(samplerate)
#recorder.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)
#recorer.setchannels(1)

pitcher = aubio.pitch("default", win_s, hop_s, samplerate)
pitcher.set_unit("Hz")
#pitcher.set_silence(-40)

#plt.ion()
frate = samplerate

while True:
    #plt.clf()
    try:
        _, data = inp.read()
        #print(data)
        samples = np.fromstring(data, dtype=np.int16) #dtype=aubio.float_type)
        if len(samples) == 0:
            continue
        w = np.fft.fft(samples)
        freqs = np.fft.fftfreq(len(samples))
        freq_to_strength = np.column_stack((np.transpose(list(map(lambda x: abs(x*frate), freqs))), np.transpose(np.abs(w))))
        fts = freq_to_strength[freq_to_strength[:,0].argsort()]
        plt.plot(fts[:,:1], fts[:,1:2])
        #print(samples[10:20])
        #print("len samples != 0")
        #freq = pitcher(samples)[0]
        #energy = np.sum(samples**2)/len(samples)
        #print(freq)
        #print(energy)
        #print("{:10.4f}{:10.4f}".format(freq, energy))
        #print("got to max")
        #print(data)
        length = len(data)
        #print(audioop.max(data[0:length//3], 2), audioop.max(data[length//3:2*length//3+1],2), audioop.max(data[2*length//3:length-1],2))
        #print(samples[20:30])
        count = 0
        new_samp = list(filter(lambda a: a, samples))
        print(new_samp[100:200])
        #freq = pitcher(new_samp)[0]
        #energy = np.sum(new_samp**2)/len(new_samp)
        #print(freq, energy)
        #print(np.fft.rfft(samples))
        #print("got np")
        print('plotting')
        # plt.plot(new_samp)
        #plt.draw()
        plt.show()
        #print(abs(audioop.max(data[0:length//3],2) - audioop.max(data[length//3:2*length//3+1],2)))
    except KeyboardInterrupt:
        #plt.show()
        break
    except ValueError:
        pass
    time.sleep(0.01)
