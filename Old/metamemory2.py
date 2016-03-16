#TODO
#make it so the score is per round
#run multiple bloks
#
from psychopy import visual, core, gui, data, misc, event, sound
import time, random
import re, csv, os, os.path, collections
#---------------------------------------------------------------------------------------------------------
#GUI------------------------------------------------------------------------------------------------------
# define experiment parameters
expInfo = {'Subject':'1','Session':'1', 'Version': ['A', 'B']}
expInfo['dateStr'] = time.strftime("%Y_%m_%d_%H%M", time.localtime())

# ask for task parameters
dlg = gui.DlgFromDict(expInfo, title='Meta Memory', fixed=['dateStr'],order=['Subject','Session', 'Version'])
if not dlg.OK: core.quit()
#-------------------------------------------------------------------------------------------------------------
#Define Window and Clock--------------------------------------------------------------------------------------
experimentclock = core.Clock()
trialClock = core.Clock()
mywin = visual.Window([1024,768],allowGUI=True,fullscr=True,monitor="testMonitor",units="pix",color="black")
myMouse = event.Mouse(win=mywin)
#----------------------------------------------------------------------------------------------------------
#Define Variables and lists--------------------------------------------------------------------------------
subject = expInfo['Subject']
session = expInfo['Session']
version = expInfo['Version']
fileName = '%s_%s_score.csv' %(subject,session)
betsFile = '%s_%s_bets.csv' %(subject,session)

round = 1
l = ''#words

score = 0
scoreYet = False
referenceWords = []
wordsTheyRecalled =[]
#-----------------------------------------------------------------------------------------------------------
#Load stuff to reference------------------------------------------------------------------------------------
instructions = []
instructions.append((visual.ImageStim(mywin,pos=[0,0],image='./instructions/prompt.jpg')))
instructions.append((visual.ImageStim(mywin,pos=[0,0],image='./instructions/howto.jpg')))
instructions.append((visual.ImageStim(mywin,pos=[0,0],image='./instructions/scoring.jpg')))


fileName  = '%s_1_score.csv' %(subject) #Maybe change this?

#------------------------------------------------------------------------------------------------------------
#Functions---------------------------------------------------------------------------------------------------
def writeToDataFile(dataFileName,wordToWrite,r,cs):#r is the risk amount variable and cs is the Cumulative Score variable
    print "IVE BEEN CALLED"
    if os.path.exists(dataFileName):
        print "IM CHECKING THE PATH"
        dataFile =open(dataFileName, 'a')
        fieldnames = ['Subject', 'Session', 'Word', 'Points','Cumulative Score']
        datafileWriter = csv.DictWriter(dataFile, lineterminator='\n', fieldnames = fieldnames)
        datafileWriter.writerow({'Subject': expInfo['Subject'], 'Session': expInfo['Session'], 'Word': wordToWrite, 'Points': r, 'Cumulative Score': cs})
        print "WRITE"
        dataFile.close()
        print "CLOSED"
    else:
        with open(dataFileName, 'w') as dataFile:
            print "IM CHECKING THE PATH"
            fieldnames = ['Subject', 'Session', 'Word', 'Points','Cumulative Score']
            dataFileWriter = csv.DictWriter(dataFile, lineterminator='\n', fieldnames = fieldnames)
            dataFileWriter.writeheader()
            datafileWriter.writerow({'Subject': expInfo['Subject'], 'Session': expInfo['Session'], 'Word': wordToWrite, 'Points': r, 'Cumulative Score': cs})
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

def WaitForKeyInput():
    text='...' 
    global scoreYet
    response = visual.TextStim(mywin, height=75,text=text,color="white",pos=(0, 250))
    response.draw()
    instructions[0].draw()
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
            instructions[0].draw()
            populateOldWords()
            response = visual.TextStim(mywin, height=75,text=text,color="white",pos=(0, 250))
            response.draw()
            mywin.flip()
    event.clearEvents()
    return text

def findBet(wordinput):
    if os.path.exists(betsFile):
        dataFileRead=open(betsFile, 'r')
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

def fScore():
    global score
    wordsToScore = wordsTheyRecalled
    throwAwayWords = l
    print "WORDS THEY RECALLED"
    print wordsTheyRecalled
    print "ORIGINAL"
    print throwAwayWords
    for w in wordsToScore:
        instructions[2].draw()
        mywin.flip()
        if w in throwAwayWords:
            risk = int(findBet(w))
            throwAwayWords.remove(w)
            score += risk
            writeToDataFile(fileName,w,risk,score)
            print score
        correctedWord = correct(w)
        if correctedWord != w:
            while event.getKeys(keyList=['return'])==[]:
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
                print corrects
            if corrects == "yes":
                if correctedWord in throwAwayWords:
                    risk = int(findBet(correctedWord))
                    throwAwayWords.remove(correctedWord)
                    score += risk
                    writeToDataFile(fileName,correctedWord,risk,score)
                    print score
    for w in throwAwayWords:
        risk = int(findBet(w))
        score -= risk
        writeToDataFile(fileName,w,risk,score)
        print score
    return score
 
def RunBlock():
    global round
    wordList = './words/words%i.txt' %(round)
    l = list(cor for cor in open(wordList).read().split("\n") if cor)
    global scoreYet
    while event.getKeys(keyList=['return'])==[]:
        instructions[1].draw()
        mywin.flip()
    while scoreYet == False:
        a = WaitForKeyInput() #get text
        wordsTheyRecalled.append(a) #add word they typed to a list of words they Recalled
    round += 1
    return wordsTheyRecalled

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
#Run-----------------------------------------------------------------------------------------
#for i in range(0,11):
k = RunBlock()
s = fScore()
print s
