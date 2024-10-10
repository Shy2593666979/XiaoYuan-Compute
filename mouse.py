from pynput import mouse

def on_click(x, y, button, pressed):
    if pressed:
        if button == mouse.Button.left:
            print(f'鼠标左键点击: ({x}, {y})')
        if button == mouse.Button.right:
            print(f'鼠标右键点击: ({x}, {y})')

def mouse_coordinate():

    # 创建一个鼠标监听器
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

if __name__ == '__main__':
    mouse_coordinate()