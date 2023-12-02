import numpy as np
import random
import math
from PIL import Image, ImageDraw, ImageFont

class Object:
    def __init__(self):
        self.direction = {'up' : False, 'down' : False, 'left' : False, 'right' : False}         
        self.position = np.array([])
        self.size = random.randint(10, 35)
        self.state = None
        self.image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/meteor1.png").resize((self.size, self.size))

        # 랜덤으로 속도 선택
        self.speed = random.randint(1, 10)

        # 랜덤으로 이미지 선택
        self.rand_image = random.randint(1, 5)
        if self.rand_image == 1:
            self.image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/meteor1.png").resize((self.size, self.size))
        elif self.rand_image == 2:
            self.image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/meteor2.png").resize((self.size, self.size))
        elif self.rand_image == 3:
            self.image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/meteor3.png").resize((self.size, self.size))
        elif self.rand_image == 4:
            self.image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/satellite.png").resize((self.size, self.size))
        elif self.rand_image == 5:
            self.image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/spaceship.png").resize((self.size, self.size))

        # 객체 위치를 무작위로 생성 (위치에 따라 방향 변화)
        self.rand_position = random.randint(1, 4)
        self.rand_num = random.randint(0, 240 - self.size)
        if self.rand_position == 1:
            self.position = np.array([0, self.rand_num, self.size, self.rand_num + self.size])
            self.direction['right'] = True
        elif self.rand_position == 2:
            self.position = np.array([self.rand_num, 0, self.rand_num + self.size, self.size])
            self.direction['down'] = True
        elif self.rand_position == 3:
            self.position = np.array([240 - self.size, self.rand_num, 240, self.rand_num + self.size])
            self.direction['left'] = True
        elif self.rand_position == 4:
            self.position = np.array([self.rand_num, 240 - self.size, self.rand_num + self.size, 240])
            self.direction['up'] = True  

        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2]) # 위치가 결정되고 center 초기화

        self.damage = int((self.size + self.speed * 3.5) // 2) # 속도와 크기의 데미지 비중을 1:1로 구현

    def move(self):
        if self.direction['up']:
            self.position[1] -= self.speed
            self.position[3] -= self.speed

        if self.direction['down']:
            self.position[1] += self.speed
            self.position[3] += self.speed

        if self.direction['left']:
            self.position[0] -= self.speed
            self.position[2] -= self.speed
            
        if self.direction['right']:
            self.position[0] += self.speed
            self.position[2] += self.speed

        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2]) # center 갱신
    
    # 캐릭터와 충돌했는지를 체크
    def collision_check(self, character, a_flag, collision_flag):
        collision = self.overlap(self.position, character.position)
        if collision and collision_flag:
            if a_flag: # energy를 사용 or 직전에 충돌했을 경우 life 변화 X
                if character.shield == False: # 실드가 있을경우 실드만 해제
                    character.life -= self.damage
            self.state = 'hit'

     # object의 위치와 other의 위치가 겹치면 True 반환
    def overlap(self, ego, other):
        ego_center = np.array([(ego[0] + ego[2]) / 2, (ego[1]+ ego[3]) / 2])
        other_center = np.array([(other[0] + other[2]) / 2, (other[1]+ other[3]) / 2])

        distance = math.sqrt((other_center[0] - ego_center[0]) ** 2 + (other_center[1] - ego_center[1]) ** 2)

        r_r = ((ego[2] - ego[0]) / 2) + ((other[2] - other[0]) / 2)

        if distance <= r_r - 4:
            return True
        else:
            return False