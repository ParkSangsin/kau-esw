import numpy as np
import random
from PIL import Image, ImageDraw, ImageFont

class Item:
    def __init__(self):   
        self.size = 20
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
            self.image = Image.open("/home/kau-esw/esw/TA-ESW/game/png/superpower.png").resize((self.size, self.size))
            self.name = "superpower"

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
                character.life += 1
            elif self.name == 'energy':
                character.energy += 1
            """elif self.name == 'superpower':
                character.super()
"""
    # object의 위치와 other의 위치가 겹치면 True 반환
    def overlap(self, ego, other):
        if ego[0] + 5 <= other[2] and ego[1] + 5 <= other[3] - 5 and ego[2] - 5 >= other[0] and ego[3] - 5 >= other[1]: # 오차를 줄이기 위해 충돌 조건 완화
            return True
        else:
            return False