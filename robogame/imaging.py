# coding:utf-8
import Image as image


def resizeImg(im, dst_w, dst_h):
    if isinstance(im, str):
        im = image.open(im)
    ori_w, ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1
    if (ori_w and ori_w > dst_w) or (ori_h and ori_h > dst_h):
        if dst_w and ori_w > dst_w:
            widthRatio = float(dst_w) / ori_w  # 正确获取小数的方式
        if dst_h and ori_h > dst_h:
            heightRatio = float(dst_h) / ori_h
        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio
        if widthRatio and not heightRatio:
            ratio = widthRatio
        if heightRatio and not widthRatio:
            ratio = heightRatio
        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h
    return im.resize((newWidth, newHeight), image.ANTIALIAS)


def clipResizeImg(im, dst_w, dst_h):
    if isinstance(im, str):
        im = image.open(im)
    ori_w, ori_h = im.size
    dst_scale = float(dst_h) / dst_w  # 目标高宽比
    ori_scale = float(ori_h) / ori_w  # 原高宽比
    if ori_scale >= dst_scale:
        # height overflow
        width = ori_w
        height = int(width * dst_scale)
        x = 0
        y = (ori_h - height) / 3
    else:
        # width overflow
        height = ori_h
        width = int(height * dst_scale)
        x = (ori_w - width) / 2
        y = 0
        # clip
    box = (x, y, width + x, height + y)
    # 这里的参数可以这么认为：从某图的(x, y)坐标开始截，截到(width + x, height + y)坐标
    # 所包围的图像，crop方法与php中的imagecopy方法大为不一样
    newIm = im.crop(box)
    im = None
    # 压缩
    ratio = float(dst_w) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    return newIm.resize((newWidth, newHeight), image.ANTIALIAS)
