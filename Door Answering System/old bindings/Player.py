import pyaudio
import wave
import sys
import os
class recorder:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 30
    p=None
    stream=None
    frames=[]
    def __init__(self):
        self.p = pyaudio.PyAudio()
    def record(self,time):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK)
        print("* recording")
        self.frames=[]
        self.RECORD_SECONDS=time
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
        print("* done recording")
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        try:
            f=open("log.txt",'r')
            count=int(f.read())
            f.close()
        except:
            ff=open("log.txt",'w')
            ff.write(str(0))
            ff.close
            count=0
        string="./player/"+str(count)+".wav"
        wf = wave.open(string, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        ff=open("log.txt",'w')
        count+=1
        ff.write(str(count))
        ff.close
class player:
    CHUNK = 1024
    p=None
    def __init__(self):
        self.p = pyaudio.PyAudio()
    def playAll(self):
        ff=os.listdir("./player")
        for i in ff:
            wf = wave.open("./player/"+i, 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            data = wf.readframes(self.CHUNK)
            while data != '':
                stream.write(data)
                data = wf.readframes(self.CHUNK)
            stream.stop_stream()
            stream.close()
            p.terminate()  
            os.remove("./player/"+i)
            f=open("log.txt",'r')
            count=int(f.read())
            count-=1
            f.close()
            f=open("log.txt",'w')
            f.write(count)
            f.close()               