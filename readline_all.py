f = open("./크롤링.txt", 'r', encoding='UTF-8')
while True:
    line = f.readline()
    if not line: break
    print(line)
f.close()