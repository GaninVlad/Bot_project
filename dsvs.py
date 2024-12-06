import csv
import sys

a = sys.stdin.readlines()
stroka = ''
spisok = []
for i in a:
    stroka = i[:-1].split(': ')
    stroka[0], stroka[1] = stroka[1], stroka[0]
    stroka.append(str(((len(stroka[0]) + int(stroka[2])) // 2)))
    stroka = '.'.join(stroka)
    spisok.append(stroka)
f = open('troll_sun.csv', mode='w', encoding='utf-8')
f.write('no.place.name.gold.importance')
for i in range(len(spisok)):
    if i < 4:
        print(i, spisok[i])
        f.write(f'{i + 1}.{spisok[i]}')