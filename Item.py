import numpy as np
import random
from PIL import Image, ImageDraw, ImageFont
import math

class Item:
    def __init__(self):   
        self.size = 25
        self.state = None
        self.image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/aid-kit.png").resize((self.size, self.size))
        self.name = ""

        # 랜덤으로 이미지 선택
        self.rand_image = random.randint(1, 3)
        if self.rand_image == 1:
            self.image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/aid-kit.png").resize((self.size, self.size))
            self.name = "life"
        elif self.rand_image == 2:
            self.image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/energy.png").resize((self.size, self.size))
            self.name = "energy"
        elif self.rand_image == 3:
            self.image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/shield.png").resize((self.size, self.size))
            self.name = "shield"

        # 아이템 위치를 무작위로 생성 (위치에 따라 방향 변화)
        self.rand_x = random.randint(0, 240 - self.size)
        self.rand_y = random.randint(0, 240 - self.size)
        self.position = np.array([self.rand_x, self.rand_y, self.rand_x + self.size, self.rand_y + self.size])
    
    # 캐릭터와 충돌했는지를 체크
    def collision_check(self, character):
        collision = self.overlap(self.position, character.position)
        if collision:
            self.state = 'hit'
            if self.name == 'life':
                if character.life + 25 >= 100:
                    character.life = 100
                else:
                    character.life += 25
            elif self.name == 'energy':
                character.energy += 1
            elif self.name == 'shield':
                character.shield = True
                
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