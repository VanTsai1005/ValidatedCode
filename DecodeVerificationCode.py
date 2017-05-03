from pytesser import *
import re

def getVerificationCode(url):
    from PIL import Image

    im = Image.open(url)
    im = im.convert("L")
    # im.show()

    threshold = 140
    table = []
    for i in range(256):
        if i< threshold:
            table.append(0)
        else:
            table.append(1)

    s = image_to_string(im)
    # s = s.split("\n")[3]
    group = re.findall('\w',s)
    text = ""
    for i in range(len(group)):
        text = text + group[i]
    return text.strip()

# getVerificationCode("C:/Users/use/Desktop/screenshot.jpg")