import pygame
from pygame.locals import *
from pygame import mixer
import random, time
from sbmax_stage import *
from create_stage import *

FPS = 120
FramePerSec = pygame.time.Clock()
pygame.init()
mixer.init()

SCREEN_H, SCREEN_V, NOTE_W, PAD_H = 800, 600, 100, 520
GameDisplay = pygame.display.set_mode((SCREEN_H, SCREEN_V))
pygame.display.set_caption("SungbumMAX")
font = pygame.font.SysFont('NanumGothic', 20)  # 기본 폰트 및 사이즈 설정
font_pj = pygame.font.SysFont('NanumGothicBold', 44)  # 판정용 폰트
font_title = pygame.font.SysFont('NanumGothicBold', 35)  # 타이틀 폰트

#-------▲--Initial Settings/Constants------
#-------▼---------Game Code----------------

def draw_note(stage, note):
    global GameDisplay, SCREEN_H, SCREEN_V, NOTE_W, PAD_H
    note_w = NOTE_W
    note_h = note.duration * stage.fallv

    note_x = (SCREEN_H / 2) + note_w * (note.row-2)
    note_y = (stage.get_dbeat() - note.target) * stage.fallv \
         + PAD_H - note_h

    if note_y + note_h < 0 or note_y > SCREEN_V:
        return

    color = (200,200,200)
    if note.do_pj == False:
        color = (50,50,50)

    pygame.draw.rect(GameDisplay, color, \
        pygame.Rect(note_x, note_y, note_w, note_h))

def draw_pad():
    global GameDisplay, SCREEN_H, NOTE_W, PAD_H
    padding = 10
    pygame.draw.rect(GameDisplay, (100,100,220), \
        pygame.Rect((SCREEN_H/2 - 2*NOTE_W - padding), PAD_H-5,\
             (4*NOTE_W + 2*padding), 10) )

def draw_panjeong(stage):
    global GameDisplay, SCREEN_H, NOTE_W, PAD_H
    msg = stage.cur_msg

    if msg == None:
        return

    dbeat = stage.get_dbeat()

    pj_text = font_pj.render(msg.text, True, msg.color)
    pj_surf = pygame.Surface((140, 60))
    pj_surf.blit(pj_text, (0,0))
    pj_surf.set_alpha(255 - max(dbeat-msg.target, 0) / msg.duration * 100)

    GameDisplay.blit(pj_surf, (SCREEN_H/2-70, PAD_H - 200))
        

def update_screen(stage, input_key):
    global GameDisplay

    for note in stage.notes:
        draw_note(stage, note)

    draw_pad()
    draw_panjeong(stage)
    


#------------MAIN----------------

if __name__ == '__main__':
    stage = Stage(bpm=180.0, stage_offset=0.05)
    
    stage.notes = generate_stage()

#    note1 = Note(row=0, target=4.0, duration=0.05)
#    note2 = Note(row=1, target=4.5, duration=0.05)
#    note3 = Note(row=2, target=5.0, duration=0.05)
#    note4 = Note(row=3, target=5.5, duration=0.05)
#    stage.notes = [note1,note2,note3,note4]


    #음원 재생
    mixer.music.load('R.mp3')
    mixer.music.set_volume(0.2)
    mixer.music.play()

    while True:
        if stage.life < 0:
            break


        input_key = None #입력받은 키 0,1,2,3: 각각 0,1,2,3번쨰 row Down
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    input_key = 0
                if event.key == pygame.K_s:
                    input_key = 1
                if event.key == pygame.K_l:
                    input_key = 2
                if event.key == pygame.K_SEMICOLON:
                    input_key = 3


        GameDisplay.fill((0,0,0))


        #노트 판정
        offset = 0.00

        miss_flag = True
        for i in range(len(stage.notes)):
            note = stage.notes[i]
            if note.do_pj == False:
                continue

            err = stage.get_err_seconds(note.target) + offset
            if err < -0.1:
                stage.add_panjeong(3) #Miss 판정
                stage.notes[i].do_pj = False
                continue

            if input_key == note.row:
                if abs(err) <= 0.05:
                    stage.add_panjeong(0) #Perfect 판정
                    stage.notes[i].do_pj = False
                elif err < 0:
                    stage.add_panjeong(1) #Slow 판정
                    stage.notes[i].do_pj = False
                elif err < 0.1:
                    stage.add_panjeong(2) #Fast 판정
                    stage.notes[i].do_pj = False
                if err < 0.3: #Miss로 처리되지 않게 함
                    miss_flag=False
                continue

        if input_key != None and miss_flag:
            stage.add_panjeong(3)


        #노트 판정 끝
        update_screen(stage=stage, input_key=input_key)


        #text = font.render(panjeong, True, (255,255,255))
        #GameDisplay.blit(text, (10, 50))

        title_text = font_title.render(f"★SUNGBUM MAX★", True, (255,255,255))
        bpm_text = font.render(f"BPM: {stage.bpm}", True, (255,255,255))
        score_text = font.render(f"SCORE: {stage.score}", True, (255,255,255))
        
        GameDisplay.blit(title_text, (10, 10))
        GameDisplay.blit(bpm_text, (10, 60))
        GameDisplay.blit(score_text, (10, 85))


        pygame.display.flip()
    
    mixer.music.fadeout(2000)
    gameover_text = font_title.render(f"GAME OVER", True, (255, 50, 50))
    GameDisplay.blit(gameover_text, (280, 250))
    pygame.display.flip()
    
    time.sleep(3)



