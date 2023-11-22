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

def main():
    # 조이스틱 객체 생성
    joystick = Joystick()

    # joystick width, height에 맞는 이미지 생성
    start_image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/startimage.jpg").resize((joystick.width, joystick.height))

    # start_image에 그릴 도구 start_draw 생성
    start_draw = ImageDraw.Draw(start_image)

    character = Character(joystick.width, joystick.height, "/home/kau-esw/esw/TA-ESW/game/png/astronaut.png") # 캐릭터 객체 생성

    # 시작화면 타이틀 텍스트 폰트 설정
    title_text = Font("~/esw/TA-ESW/game/font/Agbalumo-Regular.ttf", 20, (23, 20))

    # 종료화면 텍스트 폰트 설정
    end_text = Font("~/esw/TA-ESW/game/font/Agbalumo-Regular.ttf", 20, (15, 10))

    # 종료화면 점수 표시 텍스트 설정
    end_score = Font("~/esw/TA-ESW/game/font/Agbalumo-Regular.ttf", 15, (145, 80))

    # "Prees anykey to play" 폰트 설정
    press_text = Font("/home/kau-esw/esw/TA-ESW/game/font/KdamThmorPro-Regular.ttf", 18, (30, 180))

    # 점수 표시 텍스트 폰트 설정
    score_text = Font("~/esw/TA-ESW/game/font/Agbalumo-Regular.ttf", 15, (5, 5))

    # 에너지 표시 텍스트 폰트 설정
    energy_text = Font("~/esw/TA-ESW/game/font/Agbalumo-Regular.ttf", 15, (163, 5))

    # 목숨 표시 텍스트 폰트 설정 (후에 하트 사진으로 변경)
    life_text = Font("~/esw/TA-ESW/game/font/Agbalumo-Regular.ttf", 15, (163, 25))

    # 시작 화면 구성
    while True:
        # 아무 키를 누르면 게임 시작
        if not joystick.button_U.value or not joystick.button_D.value or not joystick.button_L.value or not joystick.button_R.value or not joystick.button_A.value or not joystick.button_B.value:
            time.sleep(0.5) # 누른 키가 게임에 적용되지 않도록 잠시 멈춤
            break
        start_draw.text(title_text.position, "The   Draft   in   Space", fill = "red", font = title_text.font) # 게임 제목
        start_draw.text(press_text.position, "Press  anykey  to  play", fill = "blue", font = press_text.font)
        joystick.disp.image(start_image)

    a_time = 0 # a 버튼이 눌린 시간
    a_flag = True # A 버튼이 여러번 눌리지 않도록 현재 상태 체크

    objects = [] # 장애물 객체를 저장하는 배열

    start_time = time.time() # 게임 시작 시간

    while True:
        cur_time = time.time() # 현재 시간
        score = "{:.1f}".format(cur_time - start_time) # 게임 진행 시간 = 점수 (소수점 첫째자리까지)
        
        # object가 나올 확률 조정
        rand_gen = random.randint(1, 15)
        if rand_gen == 1: 
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
                print(character.energy)
        
        # a버튼이 눌렸는지 계속해서 체크
        a_flag = character.a_pressed_check(a_time, cur_time)

        for i, object in enumerate(objects):
            object.move()
            object.collision_check(character)
            if object.center[0] < 0 or object.center[0] > joystick.height or object.center[1] < 0 or object.center[1] > joystick.width or object.state == 'hit': # 화면 밖으로 벗어나거나, 캐릭터와 충돌한 객체 삭제
                objects.pop(i) 

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
        game_image.paste(character.image, tuple(map(int, character.position)), character.image) # 캐릭터 그리기 (맨 위에 그리기 -> 캐릭터가 가리지 않도록)

        for object in objects:
            if object.state != 'hit':
                game_image.paste(object.image, tuple(map(int, object.position)), object.image)

        joystick.disp.image(game_image)

    end_time = "{:.1f}".format(time.time() - start_time) # 종료시간

    print(end_time)

    # 종료 화면 구성

    # joystick width, height에 맞는 종료화면 이미지 생성
    end_image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/endimage.png").resize((joystick.width, joystick.height))

    # end_image에 그릴 도구 my_draw 생성
    end_draw = ImageDraw.Draw(end_image)

    end_draw.text(end_text.position, "You   Dead", fill = "red", font = end_text.font)
    end_draw.text(end_score.position, "SCORE: " + score, fill = "red", font = end_score.font)

    joystick.disp.image(end_image)

    # 죽고 난 후 버튼 눌러짐 방지를 위해 잠시 일시정지
    time.sleep(1)
    
    while True:
        # 아무 키를 누르면 다시 게임 시작
        if not joystick.button_U.value or not joystick.button_D.value or not joystick.button_L.value or not joystick.button_R.value or not joystick.button_A.value or not joystick.button_B.value:
            time.sleep(0.5) # 누른 키가 시작화면에 적용되지 않도록 잠시 멈춤
            break

if __name__ == '__main__':
    while True:
        main()