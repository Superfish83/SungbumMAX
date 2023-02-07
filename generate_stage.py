import random
from sbmax_stage import *

def gen_random(code='', bpm=180, offset=0.0):
    stage = Stage(bpm=bpm, stage_offset=offset)
    if code == 'Hyomin':
        for i in range(4,840):
            n = random.randrange(0,4)
            stage.notes.append(Note(row=n, target=float(i)/2))
            if random.randrange(0,1) == 0:
                stage.notes.append(Note(row=(n+1) % 4, target=float(i)/2))
                if random.randrange(0,1) == 0:
                    stage.notes.append(Note(row=(n+3) % 4, target=float(i)/2))

    elif code == 'Eunsu':
        for i in range(4,420):
            n = random.randrange(0,4)
            stage.notes.append(Note(row=n, target=float(i)))
            if random.randrange(0,5) == 0:
                stage.notes.append(Note(row=(n+1) % 4, target=float(i)+0.5))

    elif code == 'Sungbum':
        for i in range(4,420):
            n = random.randrange(0,4)
            stage.notes.append(Note(row=n, target=float(i)))
            if random.randrange(0,2) == 0:
                stage.notes.append(Note(row=(n+1) % 4, target=float(i)))
                if random.randrange(0,1) == 0:
                    stage.notes.append(Note(row=(n+3) % 4, target=float(i)+0.5))

    else:
        for i in range(4,420):
            n = random.randrange(0,4)
            stage.notes.append(Note(row=n, target=float(i)))
            if random.randrange(0,3) == 0:
                stage.notes.append(Note(row=(n+1) % 4, target=float(i)))
                if random.randrange(0,2) == 0:
                    stage.notes.append(Note(row=(n+3) % 4, target=float(i)+0.5))
    
    stage.length = 420 #음원 길이
    return stage

def gen_stage_from_file(path):
    f = open(path)
    data = f.read()

    bpm = float(data[data.find('<')+1:data.find('>')])
    offset = float(data[data.find('[')+1:data.find(']')])
    stage = Stage(bpm=bpm, stage_offset=offset)

    beats_map = {'!':1.0,'@':0.5,'#':0.25}

    t = 0
    while data.find('-') > 0:
        data = data[data.find('-')+1:].strip()
        
        beat = beats_map[data[0]]
        for i in range(4):
            if data[i+1] == '1':
                stage.notes.append(Note(row=i, target=t))
            elif data[i+1] != '.':
                break
        t += beat

    stage.length = t #음원 길이
    return stage