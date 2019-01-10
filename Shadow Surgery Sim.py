# -*- coding: utf-8 -*-
"""
Created for the purpose of trying out the shadowborn surgical deck
(C) Ignatius Liu 2018

E = Emrakul
H = Hamilar Depth
X = Surgical Extraction
S = Serum Powder
D = Shelldock Isle
A = Shadowborn Apostle

"""
import csv
import math
from random import shuffle

E, H, X, S, D = 4, 3, 4, 4, 4
A = 60 - E - H - X - S - D

#Rules
max_mull = 3
ex_emra = 3
ex_dock = 3

test_times = 200000
deck = ['E']* E
deck.extend('H' * H)
deck.extend('X' * X)
deck.extend('S' * S)
deck.extend('D' * D)
deck.extend('A' * A)
shuffle(deck)

action = ''

def newDeck():
    global deck
    deck = ['E']* E
    deck.extend('H' * H)
    deck.extend('X' * X)
    deck.extend('S' * S)
    deck.extend('D' * D)
    deck.extend('A' * A)
    shuffle(deck)

def mulligan(hs):
    global deck
    shuffle(deck)
    return hs - 1


"""
ev codes (event codes):
1 = Surgical Found
M = Mulligan
S = Serum (no combo pieces exiled)
E= Emrakul Exiled (from Serum)
D = Shelldock Exiled (from Serum)
B = Emrakul and Shelldock Exiled (from Serum)
0 = Surgical Not found after 2 Mulligan

hs = handsize
"""
def drawHand(ev, hs):
    global deck, ex_emra, ex_dock
    hand = deck[0:hs]
    if 'X' in hand:
        return ev + '1'
    elif 'S' in hand:
        if 'E' in hand and 'D' not in hand and hand.count('E') + ev.count('B') + ev.count('E')< ex_emra:
            deck = deck[hs:]
            return drawHand(ev + 'E', hs)
        elif 'D' in hand and 'E' not in hand and hand.count('D') + ev.count('B') + ev.count('D')< ex_dock:
            deck = deck[hs:]
            return drawHand(ev + 'D', hs)
        elif 'E' in hand and 'D' in hand and hand.count('D') + ev.count('B') + ev.count('D')< ex_dock and hand.count('E') + ev.count('B') + ev.count('E')< ex_emra:
            deck = deck[hs:]
            return drawHand(ev + 'B', hs)
        elif 'E' not in hand and 'D' not in hand:
            deck = deck[hs:]
            return drawHand(ev + 'S', hs)
        else:
            if ev.count('M') < max_mull:
                hs = mulligan(hs)
                return drawHand(ev + 'M', hs)
            else:
                return ev + '0'
    else:
        if ev.count('M') < max_mull:
            hs = mulligan(hs)
            return drawHand(ev + 'M', hs)
        else:
            return ev + '0'
def draw(hand, deck):
    #global action #debugging
    #action += deck[0]
    hand.append(deck[0])
    del deck[0]
def extract(card, deck):
    #global action #debugging
    #action += 'x(' + card + ')'
    deck = [x for x in deck if not x==card]
    shuffle(deck)
    return deck
def shelldock(deck):
    #global action
    #action += 'i'
    succ = False
    if 'E' in deck[:4]:
        del deck[deck.index('E')]
        succ = True
    elif 'S' in deck[:4]:
        del deck[deck.index('S')]
    elif 'X' in deck[:4]:
        del deck[deck.index('X')]
    elif 'H' in deck[:4]:
        del deck[deck.index('H')]
    cards = 3
    while 'S' in deck[:cards]:
        del deck[deck.index('S')]
        deck.append('S')
        cards -= 1
    while 'X' in deck[:cards]:
        del deck[deck.index('X')]
        deck.append('X')
        cards -= 1
    while 'H' in deck[:cards]:
        del deck[deck.index('H')]
        deck.append('H')
        cards -= 1
    return succ
def halimar(hand, deck):
    #global action
    #action += 'h'
    if 'D' not in hand:
        if 'D' in deck[:3]:
            deck[deck.index('D')], deck[0] = deck[0], deck[deck.index('D')]
        elif 'X' in deck[:3]:
            deck[deck.index('X')], deck[0] = deck[0], deck[deck.index('X')]
        elif 'H' in deck[:3]:
            deck[deck.index('H')], deck[0] = deck[0], deck[deck.index('H')]
        elif 'S' in deck[:3]:
            deck[deck.index('S')], deck[0] = deck[0], deck[deck.index('S')]
    else:
        if len(deck)> 1 and deck[0] == 'E' and deck[1] == 'E':
            if len(deck) > 2:
                deck[0], deck[2] = deck[2], deck[0]
        elif len(deck) > 1 and  deck[0] == 'E':
            deck[0], deck[1] = deck[1], deck[0]

