from cmu_112_graphics import *
import random
from dataclasses import make_dataclass
import math

def make2dList(rows, cols):
    return [ ([None] * cols) for row in range(rows) ]

Orb = make_dataclass('Orb', ['cx', 'cy', 'r', 'color', 'row', 'col'])

class Unit(object):
    def __init__(self, element, type, image, HP, ATK, DEF, KI):
        self.element = element
        self.type = type
        self.image = image
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF
        self.KI = KI

# Color Wheel (for advan) and Inverse Color Wheel (for disad)
    # PHY->0, INT->1, TEQ->2, AGL->3, STR->4
colorWheel = {0:1, 1:2, 2:3, 3:4, 4:0}
inverseColorWheel = {0:4, 4:3, 3:2, 2:1, 1:0}

# Your Team (stats from dbz.space) (images from Dokkan Battle Wiki)
ssj4Goku = Unit("Super", ("STR", 4), "ssj4_goku.png", 16333, 2205, 840, 0)
superGogeta = Unit("Super", ("INT", 1), "super gogeta.png", 15695, 2292, 862, 0)
ssj3Goku = Unit("Super", ("TEQ", 2), "ssj3 goku.png", 15225, 2266, 884, 0)
gotenks = Unit("Super", ("PHY", 0), "gotenks.png", 15900, 2188, 992, 0)
ssjVegito = Unit("Super", ("AGL", 3), "ssjvegito.png", 15750, 2319, 928, 0)
dbsGogeta = Unit("Super", ("AGL", 3), "dbs gogeta.png", 15745, 2299, 1073, 0)
uiGoku = Unit("Super", ("INT", 1), "uigoku.png", 15335, 2282, 1080, 0)

# Enemy Team (stats from dbz.space) (images from Dokkan Battle Wiki)
Cooler = Unit("Extreme", ("PHY", 0), "cooler_phy.png", 16525, 2196, 927, 0)
kidBuu = Unit("Extreme", ("INT", 1), "kid_buu.png", 16875, 2170, 894, 0)
super17 = Unit("Extreme", ("AGL", 3), "super_17.png", 16225, 2118, 2, 0)
ssj3Broly = Unit("Extreme", ("TEQ", 2), "ssj3 broly.png", 14850, 2257, 927, 0)
janemba = Unit("Extreme", ("STR", 4), "janemba.png", 16333, 2098, 963, 0)
rose = Unit("Extreme", ("STR", 4), "rose.png", 15875, 2270, 1133, 0)
majinVegeta = Unit("Extreme", ("STR", 4), "majin vegeta.png",12727,2700,1029,0)

enemy = [Cooler, kidBuu, super17, ssj3Broly, janemba, rose, majinVegeta]
you = [ssj4Goku, superGogeta, ssj3Goku, gotenks, ssjVegito, dbsGogeta, uiGoku]

###############
# Main App
def distance(x0, y0, x1, y1):
    return math.sqrt((x0-x1)**2+(y0-y1)**2)

