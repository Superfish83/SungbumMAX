import pygame
from pygame.locals import *
from pygame import mixer
import random, time
from sbmax_stage import *
from generate_stage import *
from math import *

FPS = 120
FramePerSec = pygame.time.Clock()
KeysOn = [False]*4
pygame.init()
mixer.init()

SCREEN_H, SCREEN_V, NOTE_W, PAD_H = 1000, 600, 100, 520
GameDisplay = pygame.display.set_mode((SCREEN_H, SCREEN_V))
pygame.display.set_caption("SungbumMAX")
font = pygame.font.SysFont('NanumGothic', 20)  # 기본 폰트 및 사이즈 설정
font_pj = pygame.font.SysFont('NanumGothicBold', 44)  # 판정용 폰트
font_cb = pygame.font.SysFont('NanumGothicBold', 50)  # 콤보용 폰트
font_title = pygame.font.SysFont('NanumGothicBold', 30)  # 타이틀 폰트

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

def draw_background():
    global GameDisplay, SCREEN_H, SCREEN_V, NOTE_W, PAD_H
    GameDisplay.fill((0,0,0))
    pygame.draw.rect(GameDisplay, (30, 30, 30), \
        pygame.Rect((SCREEN_H/2 - 2*NOTE_W), 0, 4*NOTE_W, PAD_H))
    pygame.draw.rect(GameDisplay, (40, 40, 40), \
        pygame.Rect((SCREEN_H/2 - 2*NOTE_W), PAD_H, 4*NOTE_W, SCREEN_V-PAD_H))

def draw_pad():
    global GameDisplay, KeysOn, SCREEN_H, SCREEN_V, NOTE_W, PAD_H
    #padding = 10

    color = [(100,100,220)]*4
    for i in range(4):
        color = (140,140,240)
        if KeysOn[i]:
            color = (160,100,220)

        pygame.draw.rect(GameDisplay, color, \
            pygame.Rect((SCREEN_H/2 + (i-2)*NOTE_W), PAD_H-5,\
                (NOTE_W), 10) )
    
    for i in range(3):
        pygame.draw.line(GameDisplay, (100,100,100), \
            (SCREEN_H/2 + (i-1)*NOTE_W, 0), (SCREEN_H/2 + (i-1)*NOTE_W, SCREEN_V), 2)

def draw_panjeong(stage):
    global GameDisplay, SCREEN_H, NOTE_W, PAD_H
    msg = stage.cur_msg

    if msg == None:
        return

    dbeat = stage.get_dbeat()

    pj_text = font_pj.render(msg.text, True, msg.color)
    pj_surf = pygame.Surface((msg.length, 60)).convert_alpha()
    pj_surf.fill((0,0,0,0))
    pj_surf.blit(pj_text, (0,0))
    pj_surf.set_alpha(255 - max(dbeat-msg.target, 0) / msg.duration * 100)

    GameDisplay.blit(pj_surf, (SCREEN_H/2-msg.length/2, PAD_H - 200))

def draw_combo(stage):
    global GameDisplay, SCREEN_H, NOTE_W, PAD_H

    if stage.combo < 5:
        return
    
    msg = stage.cur_combo

    dbeat = stage.get_dbeat()

    cb_text = font_pj.render(msg.text, True, msg.color)
    cb_surf = pygame.Surface((msg.length, 60)).convert_alpha()
    cb_surf.fill((0,0,0,0))
    cb_surf.blit(cb_text, (0,0))
    cb_surf.set_alpha(255 - max(dbeat-msg.target, 0) / msg.duration * 100)

    anim = 5*sqrt(dbeat-msg.target) #위로 올라오는 애니메이션

    GameDisplay.blit(cb_surf, ((SCREEN_H/2)-(msg.length/2), 100 - anim))
    
        

def update_screen(stage):
    global GameDisplay
    
    draw_background()

    for note in stage.notes:
        draw_note(stage, note)

    draw_pad()
    draw_panjeong(stage)
    draw_combo(stage)
    


#------------MAIN----------------

if __name__ == '__main__':
    stage = gen_random(code='',bpm=180,offset=0.16)
    #stage = gen_stage_from_file('maps/plum_R.sbmax')

    #음원 재생
    mixer.music.load('music/plum_R.mp3')
    mixer.music.set_volume(0.2)
    mixer.music.play()

    while True:
        if stage.life < 0 or stage.get_dbeat() > stage.length:
            break


        input_key = 8 #입력받은 키 0,1,2,3: 각각 0,1,2,3번쨰 row Down
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

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    input_key = 4
                if event.key == pygame.K_s:
                    input_key = 5
                if event.key == pygame.K_l:
                    input_key = 6
                if event.key == pygame.K_SEMICOLON:
                    input_key = 7

        if input_key < 8:
            b = True
            if input_key>=4:
                b = False
            KeysOn[input_key%4] = b


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

        if input_key < 4 and miss_flag:
            stage.add_panjeong(3)

        #노트 판정 끝
        update_screen(stage=stage)


        #text = font.render(panjeong, True, (255,255,255))
        #GameDisplay.blit(text, (10, 50))

        title_text = font_title.render(f"★SUNGBUM MAX★", True, (255,255,255))
        bpm_text = font.render(f"BPM: {stage.bpm}", True, (255,255,255))
        score_text = font.render(f"SCORE: {stage.score}", True, (255,255,255))
        life_text = font.render(f"{'♥' * (stage.life+1)}", True, (220,100,100))
        
        GameDisplay.blit(title_text, (10, 10))
        GameDisplay.blit(bpm_text, (10, 55))
        GameDisplay.blit(score_text, (10, 80))
        GameDisplay.blit(life_text, (10, 105))


        pygame.display.flip()
    
    mixer.music.fadeout(2000)

    if stage.life < 0: # 죽어서 끝난 경우
        gameover_text = pygame.font.SysFont('NanumGothicBold', 50)\
            .render(f"GAME OVER", True, (255, 50, 50))
        GameDisplay.blit(gameover_text, (SCREEN_H/2-150, 220))
    else: # 스테이지를 클리어한 경우
        gameover_text = pygame.font.SysFont('NanumGothicBold', 60)\
            .render(f"CLEAR!", True, (50, 250, 50))
        GameDisplay.blit(gameover_text, (SCREEN_H/2-110, 240))

    

    pygame.display.flip()
    
    time.sleep(3)



