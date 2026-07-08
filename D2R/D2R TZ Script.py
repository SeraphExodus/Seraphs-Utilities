from cInputs import sendInput
from datetime import datetime, timezone, timedelta
import FreeSimpleGUI as sg
import json
import ntplib
from pynput.mouse import Listener, Button
from requests import get
import sys
import win32api
from win32gui import GetWindowText, GetForegroundWindow

headerFont = ("Calibri", 12, 'bold')
summaryFont = ("Calibri", 11, 'bold')
summaryFontStats = ("Calibri", 11)
baseFont = ("Calibri", 10, 'bold')
baseFontStats = ("Calibri", 10, 'bold')
buttonFont = ("Calibri", 13, 'bold')
fontPadding = 0
elementPadding = 4
bgColor = '#202225'
boxColor = '#313338'
textColor = '#f3f4f5'

theme_definition = {'BACKGROUND': boxColor,
                    'TEXT': textColor,
                    'INPUT': bgColor,
                    'TEXT_INPUT': textColor,
                    'SCROLL': bgColor,
                    'BUTTON': ('#f3f4f5', '#202225'),
                    'PROGRESS': ('#01826B', '#D0D0D0'),
                    'BORDER': 1,
                    'SLIDER_DEPTH': 0,
                    'PROGRESS_DEPTH' : 0}

sg.theme_add_new('Discord_Dark', theme_definition)

sg.theme('Discord_Dark')

#Handle pCount control via mouse inputs

pCount = 1
mode = True

def on_click(x, y, button, pressed):
    global pCount
    global mode
    activeWindow = GetWindowText(GetForegroundWindow())
    if pressed and button == Button.middle:
        if activeWindow == 'Diablo II: Resurrected':
            mode = not mode
            if mode:
                print('Mode set to 1-3-5-8')
                if pCount == 7:
                    pCount += 1
                if pCount <= 6 and pCount%2 == 0:
                    pCount -= 1
                sendInput('/players ' + str(pCount))
                print('pCount set to ' + str(pCount))
            else:
                print('Mode set to 1-2-3-4-5-6-7-8')
    if pressed and button == Button.x2:
        if activeWindow == 'Diablo II: Resurrected':
            if mode and pCount <= 5:
                if pCount <= 3:
                    pCount += 2
                else:
                    pCount += 3
                sendInput('/players ' + str(pCount))
                print('pCount set to ' + str(pCount))
            elif not mode and pCount <= 7:
                pCount += 1
                sendInput('/players ' + str(pCount))
                print('pCount set to ' + str(pCount))
    if pressed and button == Button.x1:
        if activeWindow == 'Diablo II: Resurrected':
            if mode and pCount >= 3:
                if pCount == 8:
                    pCount -= 3
                else:
                    pCount -= 2
                print('pCount set to ' + str(pCount))
                sendInput('/players ' + str(pCount))
            elif not mode and pCount >= 2:
                pCount -= 1
                print('pCount set to ' + str(pCount))
                sendInput('/players ' + str(pCount))
                
dataSourceURL = 'https://d2emu.com/data/tz-2023-localized.json'

timeFormat = '%Y-%m-%dT%H:%M:%S'

def formatTime(inputTime):
    return datetime(inputTime.year,inputTime.month,inputTime.day,inputTime.hour,inputTime.minute)

def resetTime():
    currentTime = datetime.now()
    #Reset system time to NTP time
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')
        realTime = datetime.fromtimestamp(response.tx_time) + timedelta(seconds=utcOffset)
        win32api.SetSystemTime(realTime.year,realTime.month,0,realTime.day,realTime.hour,realTime.minute,realTime.second,int(realTime.microsecond/1000))
        print('Time changed from',currentTime,'to',datetime.now())
    except OSError:
        print('Internet date and time could not be reported by server.')