def appStarted(app):
    app.order = None
    app.team = False
    app.selectChar = None
    app.switchWith = None
    app.switch = False
    app.switchChar = None
    app.attacked = None
    app.mode = 'start'
    app.extraOrbs = None
    app.attack = False
    app.turn = 0
    app.next = False # False: CPU goes, True: You will go
    app.selected = False
    app.orbSelect = None
    app.drawLines = False
    app.bestPath = []
    app.score = 0
    app.cR = 60
    app.image1 = app.loadImage('dokkan_bg1.jpg')
    app.image2 = app.scaleImage(app.image1, 2/3)
    app.image3 = app.loadImage('bg1.png')
    app.image4 = app.scaleImage(app.image3, 3/4)
    app.arrowI = app.loadImage('arrow.png')
    app.arrow1 = app.scaleImage(app.arrowI, 1/6)
    app.arrowI2 = app.loadImage('arrow2.png')
    app.arrow2 = app.scaleImage(app.arrowI2, 1/6)
    app.wheelI = app.loadImage('All_types_squash.png')
    app.wheel = app.scaleImage(app.wheelI, 1/2)
    app.nimbusI = app.loadImage('nimbus.png')
    app.nimbus = app.scaleImage(app.nimbusI, 1/2)
    #######
    #test for card images
        # will probably take a randomized list of the order of the team
        # and load each image from there (rather than hard code it)
    app.ssj4GokuImage = app.loadImage(ssj4Goku.image)
    app.ssj4GokuI = app.scaleImage(app.ssj4GokuImage, 1/4)
    app.ssj3GokuImage = app.loadImage(ssj3Goku.image)
    app.ssj3GokuI = app.scaleImage(app.ssj3GokuImage, 1/4)
    app.superGogetaImage = app.loadImage(superGogeta.image)
    app.superGogetaI = app.scaleImage(app.superGogetaImage, 1/4)
    app.uiGokuImage = app.loadImage(uiGoku.image)
    app.uiGokuI = app.scaleImage(app.uiGokuImage, 1/4)
    app.gotenksImage = app.loadImage(gotenks.image)
    app.gotenksI = app.scaleImage(app.gotenksImage, 1/4)
    app.ssjVegitoImage = app.loadImage(ssjVegito.image)
    app.ssjVegitoI = app.scaleImage(app.ssjVegitoImage, 1/4)
    app.dbsGogetaImage = app.loadImage(dbsGogeta.image)
    app.dbsGogetaI = app.scaleImage(app.dbsGogetaImage, 1/4)
    app.team1 = [(ssj4Goku, app.ssj4GokuI), (ssj3Goku, app.ssj3GokuI),
    (superGogeta, app.superGogetaI), (uiGoku, app.uiGokuI),
    (gotenks, app.gotenksI), (ssjVegito, app.ssjVegitoI),
    (dbsGogeta, app.dbsGogetaI)]

    app.CoolerImage = app.loadImage(Cooler.image)
    app.CoolerI = app.scaleImage(app.CoolerImage, 1/4)
    app.kidBuuImage = app.loadImage(kidBuu.image)
    app.kidBuuI = app.scaleImage(app.kidBuuImage, 1/4)
    app.super17Image = app.loadImage(super17.image)
    app.super17I = app.scaleImage(app.super17Image, 1/4)
    app.ssj3BrolyImage = app.loadImage(ssj3Broly.image)
    app.ssj3BrolyI = app.scaleImage(app.ssj3BrolyImage, 1/4)
    app.janembaImage = app.loadImage(janemba.image)
    app.janembaI = app.scaleImage(app.janembaImage, 1/4)
    app.roseImage = app.loadImage(rose.image)
    app.roseI = app.scaleImage(app.roseImage, 1/4)
    app.majinVegetaImage = app.loadImage(majinVegeta.image)
    app.majinVegetaI = app.scaleImage(app.majinVegetaImage, 1/4)
    app.team2 = [(Cooler, app.CoolerI), (kidBuu, app.kidBuuI),
    (super17,app.super17I),(ssj3Broly,app.ssj3BrolyI),(janemba,app.janembaI),
    (rose, app.roseI),(majinVegeta, app.majinVegetaI)]
    ######
    app.enemy = random.sample(app.team2, len(app.team2))
    app.you = random.sample(app.team1, len(app.team1))
    app.rows = 5
    app.cols = 5
    app.cellSize = 30
    app.space = 30
    app.margin = (app.width/2) - (3*app.cellSize)
    app.advan = colorWheel
    app.disad = inverseColorWheel
    app.orbColors = [ "orange","purple","green","blue","red"]
    app.board = make2dList(app.rows,app.cols)
    orbBoard(app)

# most of the board stuff is a modified version of the board from Tetris
def orbBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == None:
                randColor = random.choice(app.orbColors)
                cx,cy,r = orbDimensions(app, row, col)
                newOrb = Orb(cx,cy,r,randColor, row, col)
                app.board[row][col] = newOrb

def drawBoard(app, canvas):
    canvas.create_text(90, app.height/2, text=f"Ki Obtained: {app.score}")
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            orb = app.board[row][col]
            canvas.create_oval(orb.cx-orb.r,orb.cy-orb.r,
                                orb.cx+orb.r,orb.cy+orb.r, fill = orb.color)
    # where the rotations are located (change from grey squares at some point)
    canvas.create_rectangle(0,0,app.width,app.height/5, fill='grey')
    canvas.create_rectangle(0,app.height-150,app.width,app.height, fill='grey')
    # color wheel
    canvas.create_image(75, (app.height/5)+80,
                            image=ImageTk.PhotoImage(app.wheel))
    # see your's and the enemy's team order
    canvas.create_rectangle(0, app.height-200, (app.width/3)-90, app.height-150,
                            fill='blue')
    canvas.create_text(43, app.height-175, text='Your Team', fill='red',
                        font='Arial 10 bold')
    
