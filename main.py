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

def main():
    # 조이스틱 객체 생성
    joystick = Joystick()
    # joystick width, height에 맞는 이미지 생성
    my_image = Image.new("RGB", (joystick.width, joystick.height))
    # my_image에 그릴 도구 my_draw 생성
    my_draw = ImageDraw.Draw(my_image)

    character = Character(joystick.width, joystick.height) # 캐릭터 객체 생성
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100)) # 하얀 배경 그리기

    a_flag = False
    a_time = 0 # a 버튼이 눌린 시간

    while True:
        cur_time = time.time() # 현재 시간 
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

        if not joystick.button_A.value: # A pressed
            # energy가 0 이상이면, 3초 동안 속도 2배 증가
            if character.energy > 0: # 여러번 눌리는 현상 수정해야함
                character.energy -= 1
                a_time = time.time()
                print(character.energy)
        
        character.a_pressed_check(a_time, cur_time)

        character.move(command)
        
    
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
        my_draw.ellipse(tuple(character.position), outline = character.outline, fill = (0, 0, 0))

        #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
        joystick.disp.image(my_image)

if __name__ == '__main__':
    main()