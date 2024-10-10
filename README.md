# XiaoYuan-Compute

以下教程对初步学习计算机的同学或未接触过计算机的同学可能有些困难，这两天会出一个视频教程🤗🤗🤗

GUZxy8Uq7EQ
[![视频标题](https://img.youtube.com/vi/GUZxy8Uq7EQ/0.jpg)](https://www.youtube.com/watch?v=GUZxy8Uq7EQ)

## 安装 OCR
[Tesseract OCR 下载链接](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.3.0.20221214.exe)

这个是图片识别的工具，可以根据指定的图片来识别数字以及中文

## 安装Python依赖
下载完需要记录安装本地的地址

- 安装Python依赖

```
pip install requirements.txt
```

## 做提前准备，找到对应的几个坐标值

先通过 mouse.py 启动后点击小猿口算中题目出现的位置

方法如下：

- 找到左边数字的左上角点击一下，然后左边数字的右下角点击一下，会给你打印出对应的坐标值，打印的两次坐标值分别对应的是一个图片的左上角的XY 和 右下角的XY，这样可以确定一个图片的位置

- 找到右边数字的左上角点击一下，然后右边数字的右下角点击一下，会给你打印出对应的坐标值，打印的两次坐标值分别对应的是一个图片的左上角的XY 和 右下角的XY，这样可以确定一个图片的位置

- 找到输入＞ or ＜ 的画板，然后点击一下，确定一下画图时的起始位置

- 注意❗上述说的点击最好使用右键，因为左键用的地方比较多，可能会导致一些数据混乱而找不到对应的坐标

## 启动文件

然后根据自己的需求来启动 main文件

```
python main.py
```