def getData():

    try:

        jsonData = get(dataSourceURL).json()
        with open('jsontzdata.json','w') as f:
            json.dump(jsonData,f)

        time = []
        zone = []

        for i in jsonData:
            zoneTime = datetime.strptime(i['datetime'][:-6], timeFormat)
            time.append(zoneTime)
            zone.append(i['zone']['enUS'])
        
        return time, zone

    except:

        try:
            with open('jsontzdata.json','r') as f:
                jsonData = json.load(f)

            time = []
            zone = []

            for i in jsonData:
                zoneTime = datetime.strptime(i['datetime'][:-6], timeFormat)
                time.append(zoneTime)
                zone.append(i['zone']['enUS'])
            
            return time, zone
        
        except:
            print('Unable to access local or remote Terror Zone time data.',
            'Please ensure you have an active internet connection and then try again in a few minutes.')
            sys.exit()

time, zone = getData()

utcOffsetRaw = formatTime(datetime.now().astimezone(timezone.utc)) - formatTime(datetime.now())
utcOffset = utcOffsetRaw.days * 60 * 60 * 24 + utcOffsetRaw.seconds

tzList = sorted(set(zone))

def main():

    resetTime()

    lCol = [
        [sg.Push(),sg.Text('Current Terror Zone:',font=baseFont,p=1)],
        [sg.Push(),sg.Text('Target Terror Zone:',font=baseFont,p=1)],
    ]

    rCol = [
        [sg.Text('',key='currTZ',font=baseFont,p=1),sg.Push()],
        [sg.Combo(tzList,default_value='Cathedral, Catacombs, Inner Cloister',key='tarTZ',s=50,font=baseFont,p=1,readonly=True),sg.Push()],
    ]

    Layout = [
        [sg.Push(),sg.Column(lCol),sg.Column(rCol),sg.Push()],
        [sg.Text('')],
        [sg.Push(),sg.Button('Set Terror Zone',font=buttonFont),sg.Button('Reset Time',font=buttonFont),sg.Button('Reset Time and Close',font=buttonFont),sg.Push()]
    ]

    window = sg.Window('Terror Zone Manager',Layout,size=(565,125),finalize=True)

    lastTime = datetime.now()
    setTZ = False
    initialize = True

    listener = Listener(
        on_move=None,
        on_click=on_click,
        on_scroll=None)
    listener.start()

    while True:
        event, values = window.read(timeout=0)

        if event == sg.WIN_CLOSED:
            resetTime()
            break

        currentTime = datetime.now()
        utcTime = formatTime(currentTime.astimezone(timezone.utc))
        if utcTime.minute >= 30:
            delta = utcTime.minute-30
        else:
            delta = utcTime.minute
        tzTime = utcTime - timedelta(minutes = delta)
        tzIndex = time.index(tzTime)
        currentTZ = zone[tzIndex]
        window['currTZ'].update(currentTZ)

        if event == 'Set Terror Zone':
            setTZ = True
            initialize = True

        if event == 'Reset Time':
            setTZ = False
            initialize = True
            resetTime()
        
        if event == 'Reset Time and Close':
            setTZ = False
            initialize = True
            resetTime()
            break

        if event == sg.WIN_CLOSE_ATTEMPTED_EVENT:
            resetTime()
            break

        if setTZ:
            if lastTime.minute != currentTime.minute or initialize:
                initialize = False
                targetTZ = values['tarTZ']
                if utcTime.minute in [29, 59] or currentTZ != targetTZ:
                    zoneTimes = []
                    zoneDeltas = []
                    for i in range(tzIndex-100,tzIndex+100):
                        if targetTZ in zone[i]:
                            zoneTimes.append(time[i])
                            delta = utcTime - time[i]
                            delta = abs(delta.days * 60 * 60 * 24 + delta.seconds)
                            zoneDeltas.append(delta)
                    targetTime = zoneTimes[zoneDeltas.index(min(zoneDeltas))]
                    win32api.SetSystemTime(targetTime.year,targetTime.month,0,targetTime.day,targetTime.hour,targetTime.minute,targetTime.second,0)
                    print('Time changed from',currentTime,'to',datetime.now())

        lastTime = currentTime

    window.close()
    listener.stop()
    sys.exit()

main()