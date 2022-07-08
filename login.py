import requests
import json
import base64
import matplotlib.pyplot as plt
import ddddocr
from encrypt import AES_encrypt


def ocr_captcha():
    """
    :return: 识别到的验证码
    """
    ocr=ddddocr.DdddOcr()
    with open('验证码.jpg','rb') as f:
        code_bytes=f.read()
    return ocr.classification(code_bytes)


def get_captcha(conf):
    """
    :param conf: conf.json
    :return: code & uuid
    """
    url = "https://xk.xidian.edu.cn/xsxk/auth/captcha"
    p = requests.post(url)
    with open("captcha_pac.json", "wb") as f:
        f.write(p.content)      # 保存为json文件
    with open("captcha_pac.json", 'r') as f:
        result = json.load(f)   # 获得返回的json
    print(result['code'])   #打印返回值,成功是200

    # print("uuid:", result['data']['uuid'])

    pic = result['data']['captcha'].replace("data:image/png;base64,", "")  # 保存验证码为图片
    b = base64.b64decode(pic)
    with open('验证码.jpg', 'wb') as f:
        f.write(b)

    if conf["ocr_captcha"] == "1":      # 默认， 自动识别验证码
        code = ocr_captcha()
        print("验证码为:", code)
    else:                               #手动输入
        img = plt.imread('验证码.jpg')
        plt.imshow(img)
        plt.show()                      # 显示验证码
        code = input("请输入验证码:")

    # print("captcha:", result['data']['captcha'])
    # print("uuid:", result['data']['uuid'])

    return code, result['data']['uuid']


def login(conf):
    """
    :param conf: conf.json
    :return: 登录后返回的json
    """
    url = "https://xk.xidian.edu.cn/xsxk/auth/login"

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44",
    }

    form = conf["data"]
    if conf["data"]["loginname"] == "" or conf["data"]["password"] == "":   # 如果缺少 用户名 和 密码
        form["loginname"] = input("学号：")
        form["password"] = input("密码：")
    form["password"] = AES_encrypt(form["password"])
    form["captcha"], form["uuid"] = get_captcha(conf)   # 构造表单

    p = requests.post(url, header, params=form)
    with open("login_pac.json", "wb") as f:
        f.write(p.content)      # 字节形式写入，保存为json文件
    # print(p.text)

    with open("login_pac.json", 'r', encoding="utf-8") as f:
        result = json.load(f)   # 加载返回的json
    return result


def show_msg(json):
    """
    :param json:    登录成功后返回的json
    :return:        NONE
    """
    try:
        print("姓名：", json["data"]["student"]["XM"])
        print("专业：", json["data"]["student"]["ZYMC"])
        print("班级：", json["data"]["student"]["schoolClass"])
        lst = json["data"]["student"]["electiveBatchList"]
        for i in lst:
            print("选课批次：", i["name"], "\t是否可选：", i["canSelect"])
    except TypeError:
        print(json["msg"])


if __name__ == '__main__':
    pass
