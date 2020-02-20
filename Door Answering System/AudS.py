from audioNet import serverRecorder
flag=True
server=serverRecorder('192.168.1.3',1080)
while flag:
    flag=server.Record()