def drawUnits(app, canvas):
    # where the enemy's character images will be (top)
    canvas.create_oval(((app.width/3)-90)-app.cR,(((app.height/5)/2)-7)-app.cR,
                        ((app.width/3)-90)+app.cR,(((app.height/5)/2)-7)+app.cR,
                            fill='red')
    canvas.create_image((app.width/3)-90,((app.height/5)/2)-7,
                            image=ImageTk.PhotoImage(app.enemy[0][1]))
    canvas.create_text((app.width/3)-90, (app.height/5)-12,
                        text=app.enemy[0][0].HP, font="Arial 12 bold")
                    #########
    canvas.create_oval(((2*app.width/3)-90)-app.cR,(((app.height/5)/2)-7)-app.cR,
                    ((2*app.width/3)-90)+app.cR,(((app.height/5)/2)-7)+app.cR,
                            fill='red')
    canvas.create_image((2*app.width/3)-90,((app.height/5)/2)-7,
                            image=ImageTk.PhotoImage(app.enemy[1][1]))
    canvas.create_text((2*app.width/3)-90, (app.height/5)-12,
                        text=app.enemy[1][0].HP, font="Arial 12 bold")
                    #########
    canvas.create_oval(((app.width)-90)-app.cR,(((app.height/5)/2)-7)-app.cR,
                        ((app.width)-90)+app.cR,(((app.height/5)/2)-7)+app.cR,
                            fill='red')
    canvas.create_image((app.width)-90,((app.height/5)/2)-7,
                            image=ImageTk.PhotoImage(app.enemy[2][1]))
    canvas.create_text((app.width)-90, (app.height/5)-12,
                        text=app.enemy[2][0].HP, font="Arial 12 bold")
    # where the player's character images will be (bottom)
    canvas.create_oval(((app.width/3)-90)-app.cR,((app.height/10)+633)-app.cR,
                        ((app.width/3)-90)+app.cR,((app.height/10)+633)+app.cR,
                            fill='blue')
    canvas.create_image((app.width/3)-90,((app.height/5)/2)+633,
                            image=ImageTk.PhotoImage(app.you[0][1]))
    canvas.create_text((app.width/3)-90, app.height-10, text=app.you[0][0].HP,
                            font='Arial 12 bold')
                    #########
    canvas.create_oval(((2*app.width/3)-90)-app.cR,((app.height/10)+633)-app.cR,
                    ((2*app.width/3)-90)+app.cR,((app.height/10)+633)+app.cR,
                            fill='blue')
    canvas.create_image((2*app.width/3)-90,((app.height/5)/2)+633,
                            image=ImageTk.PhotoImage(app.you[1][1]))
    canvas.create_text((2*app.width/3)-90, app.height-10, text=app.you[1][0].HP,
                            font='Arial 12 bold')
                    #########
    canvas.create_oval(((app.width)-90)-app.cR,((app.height/10)+633)-app.cR,
                        ((app.width)-90)+app.cR,((app.height/10)+633)+app.cR,
                            fill='blue')
    canvas.create_image((app.width)-90,((app.height/5)/2)+633,
                            image=ImageTk.PhotoImage(app.you[2][1]))
    canvas.create_text(app.width-90, app.height-10, text=app.you[2][0].HP,
                            font='Arial 12 bold')

def drawAttackPhase(app, canvas):
    canvas.create_rectangle(0, app.height/5, app.width, app.height-150,
                                fill='black')
    canvas.create_text(app.width/2, app.height/2, text='Attack Phase!!!',
                        font='Arial 30 bold', fill='red')
    canvas.create_image(75, (app.height/5)+80,
                            image=ImageTk.PhotoImage(app.wheel))
    if not app.next:
        canvas.create_image(((app.turn+1)*app.width/3)-90, (app.height/5)+60,
                                image=ImageTk.PhotoImage(app.arrow1))
    elif app.next:
        canvas.create_image(((app.turn+1)*app.width/3)-90, app.height-200,
                                image=ImageTk.PhotoImage(app.arrow2))

def addKi(app):
    while (app.turn < 3) and app.selected:
        if not app.next:
            app.enemy[app.turn][0].KI = app.score
        elif app.next:
            app.you[app.turn][0].KI = app.score
        app.selected = False
    
