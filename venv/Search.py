# 제목: 도서 검색 API 활용하여 도서 정보 출력

# import
import urllib.request
import json


def searchbook(title):
    # 애플리케이션 클라이언트 id 및 secret
    client_id = "[WkXXvPGDCEbtWlp9N8sY]"
    client_secret = "[RX3NPPjkkv]"

    # 도서검색 url
    url = "https://openapi.naver.com/v1/search/book.json"
    option = "&display=3&sort=count"
    query = "?query=" + urllib.parse.quote(title)
    url_query = url + query + option

    # Open API 검색 요청 개체 설정
    request = urllib.request.Request(url_query)
    request.add_header("WkXXvPGDCEbtWlp9N8sY", client_id)
    request.add_header("RX3NPPjkkv", client_secret)

    # 검색 요청 및 처리
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode == 200):
        return response.read().decode('utf-8')
    else:
        return None


# 검색 결과 항목 정보 출력하기
def showitem(item):
    print("제목:" + item['title'])
    print("설명:" + item['description'])
    print("url:" + item['link'])
    print("================")


# 프로그램 진입점
def main():
    # 검색 질의 요청
    res = searchbook(input("질의:"))
    if (res == None):
        print("검색 실패!!!")
        exit()
    # 검색 결과를 json개체로 로딩
    jres = json.loads(res)
    if (jres == None):
        print("json.loads 실패!!!")
        exit()

    # 검색 결과의 items 목록의 각 항목(post)을 출력
    for post in jres['items']:
        showitem(post)


# 진입점 함수를 main으로 지정
if __name__ == '__main__':
    main()