#TO DO
#make sure that the list doesn't populate the old words on the recall page--DONE
#Add version to wordListstring so that we can have multiple versions
#Timed feedback--DONE
#add Reaction time to data file--Why does this cause it to repeat???!?!--DONE, did it a different way, ask Martin and Susanne about it
#add performance feedback slide--Done, maybe add to this

from __future__ import division
from psychopy import visual, core, gui, data, misc, event, sound
import time, random
import re, csv, os, os.path,collections

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
#-----------------------------------------------------------------------------------------------------------
#Define Variables and lists---------------------------------------------------------------------------------
subject = expInfo['Subject']
session = expInfo['Session']
version = expInfo['Version']

#load instructions
instructions = []
for n in range (0,3):
    instructions.append((visual.ImageStim(mywin,pos=[0,0],image='./instructions/%s/%i.jpg' %(version,n+1))))
ready = visual.ImageStim(mywin,pos=[0,0],image='./instructions/ready.jpg')
instructions2 = []
instructions2.append((visual.ImageStim(mywin,pos=[0,0],image='./instructions/prompt.jpg')))
instructions2.append((visual.ImageStim(mywin,pos=[0,0],image='./instructions/howto.jpg')))
instructions2.append((visual.ImageStim(mywin,pos=[0,0],image='./instructions/scoring.jpg')))

#load questions
questions = visual.ImageStim(mywin,pos=[0,0],image='./blankpage.jpg')
betAsk = visual.ImageStim(mywin, pos=[0,0], image = './questions/%s/R.jpg'%(version))

#File Names
fileName  = '%s_%s_bets.csv' %(subject,session)
scorefileName  = '%s_1_score.csv' %(subject) #Maybe change this?

#Variables
round = 1
score = 0
scoreYet = False
referenceWords = []
wordsTheyRecalled =[]
corrects = ''
#------------------------------------------------------------------------------------------------------------
#Functions---------------------------------------------------------------------------------------------------

def WaitForKeyInput():
    timer= core.CountdownTimer(5)
    trialClock.reset()
    text='...'
    #until return pressed, listen for letter keys & add to text string
    while event.getKeys(keyList=['return'])==[]:
        letterlist=event.getKeys(keyList=['0', '1', '2', '3', '4',  '5' , '6', '7', '8', '9','backspace','q'])
        color = 'black'
        if timer.getTime() >= 3:
            color = 'green'
        elif timer.getTime() >=0:
            color = 'yellow'
        elif timer.getTime() <0:
            color = 'red'
        feedback = visual.Rect(mywin, width= 200,height = 200, pos = (0,-100), lineWidth=5.0, lineColor = color)
        betAsk.draw()
        feedback.draw()
        response = visual.TextStim(mywin, height=36,text=text,color="white",pos=(0,-100))
        if text != '...':
            response.draw()
        mywin.flip()
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
            event.clearEvents()
    #RT = trialClock.getTime()
    return text
def writeToDataFile(dataFileName,wordToWrite,r,cs):#r is the risk amount variable and cs is the Cumulative Score variable
    print "IVE BEEN CALLED"
    if os.path.exists(dataFileName):
        print "IM CHECKING THE PATH"
        dataFile =open(dataFileName, 'a')
        fieldnames = ['Subject', 'Session', 'Round', 'Word','Points','Cumulative Score']
        dataFileWriter = csv.DictWriter(dataFile, lineterminator='\n', fieldnames = fieldnames)
        dataFileWriter.writerow({'Subject': expInfo['Subject'], 'Session': expInfo['Session'], 'Round':round-1, 'Word': wordToWrite, 'Points': r, 'Cumulative Score': cs})
        print "WRITE"
        dataFile.close()
        print "CLOSED"
    else:
        with open(dataFileName, 'w') as dataFile:
            print "IM CHECKING THE PATH"
            fieldnames = ['Subject', 'Session', 'Round', 'Word','Points','Cumulative Score']
            dataFileWriter = csv.DictWriter(dataFile, lineterminator='\n', fieldnames = fieldnames)
            dataFileWriter.writeheader()
            dataFileWriter.writerow({'Subject': expInfo['Subject'], 'Session': expInfo['Session'], 'Round': round-1, 'Word': wordToWrite, 'Points': r, 'Cumulative Score': cs})
            dataFile.close()
    
