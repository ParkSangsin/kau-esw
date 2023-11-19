from PIL import Image, ImageDraw, ImageFont
import os

class Font():
    def __init__(self, path, size, position):
        self.font_path = os.path.expanduser(path) # 틸드를 확장하여 절대 경로로 변환
        self.position = position # 위치
        self.font = ImageFont.truetype(self.font_path, size)
