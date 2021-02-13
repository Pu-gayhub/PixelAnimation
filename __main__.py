#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""注意
! 如果生成视频会用很久， 很久...
! 需要安装imagemagick以截图
! 终端需要调小字号并支持真彩色
! 可以只使用show函数显示图片
"""
from pathlib import Path
from time import sleep
from subprocess import run

import cv2 as cv
from rich.color import Color
from rich.console import Console
from rich.style import Style
from rich.text import Text


FRAMES_DIR = "./frames"  # 视频帧目录
OUT_DIR = "./out"  # 截图输出目录
VIDEO_PATH = "./source.mp4"  # 原视频路径

CONSOLE = Console(color_system="truecolor")  # 需要终端支持真彩色


def mkdir(dir_path):
    dir_ = Path(dir_path)
    if not dir_.is_dir():
        dir_.mkdir()


def getFrames(frames_dir):
    """获取所有帧并排序"""
    frames = Path(frames_dir).glob("*.png")
    return sorted(frames)


def load(image_path, percent=0.5):
    """

    Args:
        percent[float]: 浮点数形式缩放百分比
    """
    img = cv.imread(image_path, flags=3)
    img = cv.resize(img, dsize=None, fx=percent*2,
                    fy=percent, interpolation=cv.INTER_AREA)
    return img


def render(img):
    size = img.shape
    text = Text()
    # 一次读取两行像素
    # bgcolor为第一行， color为第二行
    for lines in range(0, size[0], 2):
        for px in range(size[1]):
            line1 = lines
            line2 = lines + 1
            b1, g1, r1 = img[line1, px]  # line1
            bgcolor = Color.from_rgb(r1, g1, b1)
            try:
                b2, g2, r2 = img[line2, px]  # line2
                color = Color.from_rgb(r2, g2, b2)
            except IndexError:
                color = None
            style = Style(color=color, bgcolor=bgcolor)
            # 使用半块生成
            # 空白部分用bgcolor渲染
            # 块使用color渲染
            # 合成两行像素
            text.append('▄', style=style)
        text.append('\n')
    return text


def show(console, image_path):
    """显示图片， 可单独使用

    Args:
        console[rich.console.Console]: rich终端对象
    """
    console.clear()
    img = load(image_path)

    text = render(img)
    console.print(text, justify="center")


def screenshots(out_dir, file_name):
    mkdir(out_dir)
    out_path = Path(out_dir, file_name).absolute()
    # 需要安装 imagemagick
    cmd = ["import", "-window", "root", out_path]
    run(cmd)


def main():
    frames = getFrames(FRAMES_DIR)
    for frame_index in range(len(frames)):
        frame = str(frames[frame_index])
        show(CONSOLE, frame)
        # 由于rich机制所以需要等待输出完成
        # 休眠时长视图片大小与性能而定
        # 暂时没有更好的方案
        sleep(0.3)
        file_name = str(frame_index).zfill(4) + ".png"
        # 截图并保存
        screenshots(OUT_DIR, file_name)


if __name__ == "__main__":
    main()
