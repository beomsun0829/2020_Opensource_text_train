import urllib.request
import json,pprint
from tkinter import *
from tkinter import messagebox

def translate():
    # 번역할 txt파일 내용 불러와서 읽기
    with open('source.txt', 'r', encoding='utf8') as memo:
        text = memo.read()

    # 번역할 내용을 txt파일로 읽어서 받아옴
    encText = urllib.parse.quote(text)
    # 한영번역
    # data = "source=ko&target=en&text=" + encText
    # 영한번역
    data = "source=en&target=ko&text=" + encText

    # 개발자센터에서 발급받은 값
    client_id = "uucszwBYG7Kx3m68gu8Y"
    client_secret = "ARQJd5IcAh"

    ##번역시작코드
    # 웹요청
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    # 결과 받아오는 부분
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))

    # 응답이 성공적일때
    rescode = response.getcode()
    # 성공
    if (rescode == 200):
        response_body = response.read()
        txt = response_body.decode('utf-8')
        # 응답데이터 형 변환, 딕셔너리화
        txt = json.loads(txt)
        # pprint 이용해서 출력 변경
        pprint.pprint(txt)

        # 수정 후 메모장 파일 생성
        with open('translate.txt', 'w', encoding='utf8') as memo:
            memo.write(txt['message']['result']['translatedText'])

        messagebox.showinfo("번역", txt['message']['result']['translatedText'])
    # 실패
    else:
        print("Error Code:" + rescode)

translate()