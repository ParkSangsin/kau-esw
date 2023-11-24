import numpy as np
import random
from PIL import Image, ImageDraw, ImageFont

class Object:
    def __init__(self):
        self.direction = {'up' : False, 'down' : False, 'left' : False, 'right' : False}         
        self.position = np.array([])
        self.size = random.randint(10, 35)
        self.state = None
        self.image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/meteor1.png").resize((self.size, self.size))

        # 랜덤으로 속도 선택
        self.speed = random.randint(1, 5)

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
    def collision_check(self, character, a_flag):
        collision = self.overlap(self.position, character.position)
        if collision:
            if a_flag: # energy를 사용했을 시에는 life 변화 X
                character.life -= 1
            self.state = 'hit'

    # object의 위치와 other의 위치가 겹치면 True 반환
    def overlap(self, ego, other):
        if ego[0] + 5 <= other[2] and ego[1] + 5 <= other[3] - 5 and ego[2] - 5 >= other[0] and ego[3] - 5 >= other[1]: # 오차를 줄이기 위해 충돌 조건 완화
            return True
        else:
            return False