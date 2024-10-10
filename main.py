import time
import mss
import pyautogui
import pytesseract
from PIL import Image

class XiaoYuan:

    def __init__(self, start_xy: tuple, left_identify: tuple, right_identify: tuple, tesseract_path: str) -> None:
        self.start_x = start_xy[0]
        self.start_y = start_xy[1]
        self.left_identify = left_identify
        self.right_identify = right_identify 
        self.tesseract_path = tesseract_path
        self.image_prefix = './image/{}'

    # 初始化OCR
    def init_tesseract(self):

        # 确保已经设置了Tesseract的路径
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

    def capture_screenshot(self, output_path: str, region: tuple):
        # 使用 mss 库来截取屏幕截图
        with mss.mss() as sct:

            screenshot = sct.grab(region)
            # 将截图保存为 PIL 图像对象
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            
            # 保存图像
            img.save(output_path)
            print(f"图片保存到: {output_path}")


    def get_image_number(self, image_path: str):
        # 打开图像文件
        img = Image.open(image_path)

        # 使用Tesseract OCR识别图像中的文本
        text = pytesseract.image_to_string(img, config='--psm 6 digits')
        number = int(text)

        return number

    # 在画板上画大于号
    def draw_image_greater(self):
        
        pyautogui.moveTo(self.start_x, self.start_y)
        pyautogui.dragRel(100, -50, duration=0.1)  # 向右上拖动sqrt(100 * 100 + 50 * 50)像素
        pyautogui.dragRel(-70, -70, duration=0.1)  # 向左上拖动sqrt(70 * 70 * 2)像素

    # 在画板上画小于号
    def draw_image_less(self):

        pyautogui.moveTo(self.start_x, self.start_y)
        pyautogui.dragRel(-100, 50, duration=0.1)  # 向左下拖动sqrt(100 * 100 + 50 * 50)像素
        pyautogui.dragRel(70, 70, duration=0.1)  # 向右下拖动sqrt(70 * 70 * 2)像素

if __name__ == '__main__':
    xiaoyuan = XiaoYuan(start_xy=(),
                        left_identify=(),
                        right_identify=(),
                        tesseract_path='')

    xiaoyuan.init_tesseract()

    # 这里面需要利用mouse文件来检测电脑屏幕中题目出现的位置
    step = 1
    
    while True:
        left_image = f'left_{step}.png'
        left_image = xiaoyuan.image_prefix.format(left_image)
        xiaoyuan.capture_screenshot(left_image, region=xiaoyuan.left_identify)

        right_image = f'right_{step}.png'
        right_image = xiaoyuan.image_prefix.format(right_image)
        xiaoyuan.capture_screenshot(right_image, region=xiaoyuan.right_identify)

        left_number = xiaoyuan.get_image_number(left_image)
        right_number = xiaoyuan.get_image_number(right_image)

        if left_number > right_image:
            xiaoyuan.draw_image_greater()
        else:
            xiaoyuan.draw_image_less()

        # 等待题目出现
        time.sleep(0.3)
        step += 1
