import random
from sbmax_stage import *

def generate_stage(code=''):
    notes = []
    if code == 'Hyomin':
        for i in range(5,800):
            n = random.randrange(0,4)
            notes.append(Note(row=n, target=float(i)/2))
            if random.randrange(0,1) == 0:
                notes.append(Note(row=(n+1) % 4, target=float(i)/2))
                if random.randrange(0,1) == 0:
                    notes.append(Note(row=(n+3) % 4, target=float(i)/2))

    if code == 'Eunsu':
        for i in range(5,800):
            n = random.randrange(0,4)
            notes.append(Note(row=n, target=float(i)))
            if random.randrange(0,5) == 0:
                notes.append(Note(row=(n+1) % 4, target=float(i)+0.5))

    else:
        for i in range(5,800):
            n = random.randrange(0,4)
            notes.append(Note(row=n, target=float(i)))
            if random.randrange(0,3) == 0:
                notes.append(Note(row=(n+1) % 4, target=float(i)))
                if random.randrange(0,2) == 0:
                    notes.append(Note(row=(n+3) % 4, target=float(i)/2))
    
    return notes