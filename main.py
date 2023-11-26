import os
import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import numpy as np
from Character import Character
from Joystick import Joystick
from Font import Font
from Object import Object
from Item import Item

score_list = ['0.0'] * 6

def main():
    global score_list
    # 조이스틱 객체 생성
    joystick = Joystick()

    # joystick width, height에 맞는 이미지 생성
    start_image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/startimage.jpg").resize((joystick.width, joystick.height))

    # start_image에 그릴 도구 start_draw 생성
    start_draw = ImageDraw.Draw(start_image)

    character = Character(joystick.width, joystick.height) # 캐릭터 객체 생성

    # 폰트 설정
    title_text = Font("~/esw/TA-ESW/game/font/Agbalumo-Regular.ttf", 20, (23, 10)) # 시작화면 타이틀 텍스트 폰트 설정
    end_text = Font("~/esw/TA-ESW/game/font/Agbalumo-Regular.ttf", 20, (15, 10)) # 종료화면 텍스트 폰트 설정
    end_score = Font("~/esw/TA-ESW/game/font/Agbalumo-Regular.ttf", 15, (145, 80)) # 종료화면 점수 표시 텍스트 설정
    press_text = Font("/home/kau-esw/esw/TA-ESW/game/font/KdamThmorPro-Regular.ttf", 18, (30, 150)) # "Prees anykey to play" 폰트 설정
    score_text = Font("~/esw/TA-ESW/game/font/Agbalumo-Regular.ttf", 15, (5, 5)) # 점수 표시 텍스트 폰트 설정
    energy_text = Font("~/esw/TA-ESW/game/font/Agbalumo-Regular.ttf", 15, (163, 5)) # 에너지 표시 텍스트 폰트 설정
    life_text = Font("~/esw/TA-ESW/game/font/Agbalumo-Regular.ttf", 15, (163, 25)) # 목숨 표시 텍스트 폰트 설정 (후에 하트 사진으로 변경)

    start_draw.text(title_text.position, "The   Draft   in   Space", fill = "gray", font = title_text.font) # 게임 제목
    start_draw.text(press_text.position, "Press  anykey  to  play", fill = "red", font = press_text.font)
    joystick.disp.image(start_image)

    # 시작 화면 구성
    while True:
        # 아무 키를 누르면 게임 시작
        if not joystick.button_U.value or not joystick.button_D.value or not joystick.button_L.value or not joystick.button_R.value or not joystick.button_A.value or not joystick.button_B.value:
            time.sleep(0.5) # 누른 키가 게임에 적용되지 않도록 잠시 멈춤
            break
        

    stage_num = 11
    stage = 0

    a_time = 0 # a 버튼이 눌린 시간
    a_flag = True # A 버튼이 여러번 눌리지 않도록 현재 상태 체크

    collision_time = 0 # 충돌 시간
    collision_effect = True # 충돌 effect 구현
    collision_flag = True

    objects = [] # 장애물 객체를 저장하는 배열
    items = []
    start_time = time.time() # 게임 시작 시간

    while True:
        cur_time = time.time() # 현재 시간
        score = "{:.1f}".format(cur_time - start_time) # 게임 진행 시간 = 점수 (소수점 첫째자리까지)
        
        # item이 나올 확률 조정
        rand_item_gen = random.randint(1, 275)
        if rand_item_gen == 1: 
            items.append(Item())
        
        # object가 나올 확률 조정
        if float(score) % 10.0 == 0 and stage <= 6:
            stage_num -= 1
            stage += 1
            print(stage, stage_num)
        rand_obj_gen = random.randint(1, stage_num)
        if rand_obj_gen == 1: 
            objects.append(Object())

        command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
    
        if not joystick.button_U.value:  # up pressed
            command['up_pressed'] = True
            command['move'] = True

        if not joystick.button_D.value:  # down pressed
            command['down_pressed'] = True
            command['move'] = True

        if not joystick.button_L.value:  # left pressed
            command['left_pressed'] = True
            command['move'] = True

        if not joystick.button_R.value:  # right pressed
            command['right_pressed'] = True
            command['move'] = True

        if not joystick.button_A.value and a_flag == True: # A pressed
            # energy가 0 이상이면, 3초 동안 속도 2배 증가
            if character.energy_check():
                character.energy -= 1
                a_time = time.time()

        # if not joystick.button_B.value and a_flag == True: # A pressed
        
        # a버튼이 눌렸는지 계속해서 체크 (중복 누름 방지)
        a_flag = character.a_pressed_check(a_time, cur_time)

        # 충돌 이펙트 구현
        if a_flag or collision_flag: # 평상시에만 충돌 체크
            collision_flag = character.collision_check(collision_time, cur_time)
        if collision_flag: # 충돌 후 2초가 지나면 True로 고정
            collision_effect = True
        else: # 충돌 후 2초 간 이펙트 생성
            if collision_effect == True:
                collision_effect = False
            else:
                collision_effect = True

        for i, object in enumerate(objects):
            object.move()
            # 에너지가 사용되지 않는 동안만 충돌체크
            object.collision_check(character, a_flag, collision_flag)
            if object.state == 'hit' and collision_flag:
                if a_flag:
                    collision_time = time.time()
                objects.pop(i)
            if object.center[0] < 0 or object.center[0] > joystick.height or object.center[1] < 0 or object.center[1] > joystick.width: # 화면 밖으로 벗어난객체 삭제
                objects.pop(i) 

        for i, item in enumerate(items):
            item.collision_check(character)
            if item.state == 'hit' or item.state == 'used':
                items.pop(i)

        # 현재 캐릭터가 살았는지 죽었는지를 체크
        if character.life_check():
            break

        # 캐릭터 이동
        character.move(command)
    
        game_image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/game.jpg").resize((joystick.width, joystick.height))
        game_draw = ImageDraw.Draw(game_image) # game_image와 draw 연동 (game_image위에 그릴 도구)
        game_draw.text(score_text.position, "SCORE: " + score, fill = "blue", font = score_text.font) # game_image 위에 점수 그리기
        game_draw.text(energy_text.position, "ENERGY: " + str(character.energy), fill = "green", font = energy_text.font) # game_image 위에 남은 에너지 그리기
        game_draw.text(life_text.position, "LIFE: " + str(character.life), fill = "red", font = life_text.font) # game_image 위에 남은 에너지 그리기

        for object in objects:
            game_image.paste(object.image, tuple(map(int, object.position)), object.image)

        for item in items:
            game_image.paste(item.image, tuple(map(int, item.position)), item.image)

        if collision_effect:
            if a_flag:
                game_image.paste(character.image, tuple(map(int, character.position)), character.image) # 캐릭터 그리기 (맨 위에 그리기 -> 캐릭터가 가리지 않도록)
            else:
                game_image.paste(character.superimage, tuple(map(int, character.position)), character.superimage) # 에너지 사용시 사진 변경
            

        joystick.disp.image(game_image)

    end_time = "{:.1f}".format(time.time() - start_time) # 종료시간
    score_list.append(end_time) # 점수판에 이번 게임의 점수 삽입
    score_list = list(map(float, score_list)) # 점수판 내용을 실수 변환 후
    score_list = sorted(score_list, reverse=True) # 점수판 내용을 내림차순 정렬
    score_list = list(map(str, score_list)) # 점수판 내용을 다시 문자열로 변환
    # 종료 화면 구성

    # joystick width, height에 맞는 종료화면 이미지 생성
    end_image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/endimage.png").resize((joystick.width, joystick.height))

    # end_image에 그릴 도구 end_draw 생성
    end_draw = ImageDraw.Draw(end_image)

    end_draw.text(end_text.position, "You   Dead", fill = "red", font = end_text.font)
    end_draw.text(end_score.position, "SCORE: " + score, fill = "red", font = end_score.font)

    joystick.disp.image(end_image)

    # 죽고 난 후 버튼 눌러짐 방지를 위해 잠시 일시정지
    time.sleep(1)
    
    while True:
        # 아무 키를 누르면 점수판 화면으로 이동
        if not joystick.button_U.value or not joystick.button_D.value or not joystick.button_L.value or not joystick.button_R.value or not joystick.button_A.value or not joystick.button_B.value:
            time.sleep(0.5) # 누른 키가 점수판 화면에 적용되지 않도록 잠시 멈춤
            break
    
    # 점수판 화면 구성

    # joystick width, height에 맞는 점수판 화면 이미지 생성
    score_image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/game.jpg").resize((joystick.width, joystick.height))

    # score_image에 그릴 도구 score_draw 생성
    score_draw = ImageDraw.Draw(score_image)

    #score_draw.text(end_text.position, "You   Dead", fill = "red", font = end_text.font)
    #end_draw.text(end_score.position, "SCORE: " + score, fill = "red", font = end_score.font)

    score_image_text = Font("/home/kau-esw/esw/TA-ESW/game/font/Roboto-Black.ttf", 30, (40, 20))
    score_draw.text(score_image_text.position, "S  C  O  R  E", fill = "yellow", font = score_image_text.font)

    if score_list[0] == end_time:
        best_score_text = Font("/home/kau-esw/esw/TA-ESW/game/font/Roboto-Black.ttf", 25, (55, 70))
        score_draw.text(best_score_text.position, f"Best Score !", fill = "red", font = best_score_text.font)

    score_left_start_position = [20, 110]
    for i, string in enumerate(score_list[0:3]):
        string_score_text = Font("/home/kau-esw/esw/TA-ESW/game/font/Roboto-Black.ttf", 20, score_left_start_position)
        score_draw.text(string_score_text.position, f"{i+1})  {string}", fill = "blue", font = string_score_text.font)
        if string == end_time:
            score_draw.text(string_score_text.position, f"{i+1})  {string}", fill = "red", font = string_score_text.font)
        score_left_start_position[1] += 40
    
    score_right_start_position = [130, 110]
    for i, string in enumerate(score_list[3:6]):
        string_score_text = Font("/home/kau-esw/esw/TA-ESW/game/font/Roboto-Black.ttf", 20, score_right_start_position) 
        score_draw.text(string_score_text.position, f"{i+4})  {string}", fill = "blue", font = string_score_text.font)
        if string == end_time:
            score_draw.text(string_score_text.position, f"{i+1})  {string}", fill = "red", font = string_score_text.font)
        score_right_start_position[1] += 40

    joystick.disp.image(score_image)

    while True:
        # 아무 키를 누르면 다시 시작 화면으로 이동
        if not joystick.button_U.value or not joystick.button_D.value or not joystick.button_L.value or not joystick.button_R.value or not joystick.button_A.value or not joystick.button_B.value:
            time.sleep(0.5) # 누른 키가 점수판 화면에 적용되지 않도록 잠시 멈춤
            break

    

if __name__ == '__main__':
    while True:
        main()