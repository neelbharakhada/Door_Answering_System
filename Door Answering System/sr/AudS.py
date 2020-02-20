from audioNet import serverRecorder
flag=True
server=serverRecorder('127.0.0.1',1080)
while flag:
    flag=server.Record()