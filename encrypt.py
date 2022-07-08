from Crypto.Cipher import AES
import base64


class Encrypt:
    def __init__(self, key):
        self.key = key.encode('utf-8')

    # @staticmethod
    def pkcs7padding(self, text):
        """明文使用PKCS7填充 """
        bs = 16
        length = len(text)
        bytes_length = len(text.encode('utf-8'))
        padding_size = length if (bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        padding_text = chr(padding) * padding
        self.coding = chr(padding)
        return text + padding_text

    def aes_encrypt(self, content):
        """ AES加密 """
        cipher = AES.new(self.key, AES.MODE_ECB)
        # 处理明文
        content_padding = self.pkcs7padding(content)
        # 加密
        encrypt_bytes = cipher.encrypt(content_padding.encode('utf-8'))
        # 重新编码
        result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
        return result


    def aes_decrypt(self, content):
        # 不可用，有报错
        """AES解密 """
        cipher = AES.new(self.key, AES.MODE_CBC)
        content = base64.b64decode(content)
        text = cipher.decrypt(content)
        text = base64.b64encode(text).decode('utf-8')
        return text.rstrip(self.coding)


def AES_encrypt(text):
    key = 'MWMqg2tPcDkxcm11'  # 密钥
    a = Encrypt(key=key)
    e = a.aes_encrypt(text)
    return e


if __name__ == '__main__':
    key = 'MWMqg2tPcDkxcm11'            #密钥
    content = 'zyx/020305'              #密码明文

    a = Encrypt(key=key)
    e = a.aes_encrypt(content)
    # d = a.aes_decrypt(e)
    print("加密:", e)
    # print("解密:", d)

