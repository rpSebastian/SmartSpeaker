# coding:utf-8
# created by wuxh @ 2018-05-06

import random
import base64
from Crypto.Cipher import AES
import sys
import json
import urllib2
import urllib
#---
#--- @music.163.com
#--- get postData "params and encSeckeys"

modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'
url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="

def getRandom():
    string = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""
    for i in range(16):
        res += string[int(random.random()*62)]
    return res

def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext).decode("utf-8")
    return ciphertext

def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(text.encode('hex'), 16)**int(pubKey, 16)%int(modulus, 16)
    return format(rs, 'x').zfill(256)

def getParam(text):
    secKey = getRandom()
    params = aesEncrypt(aesEncrypt(text,secKey),nonce)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    return params , encSecKey

HEADER = {}
def setHeader():
    HEADER = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'music.163.com',
        'Referer': 'https://music.163.com/search/',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
    }

def search(s,type,offset):
    text = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "#/discover": "", "s": s, "type": type,"offset": offset, "total": "true", "limit": "30", "csrf_token": ""}
    secKey = getRandom()
    text = json.dumps(text)
    params = aesEncrypt(aesEncrypt(text,nonce),secKey)
    encSecKey = rsaEncrypt(secKey,pubKey,modulus)
    data =  "params="+urllib2.quote(params)+"&encSecKey="+urllib2.quote(encSecKey)
    req = urllib2.Request(url,data=data.encode("utf-8"),headers=HEADER)
    return urllib2.urlopen(req).read()



if __name__ == "__main__":
    setHeader()
    # search(sys.argv[0],sys.argv[1],sys.argv[2])
    print search("林俊杰","1","0")
    # text = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "#/discover": "", "s": "刘德华", "type": "1","offset": "0", "total": "true", "limit": "30", "csrf_token": ""}
    # secKey = getRandom()
    # text = json.dumps(text)
    #
    # params = aesEncrypt(aesEncrypt(text,nonce),secKey)
    # encSecKey = rsaEncrypt(secKey,pubKey,modulus)
    # print(params)
    # print(encSecKey)
    # print( "params="+urllib2.quote(params)+"&encSecKey="+urllib2.quote(encSecKey))

