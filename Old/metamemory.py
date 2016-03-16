#TO DO
#if they press enter without a bet
#add remember slide
#dont re show them word if the dont put in a bet
#
from __future__ import division
from psychopy import visual, core, gui, data, misc, event, sound
import time, random
import re, csv, os, os.path

# define experiment parameters
expInfo = {'Subject':'1','Session':'1', 'Version': ['A', 'B']}
expInfo['dateStr'] = time.strftime("%Y_%m_%d_%H%M", time.localtime())

# ask for task parameters
dlg = gui.DlgFromDict(expInfo, title='Meta Memory', fixed=['dateStr'],order=['Subject','Session', 'Version'])
if not dlg.OK: core.quit()

#define clocks
experimentclock = core.Clock()
trialClock = core.Clock()

#define window and mouse
mywin = visual.Window([1024,768],allowGUI=True,fullscr=True,monitor="testMonitor",units="pix",color="black")
myMouse = event.Mouse(win=mywin)
#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
#Define Variables and lists
subject = expInfo['Subject']
session = expInfo['Session']
version = expInfo['Version']

round = 1

#load instructions
instructions = []
for n in range (0,3):
    instructions.append((visual.ImageStim(mywin,pos=[0,0],image='./instructions/%s/%i.jpg' %(version,n+1))))
ready = visual.ImageStim(mywin,pos=[0,0],image='./instructions/ready.jpg')

#load questions
questions = visual.ImageStim(mywin,pos=[0,0],image='./blankpage.jpg')


betAsk = visual.ImageStim(mywin, pos=[0,0], image = './questions/%s/R.jpg'%(version))
fileName  = '%s_%s_bets.csv' %(subject,session)

#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------

def WaitForKeyInput():
    text='...'
    #until return pressed, listen for letter keys & add to text string
    while event.getKeys(keyList=['return'])==[]:
        letterlist=event.getKeys(keyList=['0', '1', '2', '3', '4',  '5' , '6', '7', '8', '9','backspace','q'])
        for l in letterlist:
            if l == 'q':
                core.quit()
            #if key isn't backspace, add key pressed to the string
            if l !='backspace':
                if text =="...":
                    text=l
                    pressedkeys=l
                else:
                    text+=l
                    pressedkeys+=(";" + l)
            #otherwise, take the last letter off the string
            elif len(text)>0:
                text=text[:-1]
                pressedkeys+=(";backspace")
            #continually redraw text onscreen until return pressed
            text = unicode(text)
            print "UNICODE"
            print text
            response = visual.TextStim(mywin, height=36,text=text,color="white",pos=(0,-100))
            betAsk.draw()
            response.draw()
            mywin.flip()
            core.wait(0.1)
    RT = trialClock.getTime()
    event.clearEvents()
    return text,RT

def RunBlock():
    already = True
    global round
    #load words
    wordList = './words/words%i.txt' %(round)
    words = list(cor for cor in open(wordList).read().split("\n") if cor)
    print type(words)
    #show words 
    i=0
    while event.getKeys(keyList=['return'])==[]:#wait till ready
        ready.draw()
        mywin.flip()
    while i <12:
        questions.draw()#draw blank
        w = visual.TextStim(mywin, height=55,text= words[i],color="white",pos=(0,0))
        if already == True:
            w.draw()
            mywin.flip()#show word
            core.wait(2)#wait 2 seconds
        betAsk.draw()#ask how much they want to bet
        mywin.flip()
        bet,RT= WaitForKeyInput()#recieve bet input
        #write to data file
        if os.path.exists(fileName): #create/modify data file
            dataFile =open(fileName, 'a')
            fieldnames = ['Subject', 'Session', 'Word', 'Bet']
            datafileWriter = csv.DictWriter(dataFile, lineterminator='\n', fieldnames = fieldnames)
            try:
                print type(bet)
                if bet.isnumeric() == True: #if they did enter a bet, add this row
                    print "FIRST"
                    print bet
                    bet = "u"+bet
                    print bet
                    i +=1
                    already = True
                    datafileWriter.writerow({'Subject': expInfo['Subject'], 'Session': expInfo['Session'], 'Word': words[i], 'Bet':bet.encode("ascii")})
            except AttributeError:
                i=i
                already = False
                print "blank entered1"
                continue
            dataFile.close()
        else:
            with open(fileName, 'w') as dataFile:
                fieldnames = ['Subject', 'Session', 'Word', 'Bet']
                dataFileWriter = csv.DictWriter(dataFile, lineterminator='\n', fieldnames = fieldnames)
                dataFileWriter.writeheader()
                try:
                    print bet
                    if bet.isnumeric() == True: #if they did enter a bet, add this row
                        i +=1
                        already = True
                        datafileWriter.writerow({'Subject': expInfo['Subject'], 'Session': expInfo['Session'], 'Word': words[i], 'Bet':int(bet)})
                except AttributeError:
                    i = i
                    already = False
                    print "blank entered2"
                    continue
                dataFile.close()
    instructions[2].draw()
    mywin.flip()
    round += 1
    core.wait(5)

for x in range(0,10):
    RunBlock()
