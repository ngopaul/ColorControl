import alsaaudio, time, audioop
import aubio
# from struct import *
# from scipy import *
# import pyaudio

samplerate = 8000
win_s = 2048
hop_s = win_s // 2
framesize = hop_s

card = 'sysdefault:CARD=Microphone'
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK, 'sysdefault:CARD=1')
inp.setchannels(0)
inp.setrate(samplerate)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(framesize)
max_value = 0

pitcher = aubio.pitch("default", win_s, hop_s, samplerate)
pitcher.set_unit("Hz")
pitcher.set_silence(-40)

while True:
    try:
        _, data = recorder.read()
        samples = np.fromstring(data, dtype=aubio.float_type)
        freq = pitcher(samples)[0]
        energy = np.sum(samples**2)/len(samples)
        print("{:10.4f}{:10.4f}".format(freq, energy))
    except KeyboardInterrupt:
        print("exit")
        break


"""
while True:
    # Read data from device
    l,data = inp.read()
    if l:
        # Return the maximum of the absolute value of all samples in a fragment.
        #print(unpack('hhl',data))
        a = audioop.max(data,2)
        if a > max_value:
            print(a)
            max_value = a
        #print(audioop.max(data, 2))
    time.sleep(.001)

a = 0

def design_filter(lowcut, highcut, fs, order=3):
    nyq = 0.5*fs
    low = lowcut/nyq
    high = highcut/nyq
    global a
    b,a = butter(order, [low,high], btype='band')
    return b,a


def normalize(block):
    global a
    count = len(block)/2/a
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )
    doubles = [x * SHORT_NORMALIZE for x in shorts]
    return doubles


def get_rms(samples):
    sum_squares = 0.0
    for sample in doubles:
        sum_squares += n*n
    return math.sqrt( sum_squares / count )


pa = pyaudio.PyAudio()
stream = pa.open(format = pyaudio.paInt16,
         channels = 1,
         rate = 8000,
         input = True,
         frames_per_buffer = 160)

errorcount = 0

# design the filter
b,a = design_filter(19400, 19600, 48000, 3)
# compute the initial conditions.
zi = lfilter_zi(b, a)

for i in range(1000):
    try:
        block = stream.read(INPUT_FRAMES_PER_BLOCK)
    except:
        errorcount += 1
        print( "(%d) Error recording: %s"%(errorcount,e) )
        noisycount = 1

    samples = normalize(block)

    bandpass_samples,zi = lfilter(b, a, samples, zi)

    amplitude = get_rms(samples)
    bandpass_ampl = get_rms(bandpass_samples)
    print(amplitude)
    print(bandpass_ampl)
"""
