import pyaudio
import wave
import sys
import os
from audioNet import clientRecorder
class recorder:
    cl=None
    def __init__(self):
        print("init recoder")
        self.cl=clientRecorder('127.0.0.1',1080)
    def record(self,time):
        print("* recording")
        data=self.cl.getRecord(time)
        print("* done recording")
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
        f=open(string,'wb')
        f.write(data)
        f.close()
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
            while True:
                data = wf.readframes(self.CHUNK)
                if data==b'':
                    break
                stream.write(data)
            stream.stop_stream()
            stream.close()
            p.terminate()
            wf.close()  
            os.remove("./player/"+i)
            f=open("log.txt",'r')
            count=int(f.read())
            count-=1
            f.close()
            f=open("log.txt",'w')
            f.write(str(count))
            f.close()               