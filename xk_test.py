import ddddocr


ocr=ddddocr.DdddOcr()
with open('验证码.jpg','rb') as f:
    code_bytes=f.read()
code=ocr.classification(code_bytes)
print(code)