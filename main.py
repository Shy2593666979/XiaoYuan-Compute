import time
import mss
import pyautogui
import pytesseract
from PIL import Image
from loguru import logger
import re

class XiaoYuan:

    def __init__(self, start_xy: tuple, left_identify: tuple, right_identify: tuple, tesseract_path: str) -> None:
        self.start_x = start_xy[0]
        self.start_y = start_xy[1]
        self.left_identify = left_identify
        self.right_identify = right_identify 
        self.tesseract_path = tesseract_path

    # 初始化OCR
    def init_tesseract(self):
        # 确保已经设置了Tesseract的路径
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

    def capture_screenshot(self, region: tuple):
        # 使用 mss 库来截取屏幕截图
        with mss.mss() as sct:
            screenshot = sct.grab(region)
            # 将截图保存为 PIL 图像对象
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            return img

    def get_image_number(self, img, convert: bool=False):
        try:
            if convert:
                # 启动灰度图像功能并应用二值化处理
                img = img.convert('L')
                img = img.point(lambda p: p > 128 and 255)
            # 使用Tesseract OCR识别数字
            custom_oem_psm_config = r'--oem 3 --psm 6 outputbase digits'
            text = pytesseract.image_to_string(img, config=custom_oem_psm_config)
            # 提取数字
            number_str = ''.join(re.findall(r'\d+', text))
            number = int(number_str)
            return number
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

    # 在画板上画大于号
    def draw_image_greater(self):
        pyautogui.moveTo(self.start_x, self.start_y)
        pyautogui.dragRel(100, -50, duration=0.1)  # 向右上拖动
        pyautogui.dragRel(-70, -70, duration=0.1)  # 向左上拖动

    # 在画板上画小于号
    def draw_image_less(self):
        pyautogui.moveTo(self.start_x, self.start_y)
        pyautogui.dragRel(-100, 50, duration=0.1)  # 向左下拖动
        pyautogui.dragRel(70, 70, duration=0.1)    # 向右下拖动

if __name__ == '__main__':
    # 提供有效的初始参数，需要根据自己设备更改
    xiaoyuan = XiaoYuan(
        start_xy=(500, 500),
        left_identify={'left': 100, 'top': 200, 'width': 100, 'height': 50},
        right_identify={'left': 300, 'top': 200, 'width': 100, 'height': 50},
        tesseract_path='C:/Program Files/Tesseract-OCR/tesseract.exe'
    )

    xiaoyuan.init_tesseract()

    # 起始位置
    step = 0

    while True:
        start_time = time.perf_counter()

        left_img = xiaoyuan.capture_screenshot(region=xiaoyuan.left_identify)
        right_img = xiaoyuan.capture_screenshot(region=xiaoyuan.right_identify)

        left_number = xiaoyuan.get_image_number(left_img)
        right_number = xiaoyuan.get_image_number(right_img)

        if left_number is None or right_number is None:
            print("Failed to recognize numbers. Retrying...")
            continue

        if left_number > right_number:
            xiaoyuan.draw_image_greater()
        else:
            xiaoyuan.draw_image_less()

        end_time = time.perf_counter()
        execution_time = end_time - start_time
        logger.info(f'第{step+1}次消耗时间为: {execution_time:.2f}秒')

        # 等待题目出现
        time.sleep(0.3)
        step += 1
