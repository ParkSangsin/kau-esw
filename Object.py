import numpy as np
import random
class Object:
    def __init__(self):
        self.direction = {'up' : False, 'down' : False, 'left' : False, 'right' : False}         
        self.position = np.array([])
        self.speed = 1
        self.size = random.randint(10, 30)
        self.state = None
        self.outline = "#0000FF"

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
    
    # 캐릭터와 충돌했는지를 체크
    def collision_check(self, character):
        collision = self.overlap(self.position, character.position)
            
        if collision:
            character.life -= 1
            self.state = 'hit'

    # object의 위치와 other의 위치가 겹치면 True 반환
    def overlap(self, ego_position, other_position):
        return False
    