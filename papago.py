import os
import sys
import urllib.request
import json

#번역할 메모장파일 내용 불러와서 읽기
with open('source.txt','r',encoding='utf8') as memo:
    text = memo.read()

encText = urllib.parse.quote(text)
#data = "source=ko&target=en&text=" + encText#한영번역
data = "source=en&target=ko&text=" + encText#영한번역

#네이버 파파고 API 이용
url = "https://openapi.naver.com/v1/papago/n2mt"
request = urllib.request.Request(url)
client_id = "uucszwBYG7Kx3m68gu8Y"
client_secret = "ARQJd5IcAh"
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request, data=data.encode("utf-8"))
rescode = response.getcode()

if(rescode==200):
    response_body = response.read()

    #json 형 변환
    res = json.loads(response_body.decode('utf-8'))
    from pprint import pprint  #pprint 모듈 이용해서 결과값만 출력시키기
    pprint(res)

    #수정 후 메모장 파일 생성
    with open('translate.txt', 'w',encoding='utf8') as memo:
        memo.write(res['message']['result']['translatedText'])#결과값만 사용
else:
    print("Error Code:" + rescode)