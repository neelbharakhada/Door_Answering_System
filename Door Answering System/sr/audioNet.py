import pyaudio
import wave
import socket
import pickle
class serverRecorder:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 30
    p=None
    stream=None
    frames=[]
    serversocket = None
    clientsocket=None
    address=None
    time=None
    def __init__(self,ip,port):
        self.serversocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((ip, port))
        self.p = pyaudio.PyAudio()
        self.serversocket.listen(10)
        self.clientsocket,self.address=self.serversocket.accept()
    def Record(self):
        byte=self.clientsocket.recv(1024)
        data=pickle.loads(byte)
        if(data>0):
            print("*recording is started*")
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    frames_per_buffer=self.CHUNK)
            print("* recording")
            self.frames=[]
            self.RECORD_SECONDS=data
            for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
                data = self.stream.read(self.CHUNK)
                self.frames.append(data)
            print("* done recording")
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            wf = wave.open("file.wav", 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            f=open("file.wav",'rb')
            data=f.read()
            f.close()
            self.clientsocket.send(pickle.dumps(len(data)))
            buf=self.clientsocket.recv(1024)
            self.clientsocket.send(data)
            return True
        else:
            print("connection closed")
            self.clientsocket.close()
            return False
class clientRecorder:
    client=None
    def __init__(self,ip,port):
        self.client=socket.socket()
        self.client.connect((ip,port))
    def getRecord(self,time):
        self.client.send(pickle.dumps(time))
        buff=self.client.recv(1024)
        size=pickle.loads(buff)
        self.client.send(b'00')
        data=b''
        while len(data)<size:
            d=self.client.recv(4096)
            data=data+d
        return data