#  coding:utf-8

from svmutil import *
from PIL import Image
import cv2
import os

def get_feature(img):
    """
    獲取指定圖片的特征值,
    1. 按照每排的像素點,高度為10,則有10個維度,然後為6列,總共16個維度
    :param img_path:
    :return:一個維度為10（高度）的列表
    """

    width, height = img.size

    pixel_cnt_list = []
    height = 10
    for y in range(height):
        pix_cnt_x = 0
        for x in range(width):
            if img.getpixel((x, y)) == 0:  # 黑色點
                pix_cnt_x += 1

        pixel_cnt_list.append(pix_cnt_x)

    for x in range(width):
        pix_cnt_y = 0
        for y in range(height):
            if img.getpixel((x, y)) == 0:  # 黑色點
                pix_cnt_y += 1

        pixel_cnt_list.append(pix_cnt_y)

    return pixel_cnt_list

# 分割圖片
def spiltimg(img):
	# 按照圖片的特點,進行切割,根據具體的驗證碼進行
	child_img_list = []
	for index in range(4):
		x = 6 + index * (8 + 1)
		y = 5
		child_img = img.crop((x, y, x + 9, img.height - 2))
		child_img_list.append(child_img)
	return child_img_list

def get_bin_table(threshold):
	table = []
	for i in range(256):
		if i < threshold:
			table.append(0)
		else:
			table.append(1)
	return table

# 去除噪点
def greyImg(image, pts=2):
	width = image.width
	height = image.height
	box = (0, 0, width, height)
	imgnew = image.crop(box)
	for i in range(0, height):
		for j in range(0, width):
			num = sum_9_region(image, j, i)
			if num < pts:
				imgnew.putpixel((j, i), 255)  # 白色
			else:
				imgnew.putpixel((j, i), 0)  #  黑色
	return imgnew

def sum_9_region(img, x, y):
    """
    9鄰域框,以當前點為中心的田字框,黑點個數
    :param x:
    :param y:
    :return:
    """
    # todo判斷圖片的長寬度下限
    cur_pixel = img.getpixel((x, y))  # 當前像素點的值
    width = img.width
    height = img.height

    if cur_pixel == 1:  # 如果當前點為白色區域,則不統計鄰域值
        return 0

    if y == 0:  # 第一行
        if x == 0:  # 左上頂點,4鄰域
            # 中心點旁邊3個點
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 4 - sum
        elif x == width - 1:  # 右上頂點
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 4 - sum
        else:  # 最上非頂點,6鄰域
            sum = img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - sum
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下頂點
            # 中心點旁邊3個點
            sum = cur_pixel \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x, y - 1))
            return 4 - sum
        elif x == width - 1:  # 右下頂點
            sum = cur_pixel \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y - 1))

            return 4 - sum
        else:  # 最下非頂點,6鄰域
            sum = cur_pixel \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x + 1, y - 1))
            return 6 - sum
    else:  # y不在邊界
        if x == 0:  # 左邊非頂點
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))

            return 6 - sum
        elif x == width - 1:  # 右邊非頂點
            # print('%s,%s' % (x, y))
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 6 - sum
        else:  # 具備9領域條件的
            sum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum

def print_binary_img(binImg):
    img = binImg.load()
    for i in range(binImg.size[1]):
        s = ""
        for j in range(binImg.size[0]):
            s += str(img[j, i]) + " "
        print s + "\n"

def train(filename, merge_pic_path):
    if os.path.exists(filename):
        os.remove(filename)
    result = open(filename, 'a')
    for f in os.listdir(merge_pic_path):
        if f != '.DS_Store' and os.path.isdir(merge_pic_path + f):
            for img in os.listdir(merge_pic_path + f):
                if img.endswith(".jpg"):
                    pic = Image.open(merge_pic_path + f + "/" + img)
                    pixel_cnt_list = get_feature(pic)
                    if ord(f) >= 97:
                        line = str(ord(f)) + " "
                    else:
                        line = f + " "
                    for i in range(1, len(pixel_cnt_list) + 1):
                        line += "%d:%d " % (i, pixel_cnt_list[i - 1])
                    result.write(line + "\n")
    result.close()

filename = "C:/Users/use/Desktop/test.txt"
path = "C:/Users/use/Desktop/ValidatedCode/test/"
train(filename, path)
# img_path = "C:/Users/use/Desktop/ValidatedCode/sample_1000/"
# for idx, file in enumerate(os.listdir(img_path)):
#     print idx
#     filename = img_path + file
#
#     image = Image.open(filename)
#     # 轉化為灰階圖
#     imgry = image.convert('L')
#
#     table = get_bin_table(110)
#     out = imgry.point(table, '1')
#
#     im = greyImg(out, 5)
#     im.save("C:/Users/use/Desktop/code.bmp")
#     # im.show()
#
#     im = cv2.imread('C:/Users/use/Desktop/code.bmp', flags=cv2.CV_LOAD_IMAGE_GRAYSCALE)
#     retval, im = cv2.threshold(im, 155, 255, cv2.THRESH_BINARY_INV)
#     contours, hierarchy = cv2.findContours(im.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x:x[1])
#     arr = []
#
#     for index, (c, _) in enumerate(cnts):
#         (x, y, w, h) = cv2.boundingRect(c)
#
#         try:
#             # 只將寬高大於 8 視為數字留存
#             if w > 8 and h > 8:
#                 add = True
#                 for i in range(0, len(arr)):
#                     # 這邊是要防止如 0、9 等，可能會偵測出兩個點，當兩點過於接近需忽略
#                     if abs(cnts[index][1] - arr[i][0]) <= 3:
#                         add = False
#                         break
#                 if add:
#                     arr.append((x, y, w, h))
#         except IndexError:
#             pass
#
#     for index, (x, y, w, h) in enumerate(arr):
#         roi = im[y: y + h, x: x + w]
#         thresh = roi.copy()
#         res = cv2.resize(thresh, (30, 30), interpolation=cv2.INTER_CUBIC)
#         cv2.imwrite('C:/Users/use/Desktop/ValidatedCode/cut_img/{}-{}.jpg'.format(idx, index+1), res)


