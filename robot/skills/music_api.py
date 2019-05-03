import requests
import random
import base64
from Crypto.Cipher import AES
import sys
import json
import binascii
import urllib

class Music_api():
    def __init__(self):
        self.modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pubKey = '010001'
        self.url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="
        self.HEADER = {}
        self.setHeader()
        self.secKey = self.getRandom()

    def getRandom(self):
        string = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        res = ""
        for i in range(16):
            res += string[int(random.random()*62)]
        return res

    def aesEncrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(secKey, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext).decode("utf-8")
        return ciphertext

    def quickpow(self, x, y, mo):
        res = 1
        while y:
            if y & 1:
                res = res * x % mo
            y = y // 2
            x = x * x % mo
        return res 

    def rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        a = int(binascii.hexlify(str.encode(text)), 16)
        b = int(pubKey, 16)
        c = int(modulus, 16)
        rs = self.quickpow(a, b, c)
        return format(rs, 'x').zfill(256)

    def setHeader(self):
        self.HEADER = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'https://music.163.com/search/',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
        }

    def search(self, s,offset,type="1"):
        text = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "#/discover": "", "s": s, "type": type,"offset": offset, "total": "true", "limit": "30", "csrf_token": ""}
        text = json.dumps(text)
        params = self.aesEncrypt(self.aesEncrypt(text,self.nonce),self.secKey)
        encSecKey = self.rsaEncrypt(self.secKey,self.pubKey,self.modulus)
        data = {
            'params': params,
            'encSecKey': encSecKey
        }
        result = requests.post(url=self.url, data=data, headers = self.HEADER).json()
        return result

    def get_music_list(self, keywords):
        music_list = []
        for offset in range(1):
            result = Music_api().search(keywords, str(offset))
            result = result['result']['songs']
            for music in result:
                # if music['copyright'] == 1 and music['fee'] == 8:
                if music['fee'] == 8:
                    music_list.append(music)
        return music_list

# print(Music_api().get_music_list("像我这样的人"))