def populateOldWords():
    x=[(0,150),(0,100),(0,50),(0,0),(0,-50),(0,-100),(0,-150),(0,-200),(0,-250),(0,-300),(0,-350),(200,150),\
    (200,100),(200,50),(200,0),(200,-50),(200,-100),(200,-150),(200,-200),(200,-250),(200,-300),(200,-350),\
    (-200,150),(-200,100),(-200,50),(-200,0),(-200,-50),(-200,-100),(-200,-150),(-200,-200),(-200,-250),(-200,-300),\
    (-200,-350),(-400,150),(-400,100),(-400,50),(-400,0),(-400,-50),(-400,-100),(-400,-150),(-400,-200),\
    (-400,-250),(-400,-300),(-400,-350),(400,150),(400,100),(400,50),(400,0),(400,-50),(400,-100),\
    (400,-150),(400,-200),(400,-250),(400,-300),(400,-350)]
    c = 0
    for w in wordsTheyRecalled: #prints words they have already typed
        a = visual.TextStim(mywin, height=50,text=w,color="white",pos=(x[c]))
        a.draw()
        c += 1

def WaitForKeyInput2():
    text='...' 
    global scoreYet
    response = visual.TextStim(mywin, height=75,text=text,color="white",pos=(0, 250))
    response.draw()
    instructions2[0].draw()
    populateOldWords()
    mywin.flip()
    #until return pressed, they can type word
    while event.getKeys(keyList=['return'])==[]:
        if scoreYet == True:
            break
        letterlist=event.getKeys(keyList=['q','w','e','r','t','y','u','i','o','p','a','s','d','f',
            'g','h','j','k','l','z','x','c','v','b','n','m', '6',\
            'backspace','f12'])
        for l in letterlist:
            if l == '6':
                scoreYet = True
                break
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
            instructions2[0].draw()
            populateOldWords()
            response = visual.TextStim(mywin, height=75,text=text,color="white",pos=(0, 250))
            response.draw()
            mywin.flip()
    event.clearEvents()
    return text

def findBet(wordinput):
    if os.path.exists(fileName):
        dataFileRead=open(fileName, 'r')
        reader = csv.reader(dataFileRead)
        RowValue = []
        for row in reader:
            RowValue.extend(row)
        targetwordindex= RowValue.index(wordinput)
        targetbetindex = targetwordindex + 1
        bet = RowValue[targetbetindex]
        dataFileRead.close()
        return bet

def WaitForMouseInput():
    goforit = True
    ans = 0
    event.clearEvents()
    waitforrelease = False

    while goforit:
        while True:
            buttons, times = myMouse.getPressed(getTime=True)
            if sum(buttons)>0:
                waitforrelease = True
                event.clearEvents
                break
            if event.getKeys(keyList = "f12"):
                event.clearEvents()
                core.quit()
            event.clearEvents()
        while waitforrelease == True:
            buttons,times = myMouse.getPressed(getTime=True)
            if sum(buttons) == 0:
                RT = trialClock.getTime()
                mouseX,mouseY = myMouse.getPos()
                if mouseY > -300 and mouseY < 0: 
                    if mouseX > -400 and mouseX <0:
                        ans = "yes"
                        goforit = False
                        event.clearEvents()
                        return ans
                        break
                    if mouseX > 0 and mouseX < 400:
                        ans = "no"
                        goforit = False
                        event.clearEvents()
                        return ans
                        break
                else:
                    myMouse.clickReset()
                    waitforrelease = False
                    continue
 