# drawKi is a version of the clock drawing from the notes
# https://www.cs.cmu.edu/~112/notes/notes-graphics.html
def drawKi(app, canvas):
    r = app.cR * 0.8
    cr = 5
    turn_e = 1
    turn_y = 1
    cy_e = (app.height/5)/2
    cy_y = cy_e + 645
    for char in range(len(app.enemy)):
        cx = ((turn_e*app.width)/3)-90
        for ki in range(app.enemy[char][0].KI):
            kiAngle = math.pi/2 - (2*math.pi)*(ki/12)
            kiX = cx + r * math.cos(kiAngle)
            kiY = cy_e - r * math.sin(kiAngle)
            canvas.create_oval(kiX-cr, (kiY-10)-cr, 
                                    kiX+cr, (kiY-10)+cr, fill='yellow')
        turn_e += 1
    for char in range(len(app.you)):
        cx = ((turn_y*app.width)/3)-90
        for ki in range(app.you[char][0].KI):
            kiAngle = math.pi/2 - (2*math.pi)*(ki/12)
            kiX = cx + r * math.cos(kiAngle)
            kiY = cy_y - r * math.sin(kiAngle)
            canvas.create_oval(kiX-cr, (kiY-10)-cr, 
                                kiX+cr, (kiY-10)+cr, fill='yellow')
        turn_y += 1

def orbDimensions(app, row, col):
    x0 = (col*app.cellSize) + app.margin + (col*app.space) - 40
    y0 = (row*app.cellSize) + app.margin + (row*app.space) + 50
    x1 = ((col+1)*app.cellSize) + app.margin + (col*app.space) - 40
    y1 = ((row+1)*app.cellSize) + app.margin + (row*app.space) + 50
    r = x1 - x0
    cx = x0 + r
    cy = y0 + r
    return cx,cy,r

# All of the orb search functions and isOrbLegal was thought up with the
# Knights Tour question from HW 10 in mind
def isOrbLegal(app, row, col, dcol):
    startDot = app.board[row+1][col]
    nextCol = col + dcol
    if ((row < 0) or 
        (nextCol < 0) or (nextCol > len(app.board[0])-1) or
        (startDot.color != app.board[row][nextCol].color)):
        return False
    return True

def orbSearchHelper(app, row, col):
    bestScore = None
    bestDot = None
    for dcol in [-1,0,1]:
        if isOrbLegal(app, row-1, col, dcol):
            score, bestPath = orbSearch(app, row-1, col+dcol)
            extraScore = orbSearchRow(app, row-1, col+dcol)
            score = score + extraScore + 1
            if bestScore == None or score > bestScore:
                bestScore = score
                bestDot = app.board[row-1][col+dcol]
    if bestDot != None:
        return score, [bestDot] + bestPath
    elif bestDot == None:
        return (1, [])

def orbSearch(app, row, col):
    return orbSearchHelper(app, row, col)

def orbSearchRow(app, row, col):
    extraScore = 0
    for left in range(col-1, -1, -1):
        if (app.board[row][left].color == app.board[row][col].color):
            extraScore += 1
        else:
            break
    for right in range(col+1, 5):
        if (app.board[row][right].color == app.board[row][col].color):
            extraScore += 1
        else:
            break
    return extraScore

def selectExtraOrbs(app):
    extraOrbs = []
    for orb in range(len(app.bestPath)):
        row = app.bestPath[orb].row
        col = app.bestPath[orb].col
        for left in range(col-1, -1, -1):
            if (app.board[row][left].color == app.board[row][col].color):
                extraOrbs.append(app.board[row][left])
            else:
                break
        for right in range(col+1, 5):
            if (app.board[row][right].color == app.board[row][col].color):
                extraOrbs.append(app.board[row][right])
            else:
                break
    return extraOrbs

def drawExtraOrbs(app, canvas):
    if app.extraOrbs != None:
        for orb in range(len(app.extraOrbs)):
            cx = app.extraOrbs[orb].cx
            cy = app.extraOrbs[orb].cy
            r = app.extraOrbs[orb].r
            color = app.extraOrbs[orb].color
            canvas.create_oval(cx-r, cy-r, cx+r, cy+r, 
                                    fill=color, width=5)

def drawPath(app, canvas):
    for orb in range(len(app.bestPath)-1):
        startOrb = app.bestPath[orb]
        endOrb = app.bestPath[orb+1]
        canvas.create_line(startOrb.cx,startOrb.cy,endOrb.cx,endOrb.cy,
                                width=5)

