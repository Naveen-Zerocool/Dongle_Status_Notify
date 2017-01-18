#--------------------------------

from bs4 import BeautifulSoup
import time,os
from gtts import gTTS
import urllib.request
from tkinter import *

#--------------------------------

global bat_percentage,bat_status,sig_strength
status = 0

#--------------------------------

def quit():
    root.destroy()

def getdata():
    global bat_percentage,bat_status,sig_strength,status
    URL = "http://jiofi.local.html/index.htm"
    page = urllib.request.urlopen(URL)
    soup = BeautifulSoup(page.read(),'html.parser')
    bat_percentage = soup.find("input" ,{"id":"batterylevel"})['value']
    bat_status = soup.find("input" ,{"id":"batterystatus"})['value']
    sig_strength = soup.find("input" ,{"id":"signalstrength"})['value']
    if bat_percentage == "100%" and bat_status == "Charging":
        status = 1
    if bat_percentage < "15%" and bat_status == "Discharging":
        status = 2
    return bat_percentage,bat_status,sig_strength,status;

def fullbat():
    tts = gTTS(text='Battery Full, Please Switch Off Charger', lang='en')
    tts.save("good.mp3")
    os.system("start good.mp3")
    os.remove("good.mp3")

def lowbat():
    tts = gTTS(text='Battery Low, Please Plug In Charger', lang='en')
    tts.save("good.mp3")
    os.system("start good.mp3")
    os.remove("good.mp3")

#--------------------------------

root = Tk()
root.title("JioFi Status")
root.geometry("200x150")

bp, bs, ss, status = getdata()

var1 = StringVar()
var2 = StringVar()
var3 = StringVar()

var1.set("Battery Level : "+bp)
var2.set("Battery Status :"+bs)
var3.set("Signal Strength :"+ss)

if status == 1:
    fullbat()
if status == 2:
    lowbat()
    
label1 = Message( root, textvariable=var1, relief=RAISED, width=200,anchor=CENTER)
label2 = Message( root, textvariable=var2, relief=RAISED, width=200,anchor=CENTER)
label3 = Message( root, textvariable=var3, relief=RAISED, width=200,anchor=CENTER)
button1 = Button( root, text = 'Quit', command=quit)
    
label1.pack()
label2.pack()
label3.pack()
button1.pack()

try:
    while True:
        time.sleep(60)
        bp, bs, ss, status = getdata()
        if status == 1:
            fullbat()
        if status == 2:
            lowbat()
        var1.set("Battery Level : "+bp)
        var2.set("Battery Status :"+bs)
        var3.set("Signal Strength :"+ss)
        root.update()
except:
    while True:
        root.destroy()
        sys.exit(0)
        pass

root.mainloop()
