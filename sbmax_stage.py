import time

class Stage():
    def __init__(self, bpm=60.0, stage_offset=0.0):
        self.notes = []
        self.bpm = bpm
        self.start_time = time.time() + stage_offset
        self.fallv = 280
        self.cur_msg = None
        self.cur_combo = None
        
        self.score = 0
        self.max_life = 5
        self.life = self.max_life

        self.combo = 0

    def get_dtime(self):
        return time.time() - self.start_time

    def get_err_seconds(self, target):
        return ( (target * 60 / self.bpm) - self.get_dtime() )

    def get_dbeat(self): #시작부터 몇 박자 지났는지
        return (time.time() - self.start_time) / 60.0 * self.bpm

    def add_panjeong(self, level):
        msg = None

        target = self.get_dbeat()
        duration = 1.0


        if level <= 2: #Miss 이외의 판정일 때 공통 작업
            self.life = min(self.life+1,self.max_life)
            self.combo += 1
            self.cur_combo = Msg((200,200,150), f"COMBO {self.combo}", target, 3.0, 280)

        
        if level == 0: #Perfect 판정
            color = (220, 220, 100)
            text = "Perfect"
            length = 140
            msg = Msg(color, text, target, duration, length)

            self.score += 2

        elif level == 1: #Slow 판정
            color = (220, 110, 220)
            text = "Slow"
            length = 100
            msg = Msg(color, text, target, duration, length)

            self.score += 1

        elif level == 2: #Fast 판정
            color = (220, 110, 220)
            text = "Fast"
            length = 80
            msg = Msg(color, text, target, duration, length)

            self.score += 1

        elif level == 3: #Miss 판정
            color = (220, 110, 100)
            text = "Miss"
            length = 90
            msg = Msg(color, text, target, duration, length)

            self.life -= 1
            self.combo= 0
        
        self.cur_msg = msg

class Msg():
    def __init__(self, color, text, target, duration, length):
        #target : 표시할 타겟 시간(타이밍)을 의미함
        self.color = color
        self.text = text
        self.target = target
        self.duration = duration
        self.length = length #표시되는 텍스트 길이(픽셀)


class Note():
    def __init__(self, row=0, target=4, duration=0.1):
        #target : 정해진 박자에 해당하는 시간(타이밍)을 의미함
        self.row = row
        self.target = target
        self.duration = duration
        self.do_pj = True #판정 함수에서 판정 대상으로 둘지 결정