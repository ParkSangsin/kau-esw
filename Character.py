import numpy as np
import time

class Character:
    def __init__(self, width, height):
        self.appearance = 'circle'
        self.state = None
        self.position = np.array([width/2 - 20, height/2 - 20, width/2 + 20, height/2 + 20])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#FFFFFF"
        self.speed = 5 # 캐릭터 속도 기본 값
        self.energy = 3

    def move(self, command = None):
        if command['move'] == False:
            self.state = None
            self.outline = "#FFFFFF" # 정지 -> 테두리 검정
        
        else:
            self.state = 'move'
            self.outline = "#FF0000" # 이동 -> 테두리 빨강

            if command['up_pressed']:
                self.position[1] -= self.speed
                self.position[3] -= self.speed

            if command['down_pressed']:
                self.position[1] += self.speed
                self.position[3] += self.speed

            if command['left_pressed']:
                self.position[0] -= self.speed
                self.position[2] -= self.speed
                
            if command['right_pressed']:
                self.position[0] += self.speed
                self.position[2] += self.speed

        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])

    def a_pressed_check(self, a_time, cur_time):
        if cur_time - a_time < 3:
            self.speed = 10
        else:
            self.speed = 5