def play():
    turn = 1
    board = ''
    global deck
    #global action
    #action = ''
    drew = drawHand("", 7)
    hs = 7 - drew.count('M')
    hand = deck[0:hs]
    deck = deck[hs:]
    while len(hand)<8 or 'A' not in hand or 'X' not in hand:
        draw(hand, deck)
        turn += 1
    del hand[hand.index('A')]
    del hand[hand.index('X')]
    deck = extract('A', deck)
    if 'X' in hand:
        hand = extract('X', hand)
        deck = extract('X', deck)
    while 'H' not in hand and 'D' not in hand:
        draw(hand, deck)
        if 'X' in hand:
            deck = extract('X', deck)
            hand = extract('X', hand)
        turn += 1
        
    if turn > 9:
        return -1
    #E = Successful Emrakul Shelldocked, H = Halimar depth, D = Bad shelldock 
    while board.count('E') < 1:
        if hand.count('E') == 1 and board.count('D') == 1:
            pass
        elif hand.count('E') == 2:
            pass
        if 'H' in hand and board.count('D') == 0:
            del hand[hand.index('H')]
            board+= "H"
            halimar(hand, deck)
        elif 'D' in hand:
            del hand[hand.index('D')]
            if shelldock(deck):
                board+= 'E'
            else:
                board+= 'D'
        elif 'H' in hand and board.count('D') == 1:
            del hand[hand.index('H')]
            board+= "H"
            halimar(hand, deck)
        elif 'X' in hand:
            deck = extract('X', deck)
            hand = extract('X', hand)
        elif 'E' in hand and len(hand) > 7:
            del hand[hand.index("E")]
            deck.append('E')
            shuffle(deck)
        turn += 1
        
        if board.count('D') == 2 or turn > 9:
            return -1
        if len(deck) == 0:
            return -1
        else:
            draw(hand, deck)
    while board.count('E') + board.count('H') + board.count('D') < 2:
        if turn > 9:
            return -1
        if 'H' in hand:
            del hand[hand.index('H')]
            board += 'H'
            turn+= 1
        elif 'D' in hand:
            del hand[hand.index('D')]
            board += 'D'
            turn+= 1
        else:
            if len(deck) > 0:
                draw(hand, deck)
            else:
                return -1
        turn += 1
    if turn > 9:
        return -1
    return turn

def singleTest():
    turns = play()
    newDeck()
    return turns
def test():
    i = 0
    result = []
    tenper = math.floor(test_times/10)
    per = 0
    while i< test_times:
        result.append(play())
        newDeck()
        #"""
        if i > per:
            print(str(per/test_times * 100)[:4] + "%")
            per += tenper
        #"""
        i+= 1
    combi = []
    count = []
    for i in result:
        if i not in combi:
            combi.append(i)
            count.append(1)
        else:
            count[combi.index(i)] += 1
    analysis = []
    for i, c in enumerate(combi):
        analysis.append([c, count[i]])
    analysis.sort()
    #"""
    print("Loses : " + str(analysis[0][1]) + " Times (" + str(round(analysis[0][1]/test_times, 4) * 100)[:7] + "%)")
    for i in analysis[1:]:
        print(str(i[0]) + " Turns : " + str(i[1]) + " Times (" + str(round(i[1]/test_times, 4) * 100)[:7] + "%)")
    #"""
    return [str(round(i[1]/test_times, 4) * 100)[:7] for i in analysis]
        


def analysis():
    numb = [0, 1, 2, 3, 4]
    result = [['E', 'H', 'S', 'D', 'A', 'MM', 'EE', 'ED', 'L', '4', '5', '6', '7', '8', '9']]
    i = 0
    global E, H, S, D, A, max_mull, ex_emra, ex_dock
    for e in numb[1:5]:
        E = e
        for h in numb[0:5]:
            H = h
            for s in numb[0:5]:
                S = s
                for d in numb[1:5]:
                    D = d
                    A = 60 - E - H - 4 - S - D
                    for mm in numb[0:4]:
                        max_mull = mm
                        for ee in numb[0: E]:
                            ex_emra = ee
                            for ed in numb[0: D]:
                                ex_dock = ed
                                tresult = [E, H, S, D, A, max_mull, ex_emra, ex_dock]
                                tresult.extend(test())
                                result.append(tresult)
                                i+= 1
                                if i%100 == 0:
                                    print(i)

    with open('output.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(result)






