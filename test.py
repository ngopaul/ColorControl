import alsaaudio, time, audioop

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
inp.setchannels(0)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_U8)
inp.setperiodsize(160)

while True:
    # Read data from device
    l,data = inp.read()
    if l:
        # Return the maximum of the absolute value of all samples in a fragment.
        print audioop.max(data, 2)
    time.sleep(.001)