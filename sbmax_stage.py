import time

class Stage():
    def __init__(self, bpm=60.0, stage_offset=0.0):
        self.notes = []
        self.bpm = bpm
        self.start_time = time.time() + stage_offset
        self.fallv = 280
        self.cur_msg = None
        
        self.score = 0
        self.max_life = 5
        self.life = self.max_life

    def get_dtime(self):
        return time.time() - self.start_time

    def get_err_seconds(self, target):
        return ( (target * 60 / self.bpm) - self.get_dtime() )

    def get_dbeat(self): #시작부터 몇 박자 지났는지
        return (time.time() - self.start_time) / 60.0 * self.bpm

    def add_panjeong(self, level):
        msg = None

        if level == 0: #Perfect 판정
            color = (220, 220, 100)
            text = "Perfect"
            target = self.get_dbeat()
            duration = 1.0
            msg = Msg(color, text, target, duration)
            self.life = min(self.life+1,self.max_life)
            self.score += 2

        elif level == 1: #Slow 판정
            color = (220, 110, 220)
            text = "Slow"
            target = self.get_dbeat()
            duration = 1.0
            msg = Msg(color, text, target, duration)
            self.life = min(self.life+1,self.max_life)
            self.score += 1

        elif level == 2: #Fast 판정
            color = (220, 110, 220)
            text = "Fast"
            target = self.get_dbeat()
            duration = 1.0
            msg = Msg(color, text, target, duration)
            self.life = min(self.life+1,self.max_life)
            self.score += 1

        elif level == 3: #Miss 판정
            color = (220, 110, 100)
            text = "Miss"
            target = self.get_dbeat()
            duration = 1.0
            msg = Msg(color, text, target, duration)
            self.life -= 1
        
        self.cur_msg = msg

class GameObject():
    def __init__(self, bpm=60.0):
        self.bpm = bpm

class Msg():
    def __init__(self, color, text, target, duration):
        #target : 표시할 타겟 시간(타이밍)을 의미함
        self.color = color
        self.text = text
        self.target = target
        self.duration = duration


class Note(object):
    def __init__(self, row=0, target=4, duration=0.05):
        #target : 정해진 박자에 해당하는 시간(타이밍)을 의미함
        self.row = row
        self.target = target
        self.duration = duration
        self.do_pj = True #판정 함수에서 판정 대상으로 둘지 결정