def collectOrbs(app):
    for row in range(len(app.board)):
            for col in range(len(app.board[0])):
                if ((app.board[row][col] in app.bestPath) or
                    (app.board[row][col] in app.extraOrbs)):
                    app.board[row][col] = None

# Great video that helped me wrap my head around the minimax shenanigans
# https://youtu.be/l-hh51ncgDI
def minimax(app, depth, isMaxPlayer, state=0):
    if depth == 0:
        app.attacked = state
        damage = calculateDamage(app, True)
        hp = app.you[app.attacked][0].HP
        if hp - damage <= 0:
            return (1, damage)
        return (0, damage)
        
    if not isMaxPlayer:
        target = None # Some score that will never happen
        for i in range(3): # 3 possible characters to attack
            app.attacked = i
            damage = calculateDamage(app)
            hp = app.you[app.attacked][0].HP
            if hp <= 0:
                continue
            score = minimax(app, depth - 1, i, True)
            if (score[0] == 1) and (hp - damage <= 0) and (i >= app.turn):
                target = (i, damage)
                return target
            elif (hp - damage <= 0) and (score[0] == 1):
                target = (i, damage)
            elif (hp - damage <= 0):
                target = (i, damage)
            elif target == None or score[1] > target[1]:
                target = (i, damage)
        return target

    if isMaxPlayer:
        target = None # Some score that will never happen
        for i in range(3): # 3 possible characters to attack
            score = minimax(app, depth - 1, i, False)
            if (score[0] == 1) and (i > app.turn):
                target = score
            elif score[0] == 1:
                target = score
            elif target == None or score[1] > target[1]:
                target = score
        return target

# Damage equation from this reddit post:
# https://www.reddit.com/r/DBZDokkanBattle/comments/d3cakb/how_defense_works_in_dokkan_battle_complete_guide/
def calculateDamage(app, hypo=False):
    # TAKEN DAMAGE = (X-DEF)*Y
    if not app.next and not hypo:
        attacker = app.enemy[app.turn][0]
        attacked = app.you[app.attacked][0]
    elif app.next or hypo:
        attacker = app.you[app.turn][0]
        attacked = app.enemy[app.attacked][0]
    atkr = (attacker.DEF, attacker.type[1])
    atkd = (attacked.DEF, attacked.type[1])
    atkdStrong = app.advan.get(atkd[1], None)
    atkdWeak = app.disad.get(atkd[1], None)
    if atkr[1] == atkdStrong:
        Y = 0.5
    elif atkr[1] == atkdWeak:
        Y = 1.5
    else:
        Y = 1
    if attacker.KI == 12:
        attack = attacker.ATK * 2
    else:
        attack = attacker.ATK
    damage = (attack - atkd[0]) * Y
    return damage

def checkForWin(app):
    enemyWin = True
    youWin = True
    for char1 in range(len(app.enemy)):
        if app.enemy[char1][0].HP >= 0:
            youWin = False
            break
    for char2 in range(len(app.you)):
        if app.you[char2][0].HP >= 0:
            enemyWin = False
            break
    if enemyWin or youWin:
        if enemyWin:
            return 1 # 1 means the enemy has won
        elif youWin:
            return 0 # 0 means you have won
    return None

def switchCharacter(app):
    char = app.you.pop(app.switchChar)
    app.you.insert((app.switchWith), char)

def drawSwitch(app, canvas):
    canvas.create_oval((((app.selectChar+1)*app.width/3)-90)-app.cR,
    ((app.height/10)+633)-app.cR, (((app.selectChar+1)*app.width/3)-90)+app.cR,
        ((app.height/10)+633)+app.cR, width=5)

def drawTeamOrder(app, canvas):
    i = 50
    canvas.create_rectangle(0, app.height/5, app.width, app.height-150,
                        fill='black')
    for char in app.you:
        canvas.create_image(i, app.height/2, 
                    image=ImageTk.PhotoImage(char[1]))
        i += 72
    canvas.create_rectangle(0, app.height-200, (app.width/3)-90, app.height-150,
                            fill='blue')
    canvas.create_text(43, app.height-175, text='Back', fill='red',
                        font='Arial 10 bold')
################

