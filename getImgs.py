import requests as r
import shutil

def getImg(num):
    for i in range(num):
        print i
        url = "C:/Users/use/Desktop/SampleImg/{}.jpg".format(i)
        res = r.get("https://netbank.jihsunbank.com.tw/include/dvcode.asp", stream=True, verify=False)
        file = open(url, "wb")
        shutil.copyfileobj(res.raw, file)
        file.close()

getImg(10000)
