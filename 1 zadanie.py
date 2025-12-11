import datetime


def a(spisok):
    for i in range(0, len(spisok), 3):
        data = spisok[i + 1].split('.')
        day = int(data[0])
        month = int(data[1])
        year = datetime.datetime.now().year
        dr = datetime.datetime(year, month, day)
        if datetime.datetime.now().month - month < 0:
            dr = datetime.date(year, month + 12, day)
            print(spisok[i], spisok[i + 1], spisok[i + 2], datetime.datetime.now() - dr)
        print(spisok[i], spisok[i + 1], spisok[i + 2], datetime.datetime.now() - dr)



(a(['РАсул', '12.10.2000', '1234567890', 'LNBls b', '12.08.2005', '8885352523']))