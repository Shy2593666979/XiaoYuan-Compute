import time
import mss
import pyautogui
import pytesseract
from PIL import Image, ImageFilter
from loguru import logger
import re

class XiaoYuan:

    def __init__(self, start_xy: tuple, left_identify: tuple, right_identify: tuple, tesseract_path: str) -> None:
        self.start_x = start_xy[0]
        self.start_y = start_xy[1]
        self.left_identify = left_identify
        self.right_identify = right_identify 
        self.tesseract_path = tesseract_path
        self.duration = 0.0 # 鼠标移动的速度

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
        # 鼠标按下一笔画完
        pyautogui.mouseDown()
        pyautogui.moveRel(50, -30, duration=self.duration)  # 向左下拖动sqrt(50 * 50 + 30 * 30)像素
        pyautogui.moveRel(-30, -30, duration=self.duration)  # 向右下拖动sqrt(30 * 30 * 2)像素
        pyautogui.mouseUp()
        
    # 在画板上画小于号
    def draw_image_less(self):
        pyautogui.moveTo(self.start_x, self.start_y)
        # 鼠标按下一笔画完
        pyautogui.mouseDown()
        pyautogui.moveRel(-50, 30, duration=self.duration)  # 向左下拖动sqrt(50 * 50 + 30 * 30)像素
        pyautogui.moveRel(30, 30, duration=self.duration)  # 向右下拖动sqrt(30 * 30 * 2)像素
        pyautogui.mouseUp()
        
if __name__ == '__main__':
    xiaoyuan = XiaoYuan(start_xy=(350, 800),
                        left_identify=(180, 330, 270, 400),
                        right_identify=(400, 340, 470, 390),
                        tesseract_path=r'D:\ocr\tesseract.exe')

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
        logger.info(f'左边的数为: {left_number}-----右边的数为: {right_number}')
        logger.info(f'第{step+1}次消耗时间为: {execution_time}')

        # 等待题目出现
        time.sleep(0.45)
        step += 1
        # 防止出现鼠标不受控制
        if step > 15:
            break
