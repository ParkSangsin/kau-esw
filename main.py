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

def main():
    # 조이스틱 객체 생성
    joystick = Joystick()
    # joystick width, height에 맞는 이미지 생성
    my_image = Image.new("RGB", (joystick.width, joystick.height))
    # my_image에 그릴 도구 my_draw 생성
    my_draw = ImageDraw.Draw(my_image)

    character = Character(joystick.width, joystick.height) # 캐릭터 객체 생성
    
    # 시작화면 타이틀 텍스트 폰트 설정
    title_text = Font("~/esw/TA-ESW/game/font/Agbalumo-Regular.ttf", 20, (23, 50))

    # "Prees anykey to play" 폰트 설정
    press_text = Font("~/esw/TA-ESW/game/font/KdamThmorPro-Regular.ttf", 15, (40, 160))

    # 점수 폰트 설정
    score_text = Font("~/esw/TA-ESW/game/font/KdamThmorPro-Regular.ttf", 15, (23, 30))

    # 시작 화면 구성
    while True:
        # 아무 키를 누르면 게임 시작
        if not joystick.button_U.value or not joystick.button_D.value or not joystick.button_L.value or not joystick.button_R.value or not joystick.button_A.value or not joystick.button_B.value:
            time.sleep(0.5) # 누른 키가 게임에 적용되지 않도록 잠시 멈춤
            break
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (0, 0, 0, 100)) # 시작 화면
        my_draw.text(title_text.position, "The   Limit   Of   Speed", fill = "white", font = title_text.font) # 게임 제목
        my_draw.text(press_text.position, "Press  anykey  to  play", fill = "white", font = press_text.font)
        joystick.disp.image(my_image)

    a_time = 0 # a 버튼이 눌린 시간
    a_flag = True # A 버튼이 여러번 눌리지 않도록 현재 상태 체크

    start_time = time.time() # 게임 시작 시간

    while True:
        cur_time = time.time() # 현재 시간
        score = "{:.1f}".format(cur_time - start_time) # 게임 진행 시간 = 점수 (소수점 첫째자리까지)
        
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

        # 캐릭터 이동
        character.move(command)
    
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
        my_draw.ellipse(tuple(character.position), outline = character.outline, fill = (0, 0, 0))
        my_draw.text(score_text.position, "SCORE: " + score, fill = "blue", font = score_text.font)

        #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
        joystick.disp.image(my_image)
    
    end_time = time.time()

if __name__ == '__main__':
    main()