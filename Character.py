import numpy as np
import time
from PIL import Image, ImageDraw, ImageFont

class Character:
    def __init__(self, width, height):
        self.appearance = 'astrounaut'
        self.size = 30
        self.image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/astronaut.png").resize((self.size, self.size))
        self.superimage = Image.open("/home/kau-esw/esw/TA-ESW/game/png/superhero.png").resize((50, 50))
        self.shieldimage = Image.open("/home/kau-esw/esw/TA-ESW/game/png/shield_astronaut2.png").resize((self.size, self.size))
        self.state = None
        self.disp_size = (width, height)
        self.position = np.array([width / 2 - 15, height / 2 - 15, width / 2 + 15, height / 2 + 15])
        #self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.speed = 7 # 캐릭터 속도 기본 값
        self.energy = 2 # 캐릭터 에너지
        self.life = 100 # 캐릭터 목숨
        self.collision_effect = True
        self.a_flag = True
        self.shield = False

    def move(self, command = None):
        if command['move'] == False:
            self.state = None
        
        else:
            self.state = 'move'

            if command['up_pressed']:
                if self.position[1] - self.speed >= 0: # 화면 밖으로 나가지 않도록 설정 (위로 못나가도록)
                    self.position[1] -= self.speed
                    self.position[3] -= self.speed

            if command['down_pressed']:
                if self.position[3] + self.speed <= self.disp_size[1]: # 화면 밖으로 나가지 않도록 설정 (아래로 못나가도록)
                    self.position[1] += self.speed
                    self.position[3] += self.speed

            if command['left_pressed']:
                if self.position[0] - self.speed >= 0: # 화면 밖으로 나가지 않도록 설정 (왼쪽으로 못나가도록)
                    self.position[0] -= self.speed
                    self.position[2] -= self.speed
                
            if command['right_pressed']:
                if  self.position[2] + self.speed <= self.disp_size[1]: # 화면 밖으로 나가지 않도록 설정 (오른쪽으로 못나가도록)
                    self.position[0] += self.speed
                    self.position[2] += self.speed
# if self.position[0] - self.speed >= 0 and self.position[0] + self.sp <= self.disp_size[0] and self.position[1] >= 0 and self.position[1] <= self.disp_size[1]:
        #self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])

    def a_pressed_check(self, a_time, cur_time):
        if cur_time - a_time < 2: # 2초 동안
            self.speed = 15 
            self.size = 50
            if self.a_flag == True:
                self.position[0] -= 10
                self.position[1] -= 10
                self.position[2] += 10
                self.position[3] += 10
                self.a_flag = False
            return False # A 버튼을 누를 수 없는 상태 (speed가 10인 상태) 이면 False
        else:
            self.speed = 7
            self.size = 30
            if self.a_flag == False:
                self.position[0] += 10
                self.position[1] += 10
                self.position[2] -= 10
                self.position[3] -= 10
                self.a_flag = True
            return True # A 버튼을 누를 수 있는 상태 (speed가 7인 상태) 이면 True
    
    def collision_check(self, collision_time, cur_time):
        if cur_time - collision_time < 1: # 1초 동안
            return False 
        else:
            return True #

    # 에너지를 사용할 수 있는지 체크하는 함수 
    def energy_check(self):
        if self.energy == 0:
            return False
        else:
            return True
    
    # 캐릭터가 죽었는지 살았는지를 체크하는 함수 (죽었으면 True 반환)
    def life_check(self):
        if self.life <= 0:
            return True
        else:
            return False
        
    def reset(self):
        self.position = np.array([self.disp_size[0] / 2 - 15, self.disp_size[1] / 2 - 15, self.disp_size[0] / 2 + 15, self.disp_size[1] / 2 + 15])
        self.energy = 2 # 캐릭터 에너지
        self.life = 100 # 캐릭터 목숨
        self.shield = False
        self.size = 30
        self.a_flag = True
        self.shield = False
            