def RunBlock():
    already = True#why is this here again?
    global round
    #load words
    wordList = './words/words%i.txt' %(round)
    words = list(cor for cor in open(wordList).read().split("\n") if cor)
    #show words 
    i=0
    event.clearEvents()
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
        #THIS IS WHERE THE TIMING STUFF WILL GO
        betAsk.draw()#ask how much they want to bet
        mywin.flip()
        trialtime = core.Clock()
        trialtime.reset()
        bet = WaitForKeyInput() #recieve bet input
        RT = trialtime.getTime()
        #write to data file
        if os.path.exists(fileName): #create/modify data file
            dataFile =open(fileName, 'a')
            fieldnames = ['Subject', 'Session','Round','Word', 'Bet','RT']
            dataFileWriter = csv.DictWriter(dataFile, lineterminator='\n', fieldnames = fieldnames)
            try:
                print type(bet)
                if bet.isnumeric() == True: #if they did enter a bet, add this row
                    print "FIRST"
                    print bet
                    i +=1
                    already = True
                    global dataFileWriter
                    dataFileWriter.writerow({'Subject': expInfo['Subject'], 'Session': expInfo['Session'],'Round': round,\
                    'Word': words[i-1],'Bet':bet.encode("ascii"),'RT': RT})
            except AttributeError: #else repeat
                i=i
                already = False
                print "blank entered1"
                continue
            dataFile.close()
        else:
            with open(fileName, 'w') as dataFile:
                fieldnames = ['Subject', 'Session', 'Round', 'Word', 'Bet','RT']
                dataFileWriter = csv.DictWriter(dataFile, lineterminator='\n', fieldnames = fieldnames)
                dataFileWriter.writeheader()
                try:
                    print bet
                    if bet.isnumeric() == True: #if they did enter a bet, add this row
                        i +=1
                        already = True
                        global dataFileWriter
                        dataFileWriter.writerow({'Subject': expInfo['Subject'], 'Session': expInfo['Session'],'Round': round,\
                        'Word': words[i-1],'Bet':bet.encode("ascii"),'RT': RT})
                except AttributeError: #else repeat
                    i = i
                    already = False
                    print "blank entered2"
                    continue
                dataFile.close()
    instructions[2].draw()#change this eventually to say "prepare for recall" or something
    mywin.flip()
    core.wait(3)
    wordList = './words/words%i.txt' %(round)
    l = list(cor for cor in open(wordList).read().split("\n") if cor)#repopulate list because for some reason it was loading as a function
    global scoreYet #I might not need this
    event.clearEvents()#clear previous key presses so the below loop runs
    while event.getKeys(keyList=['return'])==[]:#draw window to recall words
        instructions2[1].draw()
        mywin.flip()
    scoreYet = False #so that this loop works past round 1
    while scoreYet == False:
        a = WaitForKeyInput2() #get text
        wordsTheyRecalled.append(a) #add word they typed to a list of words they Recalled
        if wordsTheyRecalled == []: scoreYet = False #don't let them go if they haven't done anything!
    round += 1
    return wordsTheyRecalled
def fScore():
    global score
    wordsToScore = wordsTheyRecalled
    wordList = './words/words%i.txt' %(round-1)
    throwAwayWords = list(cor for cor in open(wordList).read().split("\n") if cor)
    print "WORDS THEY RECALLED"
    print wordsTheyRecalled
    print "ORIGINAL"
    print throwAwayWords
    for w in wordsToScore:
        instructions2[2].draw()
        mywin.flip()
        core.wait(0.1)
        if w in throwAwayWords:
            risk = int(findBet(w))
            throwAwayWords.remove(w)
            score += risk
            writeToDataFile(scorefileName,w,risk,score)
            print score
        correctedWord = correct(w)
        if correctedWord != w:
            while event.getKeys(keyList=['return'])==[]:
                global corrects
                misspelled = visual.TextStim(mywin, height=30,text=w,color="white",pos=(-300,0))
                didYouMean = visual.TextStim(mywin, height=30,text=correctedWord,color="white",pos=(300, 0))
                ask = visual.TextStim(mywin, height=45,text='Did you mean:',color="white",pos=(0, 0))
                how = visual.TextStim(mywin, height=30,text='press y for Yes or n for No',color="white",pos=(0, -200))
                instructions[2].draw()
                misspelled.draw()
                didYouMean.draw()
                ask.draw()
                how.draw()
                mywin.flip()
                event.clearEvents()
                corrects = WaitForMouseInput()
                print "DID THEY CHANGE?"
                print corrects + "in loop"
                if corrects == "yes":
                    if correctedWord in throwAwayWords:
                        risk = int(findBet(correctedWord))
                        throwAwayWords.remove(correctedWord)
                        score += risk
                        writeToDataFile(scorefileName,correctedWord,risk,score)
                        print score
                    else:
                        continue
    for w in throwAwayWords:
        risk = int(findBet(w))
        score -= risk
        writeToDataFile(scorefileName,w,risk,score)
        print score
    questions.draw()
    #THIS IS WHERE THE FEEDBACK GOES
    t = visual.TextStim(mywin, height=36,text="Your current score: ",color="white",pos=(-150,-100))
    doing = visual.TextStim(mywin, height=36,text=score,color="white",pos=(150,-100))
    t.draw()
    doing.draw()
    mywin.flip()
    core.wait(4)
    return score
#----------------------------------------------------------------------------------------
#Spelling Corrector----------------------------------------------------------------------

def words(text): return re.findall('[a-z]+', text.lower())
def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('./Reference/big.txt').read()))
alphabet = 'abcdefghijklmnopqrstuvwxyz'
def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)
def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)
#--------------------------------------------------------------------------------------------
#Run-(how is it possible that such a large program can come down to two functions...idk)-----

for x in range(0,4):
    k = RunBlock()
    s = fScore()
    wordsTheyRecalled= [] #hopefully this makes it so that it doesnt show the old words