################
# Start Mode
def start_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2,
                                image=ImageTk.PhotoImage(app.image4))
    canvas.create_rectangle((app.width/2)-100, (app.height/2)+100,
                            (app.width/2)+100, (app.height/2)+250, fill='red')
    canvas.create_text(app.width/2, (app.height/2)+175, fill='blue',
                    text="Click Here To Start!", font='Arial 15')
    canvas.create_image(app.width/2, (app.height/2)-150,
                                image=ImageTk.PhotoImage(app.nimbusI))
    canvas.create_text((app.width/2)-50, (app.height/2)-180, text='DBZ:',
                        font='Arial 20', fill='red')
    canvas.create_text((app.width/2)-50,(app.height/2)-150,text='112 Battle!!!',
                        font='Arial 20', fill='red')

def start_mousePressed(app, event):
    if (distance(event.x, event.y, (app.width/2), (app.height/2)+175) < 125):
        app.mode = 'pick'

#################

#################
# Pick Mode
def pick_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2,
                                image=ImageTk.PhotoImage(app.image4))
    canvas.create_rectangle((app.width/2)-100, (app.height/2)+100,
                            (app.width/2)+100, (app.height/2)+250, fill='red')
    canvas.create_rectangle((app.width/2)-100, (app.height/2)-150,
                            (app.width/2)+100, (app.height/2), fill='red')
    canvas.create_text(app.width/2, (app.height/2)-75, fill='blue',
                    text="Team 1", font='Arial 15')
    canvas.create_text(app.width/2, (app.height/2)+175, fill='blue',
                    text="Team 2", font='Arial 15')

def pick_mousePressed(app, event):
    if (distance(event.x, event.y, (app.width/2), (app.height/2)+170) < 100):
        app.enemy = random.sample(app.team1, len(app.team1))
        app.you = random.sample(app.team2, len(app.team2))
        app.mode = 'game'
    elif (distance(event.x, event.y, (app.width/2), (app.height/2)-75) < 100):
        app.enemy = random.sample(app.team2, len(app.team2))
        app.you = random.sample(app.team1, len(app.team1))
        app.mode = 'game'
#################

#################
# Win Mode
def win_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2,
                                image=ImageTk.PhotoImage(app.image4))
    canvas.create_rectangle((app.width/2)-100, (app.height/2)+100,
                            (app.width/2)+100, (app.height/2)+250, fill='red')
    canvas.create_text(app.width/2, (app.height/2)+175, fill='blue',
                    text="Back to Start!", font='Arial 15')
    if app.win == 1:
        canvas.create_text(app.width/2, app.height/2, text='The Enemy Wins!!!',
                    font='Arial 25 bold', fill='red')
    if app.win == 0:
        canvas.create_text(app.width/2, app.height/2, text='You Win!!!',
                    font='Arial 25 bold', fill='green')

def win_mousePressed(app, event):
    if (distance(event.x, event.y, (app.width/2), (app.height/2)+170) < 100):
        appStarted(app)
        app.mode = 'start'
#################

#################
# Game Mode
def game_mouseDragged(app, event):
    if app.switchChar != None:
        for i in range(3):
            if i == app.switchChar:
                continue
            if ((distance(event.x,event.y,((i+1)*app.width/3)-90,
                (app.height/10)+633) < app.cR) and app.turn):
                char = app.you.pop(app.switchChar)
                if i == 0:
                    app.you.insert(0, char)
                elif i == 1:
                    app.you.insert(1, char)
                elif i == 2:
                    app.you.append(char)
    for j in range(len(app.board[0])):
        if (distance(event.x,event.y,app.board[4][j].cx,app.board[4][j].cy) 
                                < app.board[4][j].r):
            app.orbSelect = j
            app.score, app.bestPath = orbSearch(app, 4, j)
            extraScore = orbSearchRow(app, 4, j)
            app.score += extraScore
            app.bestPath.insert(0, app.board[4][j])
            app.extraOrbs = selectExtraOrbs(app)
            app.drawLines = True

def game_mouseReleased(app, event):
    if not app.attack:
        if app.orbSelect != None:
            collectOrbs(app)
            app.selected = True
            addKi(app)
            orbBoard(app)
            app.bestPath = []
            app.orbSelect = None
            app.extraOrbs = None
            app.drawlines = False
            app.turn += 1
            if app.turn == 3:
                app.turn = 0
                app.attack = True
            app.next = False
    elif app.attack:
        if app.turn > 2:
            for _ in range(3):
                char = app.enemy.pop(0)
                app.enemy.append(char)
        win = checkForWin(app)
        if win == 1:
            app.win = 1
            app.mode = 'win'
        if win == 0:
            app.win = 0
            app.mode = 'win'

