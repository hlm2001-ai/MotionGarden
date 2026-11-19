"""Generate original, royalty-free calming nature-inspired loops for MotionGarden."""
from pathlib import Path
import numpy as np
from scipy.signal import butter, sosfilt, lfilter
from scipy.io.wavfile import write
import subprocess

out=Path(__file__).parent/'assets'/'audio';out.mkdir(parents=True, exist_ok=True)
sr=22050; duration=32; n=sr*duration; rng=np.random.default_rng(41)
t=np.arange(n)/sr

def smooth(x, fc=200):
    return sosfilt(butter(2,fc,fs=sr,output='sos'), x)

def hp(x,fc=250):
    return sosfilt(butter(2,fc,fs=sr,btype='highpass',output='sos'),x)

def fade_loop(a,sec=2.2):
    # Seam-free periodic crossfade of first and last seconds
    k=int(sr*sec); w=np.sin(np.linspace(0,np.pi/2,k))**2
    mix=a[:k]*w+a[-k:]*(1-w)
    a[:k]=mix;a[-k:]=mix
    return a

def export(name,data,vol=1):
    data=fade_loop(data)
    m=np.max(np.abs(data));data=np.tanh(data*vol/(max(m,1e-6))*0.91)
    wav=out/(name+'.wav');dest=out/(name+'.ogg')
    write(wav,sr,(data*32000).astype('int16'))
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-c:a','libvorbis','-qscale:a','3',str(dest)],check=True)
    wav.unlink();print(name,dest.stat().st_size)

# A rippling shallow stream: multi-band noise, with soft periodic bubbling/ripples.
white=rng.normal(0,1,n)
low=smooth(white,700)
wide=smooth(rng.normal(0,1,n),2100)
stream=(0.64*low+0.20*wide+0.1*hp(smooth(white,5000),500))
mod=(0.83+0.13*np.sin(2*np.pi*t/4.8)+0.08*np.sin(2*np.pi*t/1.21))
stream*=mod
for _ in range(115):
    start=int(rng.uniform(0,duration-.2)*sr);length=int(rng.uniform(.04,.15)*sr)
    dur=np.arange(length)/sr
    bub=(np.sin(2*np.pi*(420*dur-60*dur**2))*np.exp(-24*dur)) * rng.uniform(.03,.11)
    stream[start:start+length]+=bub
export('water',stream,.62)

# Breeze: slow-moving, high-passed airy wash, occasional rolling gusts.
windNoise=smooth(rng.normal(0,1,n),1800)
wind=(windNoise*.7+smooth(rng.normal(0,1,n),380)*.35)*(0.26+0.12*np.sin(2*np.pi*t/8.8)**2+0.12*np.sin(2*np.pi*t/13.4))
export('wind',wind,.47)

# Distant pleasant birds: gently swept and harmonically rich intermittent calls.
birds=np.zeros(n)
for _ in range(63):
    start=int(rng.uniform(.2,duration-.35)*sr);d=rng.uniform(.10,.28);k=int(d*sr)
    td=np.arange(k)/sr
    f0=rng.uniform(1400,2700);sweep=rng.uniform(200,800)
    phase=2*np.pi*(f0*td+sweep*td*td/d/3+70*np.sin(2*np.pi*5*td)*td)
    envelope=np.sin(np.pi*np.minimum(td/d,1))**1.6
    call=(np.sin(phase)+0.28*np.sin(2*phase)) * envelope * rng.uniform(.08,.19)
    birds[start:start+k]+=call
# airy background to keep this layer from being dead silent
birds+=smooth(rng.normal(0,.018,n),650)
export('birds',birds,.83)

# Original music: subtle evolving warm-pad harmonies (Cmaj9 -> Am7 -> Fmaj9 -> Gsus2)
notes=[[130.81,164.81,196,246.94,293.66],[110,130.81,164.81,196,261.63],[87.31,130.81,164.81,196,261.63],[98,146.83,196,220,293.66]]
music=np.zeros(n)
for j, chord in enumerate(notes):
    segStart=j*8;length=int(sr*10);start=int(segStart*sr)
    if start+length>n:length=n-start
    tt=np.arange(length)/sr
    fadeIn=np.minimum(1,tt/3.5);fadeOut=np.minimum(1,np.maximum(0,(10-tt)/3.4));env=fadeIn*fadeOut
    part=np.zeros(length)
    for idx,f in enumerate(chord):
        phase=2*np.pi*f*tt
        part+=(np.sin(phase+0.1*np.sin(2*np.pi*.11*tt))+.2*np.sin(2*phase))*1/(idx+2.6)
    music[start:start+length]+=part*env*.17
# subtle harmonic airy shimmer
music+=0.015*np.sin(2*np.pi*440*t)*np.sin(2*np.pi*t/13)**2
export('music', music, .32)
