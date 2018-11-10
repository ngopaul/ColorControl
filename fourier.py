import numpy as np, matplotlib.pyplot as plt
from math import *

def index_big(lst):
    for i in range(len(lst)):
        if lst[i] > 1:
            lst[i] = i + 1
        else:
            lst[i] = 0
    return lst

def big(lst):
    return list(map(lambda x : int(x >=1), lst))

frate = 4

x = np.array([0, 1, 0, -1] * 90)
a = sqrt(2)/2
y = np.array([0, a, a, 0, -a, -a] * 60)
mean = 0
std = 1
noise = np.random.normal(mean, std, size=360)
x = x+y+noise

#x = y
w = np.fft.fft(x)
freqs = np.fft.fftfreq(len(x))

# for coef,freq in zip(w,freqs):
#     if coef:
#         print('{c:>6} * exp(2 pi i t * {f})'.format(c=coef,f=freq))

print(freqs.min(), freqs.max())
# print((list(map(lambda x: abs(x*frate), freqs))))
# print((np.abs(w)))

freq_to_strength = np.column_stack((np.transpose(list(map(lambda x: abs(x*frate), freqs))), np.transpose(np.abs(w))))

fts = freq_to_strength[freq_to_strength[:,0].argsort()]

plt.plot(fts[:,:1], fts[:,1:2])

print(fts)

idx = np.argmax(np.abs(w))
freq = freqs[idx]
print(freq)
freq_in_hertz = abs(freq * frate)
#print(freq_in_hertz)

# print('waveform:', a)
# plt.plot(a)
# fft = np.fft.rfftfreq(a)
# print(fft)
# print(index_big(fft))
plt.show()

plt.plot(x)
plt.show()