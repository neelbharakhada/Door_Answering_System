import RPi.GPIO as a
import time
from NetPlayer import recorder
from NetPlayer import player
rec=recorder()
pl=player()
flag = True
flag2 = False
a.setwarnings(False) # Ignore warning for now
a.setmode(a.BOARD) # Use physical pin numbering
a.setup(8, a.IN, pull_up_down=a.PUD_DOWN)
a.setup(10, a.IN, pull_up_down=a.PUD_DOWN)
while True:
    if a.input(8)==1:
        flag = not flag
        print(flag," Button8")
        time.sleep(0.3)
        if flag==True:
            print('play')
            pl.playAll()
    if a.input(10)==1:
        if flag:
            print("bell")
        else:
            print("record")
            rec.record(30)

        time.sleep(0.3)