def game_mousePressed(app, event):
    if not app.switch and not app.attack and not app.team:
        for i in range(3):
            if ((distance(event.x,event.y,((i+1)*app.width/3)-90,
                (app.height/10)+633) < app.cR) and app.next):
                app.switchChar = i
                app.selectChar = i
                app.switch = True
    if app.switch:
        for i in range(3):
            if ((distance(event.x,event.y,((i+1)*app.width/3)-90,
                (app.height/10)+633) < app.cR) and app.next and 
                i != app.switchChar):
                app.switchWith = i
                switchCharacter(app)
                app.switch = False
    if not app.attack and not app.switch and not app.team:
        for j in range(len(app.board[0])):
            if (distance(event.x,event.y,app.board[4][j].cx,app.board[4][j].cy) 
                                    < app.board[4][j].r):
                app.orbSelect = j
                app.score, app.bestPath = orbSearch(app, 4, j)
                extraScore = orbSearchRow(app, 4, j)
                app.score += extraScore
                app.bestPath.insert(0, app.board[4][j])
                app.extraOrbs = selectExtraOrbs(app)
                app.drawLines = True
        if ((event.x > 0) and (event.x < (app.width/3)-90) and
            (event.y > app.height-200) and (event.y < app.height-150)):
            app.team = True
    elif app.team:
        if ((event.x > 0) and (event.x < (app.width/3)-90) and
            (event.y > app.height-200) and (event.y < app.height-150)):
            app.team = False
    elif app.attack:
        if app.next:
            y = (app.height/10) - 7
            for char in range(3):
                if (distance(event.x, event.y,
                ((char+1)*app.width/3)-90, y) < app.cR):
                    app.attacked = char
                    damage = calculateDamage(app)
                    app.enemy[char][0].HP -= damage
                    app.next = False
                    app.turn += 1
        if app.turn == 3:
            app.turn = 0
            app.attack = False
            for char in range(3):
                app.enemy[char][0].KI = 0
                app.you[char][0].KI = 0
            for _ in range(3):
                char_e = app.enemy.pop(0)
                app.enemy.append(char_e)
                char_y = app.you.pop(0)
                app.you.append(char_y)

def game_mouseMoved(app, event):
    if app.switch:
        for i in range(3):
            if ((distance(event.x,event.y,((i+1)*app.width/3)-90,
            (app.height/10)+633) < app.cR)):
                app.selectChar = i

def game_timerFired(app):
    # simulate a whole turn if it is the CPU's turn
    if not app.next and not app.attack:
        bestPath = None
        bestScore = None
        bestIndex = -1
        for j in range(len(app.board[0])):
            score, currCompPath = orbSearch(app, 4, j)
            if bestScore == None or score > bestScore:
                bestPath = currCompPath
                bestScore = score
                bestIndex = j
        app.score = bestScore
        app.bestPath = bestPath
        app.orbSelect = bestIndex
        app.bestPath.insert(0, app.board[4][bestIndex])
        app.extraOrbs = selectExtraOrbs(app)
        app.drawLines = True
        collectOrbs(app)
        app.selected = True
        addKi(app)
        orbBoard(app)
        app.bestPath = []
        app.orbSelect = None
        app.extraOrbs = None
        app.drawlines = False
        app.next = True
    elif app.attack and not app.next:
        if not app.next:
            target = minimax(app, 2, False)
            app.attacked = target[0]
            damage = calculateDamage(app)
            app.you[app.attacked][0].HP -= damage
            win = checkForWin(app)
        if win == 1:
            app.win = 1
            app.mode = 'win'
        if win == 0:
            app.win = 0
            app.mode = 'win'
        app.next = True

def game_redrawAll(app, canvas):
    canvas.create_image(250, 350, 
                            image=ImageTk.PhotoImage(app.image2))             
    drawBoard(app, canvas)
    drawUnits(app,canvas)
    if app.switch:
        drawSwitch(app, canvas)
    if app.drawLines:
        drawPath(app, canvas)
        drawExtraOrbs(app, canvas)
    drawKi(app, canvas)
    if app.team:
        drawTeamOrder(app, canvas)
    if app.attack:
        drawAttackPhase(app, canvas)
    

runApp(width=528, height=792)