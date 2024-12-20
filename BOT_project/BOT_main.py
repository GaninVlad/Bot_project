import logging
import sqlite3
import requests
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session import aiohttp
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram import Dispatcher, Bot, F

bot = Bot(token='7077172699:AAF2s68YdFofxNpLJ-KXoe1bjOhFjHTVtWY', default=DefaultBotProperties())
logger = logging.getLogger(__name__)
dp = Dispatcher()
button_1 = KeyboardButton(text='/start')
button_2 = KeyboardButton(text='/help')
button_3 = KeyboardButton(text='/lists_of_classes')
button_4 = KeyboardButton(text='/schedules_of_classes')
button_5 = KeyboardButton(text='/maps_of_schools')
button_6 = KeyboardButton(text='/change_list_class_1')
button_7 = KeyboardButton(text='/change_list_class_2')
button_8 = KeyboardButton(text='/change_list_class_3')
keyboard = ReplyKeyboardMarkup(keyboard=[[button_1, button_2],
                                         [button_3, button_4, button_5],
                                         [button_6, button_7, button_8]])
klass_1_but = InlineKeyboardButton(text='Список 1 класса', callback_data='list_class1')
klass_2_but = InlineKeyboardButton(text='Список 2 класса', callback_data='list_class2')
klass_3_but = InlineKeyboardButton(text='Список 3 класса', callback_data='list_class3')
keyboard_klasses = InlineKeyboardMarkup(
    inline_keyboard=[[klass_1_but],
                     [klass_2_but],
                     [klass_3_but]])
schedule_but_1 = InlineKeyboardButton(text='Расписание 1 класса', callback_data='schedule_class1')
schedule_but_2 = InlineKeyboardButton(text='Расписание 2 класса', callback_data='schedule_class2')
schedule_but_3 = InlineKeyboardButton(text='Расписание 3 класса', callback_data='schedule_class3')
keyboard_schedules = InlineKeyboardMarkup(
    inline_keyboard=[[schedule_but_1],
                     [schedule_but_2],
                     [schedule_but_3]])
mapLiceum1_but = InlineKeyboardButton(text='Местоположение Лицея№1', callback_data='map_Liceum1')
mapLiceum2_but = InlineKeyboardButton(text='Местоположение Лицея№2', callback_data='map_Liceum2')
mapGimnazia1_but = InlineKeyboardButton(text='Местоположение Гимназии№1', callback_data='map_Gimnazia1')
mapGimnazia2_but = InlineKeyboardButton(text='Местоположение Гимназии№2', callback_data='map_Gimnazia2')
mapGimnazia3_but = InlineKeyboardButton(text='Местоположение Гимназии№3', callback_data='map_Gimnazia3')
mapschool4_but = InlineKeyboardButton(text='Местоположение СОШ№4', callback_data='map_school4')
mapschool16_but = InlineKeyboardButton(text='Местоположение СОШ№16', callback_data='map_school16')
keyboard_of_maps = InlineKeyboardMarkup(
    inline_keyboard=[[mapLiceum1_but, mapLiceum2_but],
                     [mapGimnazia1_but, mapGimnazia2_but],
                     [mapGimnazia3_but, mapschool4_but],
                     [mapschool16_but]])
res_str = ''
flag = 0
pass


def geocode(address):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": '40d1649f-0493-4b70-98ba-98533de7710b',
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_request, params=geocoder_params)

    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            f"""Ошибка выполнения запроса:
            {geocoder_request}
            Http статус: {response.status_code} ({response.reason})""")
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


def get_ll_spn(address):
    toponym = geocode(address)
    if not toponym:
        return (None, None)

    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])
    envelope = toponym["boundedBy"]["Envelope"]
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0
    span = f"{dx},{dy}"
    return ll, span


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Здравствуйте я бот-помощник учителям, выберите нужную опцию', reply_markup=keyboard)


@dp.message(Command(commands=['help']))
async def help(message: Message):
    await message.answer('/lists_of_classes - вызывает несколько кнопок с выбором списка одного из классов\n'
                         '/schedules_of_classes - вызывает несколько кнопок с выбором расписания одного из классов\n'
                         '/maps_of_schools - вызывает несколько кнопок с выбором местоположения одной из школ Чистополя\n'
                         '/change_list_class_1 - изменение списка учеников 1 класса\n'
                         '/change_list_class_2 - изменение списка учеников 2 класса\n'
                         '/change_list_class_3 - изменение списка учеников 3 класса', reply_markup=keyboard)


@dp.callback_query(F.data == 'list_class1')
async def spisok_class_1(callback: CallbackQuery):
    query = """SELECT id, Student FROM Class1 WHERE id BETWEEN 0 AND 24"""
    con = sqlite3.connect('project_bd.sqlite')
    cur = con.cursor()
    result = cur.execute(query).fetchall()
    f = open('bot.txt', mode='w', encoding='utf8')
    stroka = ''
    for i in result:
        stroka = str(i[0]) + ' - ' + i[1]
        f.write(f'{stroka}\n')
    f = open('bot.txt', mode='r+', encoding='utf8')
    a = f.read()
    f.truncate(0)
    await callback.message.answer(a)


@dp.callback_query(F.data == 'list_class2')
async def spisok_class_1(callback: CallbackQuery):
    query = """SELECT id, Student FROM Class2 WHERE id BETWEEN 0 AND 24"""
    con = sqlite3.connect('project_bd.sqlite')
    cur = con.cursor()
    result = cur.execute(query).fetchall()
    f = open('bot.txt', mode='w', encoding='utf8')
    stroka = ''
    for i in result:
        stroka = str(i[0]) + ' - ' + i[1]
        f.write(f'{stroka}\n')
    f = open('bot.txt', mode='r+', encoding='utf8')
    a = f.read()
    f.truncate(0)
    await callback.message.answer(a)


@dp.callback_query(F.data == 'list_class3')
async def spisok_class_1(callback: CallbackQuery):
    query = """SELECT id, Student FROM Class3 WHERE id BETWEEN 0 AND 24"""
    con = sqlite3.connect('project_bd.sqlite')
    cur = con.cursor()
    result = cur.execute(query).fetchall()
    f = open('bot.txt', mode='w', encoding='utf8')
    stroka = ''
    for i in result:
        stroka = str(i[0]) + ' - ' + i[1]
        f.write(f'{stroka}\n')
    f = open('bot.txt', mode='r+', encoding='utf8')
    a = f.read()
    f.truncate(0)
    await callback.message.answer(a)


@dp.message(Command(commands=['change_list_class_1']))
async def change_spisok_class_1(message: Message):
    global flag
    flag = 1
    await message.answer('Введите номер ученика от 1 до 18 и его фамилию и имя через дефис, без пробелов')


@dp.message(Command(commands=['change_list_class_2']))
async def change_spisok_class_2(message: Message):
    global flag
    flag = 2
    await message.answer('Введите номер ученика от 1 до 18 и его фамилию и имя через дефис, без пробелов')


@dp.message(Command(commands=['change_list_class_3']))
async def change_spisok_class_3(message: Message):
    global flag
    flag = 3
    await message.answer('Введите номер ученика от 1 до 18 и его фамилию и имя через дефис, без пробелов')


@dp.message(Command(commands=['lists_of_classes']))
async def lists_of_classes(message: Message):
    await message.answer('Выберите пункт, который хотите увидеть', reply_markup=keyboard_klasses)


@dp.callback_query(F.data == 'schedule_class1')
async def spisok_class_1(callback: CallbackQuery):
    query = """SELECT Понедельник, Вторник, Среда, Четверг, Пятница, Суббота  FROM Schedule_class1 WHERE id BETWEEN 0 AND 7"""
    con = sqlite3.connect('project_bd.sqlite')
    cur = con.cursor()
    result = cur.execute(query).fetchall()
    f = open('bot.txt', mode='w', encoding='utf8')
    week = ['Понедельник: ', 'Вторник: ', 'Среда: ', 'Четверг: ', 'Пятница: ', 'Суббота: ']
    res = ''
    for i in range(len(result) - 1):
        stroka = ''
        for j in range(7):
            stroka += f'{result[j][i]}\n'
        res += f'{week[i]}\n{stroka}\n'
    f.write(res)
    f = open('bot.txt', mode='r+', encoding='utf8')
    a = str(f.read())
    f.truncate(0)
    await callback.message.answer(a)


@dp.callback_query(F.data == 'schedule_class2')
async def schedule_class_2(callback: CallbackQuery):
    query = """SELECT Понедельник, Вторник, Среда, Четверг, Пятница, Суббота  FROM Schedule_class2 WHERE id BETWEEN 0 AND 7"""
    con = sqlite3.connect('project_bd.sqlite')
    cur = con.cursor()
    result = cur.execute(query).fetchall()
    f = open('bot.txt', mode='w', encoding='utf8')
    week = ['Понедельник: ', 'Вторник: ', 'Среда: ', 'Четверг: ', 'Пятница: ', 'Суббота: ']
    res = ''
    for i in range(len(result) - 1):
        stroka = ''
        for j in range(7):
            stroka += f'{result[j][i]}\n'
        res += f'{week[i]}\n{stroka}\n'
    f.write(res)
    f = open('bot.txt', mode='r+', encoding='utf8')
    a = str(f.read())
    f.truncate(0)
    await callback.message.answer(a)


@dp.callback_query(F.data == 'schedule_class3')
async def schedule_class_3(callback: CallbackQuery):
    query = """SELECT Понедельник, Вторник, Среда, Четверг, Пятница, Суббота  FROM Schedule_class3 WHERE id BETWEEN 0 AND 7"""
    con = sqlite3.connect('project_bd.sqlite')
    cur = con.cursor()
    result = cur.execute(query).fetchall()
    f = open('bot.txt', mode='w', encoding='utf8')
    week = ['Понедельник: ', 'Вторник: ', 'Среда: ', 'Четверг: ', 'Пятница: ', 'Суббота: ']
    res = ''
    for i in range(len(result) - 1):
        stroka = ''
        for j in range(7):
            stroka += f'{result[j][i]}\n'
        res += f'{week[i]}\n{stroka}\n'
    f.write(res)
    f = open('bot.txt', mode='r+', encoding='utf8')
    a = str(f.read())
    f.truncate(0)
    await callback.message.answer(a)


@dp.message(Command(commands=['schedules_of_classes']))
async def schedules_of_classes(message: Message):
    await message.answer('Выберите пункт, который хотите увидеть', reply_markup=keyboard_schedules)


@dp.callback_query(F.data == 'map_Liceum1')
async def map_Liceum1(callback: CallbackQuery):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": 'Чистополь,+улица+Льва+Толстого+144'
    })
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn('Чистополь,+улица+Льва+Толстого+144')
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.005,0.002&l=map"
    await callback.message.bot.send_photo(
        callback.message.chat.id, static_api_request,
        caption=f"Нашёл: https://yandex.ru/maps/11129/chistopol/house/ulitsa_lva_tolstogo_144/YUkYcANhSUMOQFtvfX92c35hZg==/?ll=50.642229%2C55.371758&z=17")


@dp.callback_query(F.data == 'map_Liceum2')
async def map_Liceum2(callback: CallbackQuery):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": 'Чистополь,+улица+Полющенкова+28+Б'
    })
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn('Чистополь,+улица+Полющенкова+28+Б')
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.005,0.002&l=map"
    await callback.message.bot.send_photo(
        callback.message.chat.id, static_api_request,
        caption=f"Нашёл: https://yandex.ru/maps/11129/chistopol/house/ulitsa_polyushchenkova_28b/YUkYcw9gS00HQFtvfX90eXhmbA==/?ll=50.581679%2C55.358244&z=17.55")


@dp.callback_query(F.data == 'map_Gimnazia1')
async def map_Gimnazia1(callback: CallbackQuery):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": 'Чистополь,+улица+Бебеля+121'
    })
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn('Чистополь,+улица+Бебеля+121')
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.005,0.002&l=map"
    await callback.message.bot.send_photo(
        callback.message.chat.id, static_api_request,
        caption=f"Нашёл: https://yandex.ru/maps/11129/chistopol/house/ulitsa_bebelya_121/YUkYcANiTUYDQFtvfX93eHtqYw==/?ll=50.642940%2C55.369958&z=17.6")


@dp.callback_query(F.data == 'map_Gimnazia2')
async def map_Gimnazia2(callback: CallbackQuery):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": 'Чистополь,+улица+Нариманова+65'
    })
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn('Чистополь,+улица+Нариманова+65')
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.005,0.002&l=map"
    await callback.message.bot.send_photo(
        callback.message.chat.id, static_api_request,
        caption=f"Нашёл: https://yandex.ru/maps/11129/chistopol/house/ulitsa_narimanova_65/YUkYcANmQUQPQFtvfX93d35kYw==/?ll=50.647368%2C55.366273&z=18.22")


@dp.callback_query(F.data == 'map_Gimnazia3')
async def map_Gimnazia3(callback: CallbackQuery):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": 'Чистополь,+улица+Академика+Королёва+5'
    })
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn('Чистополь,+улица+Академика+Королёва+5')
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.005,0.002&l=map"
    await callback.message.bot.send_photo(
        callback.message.chat.id, static_api_request,
        caption=f"Нашёл: https://yandex.ru/maps/11129/chistopol/house/ulitsa_akademika_korolyova_5/YUkYcw5nSUwBQFtvfX93c35rYg==/?ll=50.598515%2C55.362284&z=18.53")


@dp.callback_query(F.data == 'map_school16')
async def map_school16(callback: CallbackQuery):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": 'Чистополь,+улица+Зелёная+2+А'
    })
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn('Чистополь,+улица+Зелёная+2+А')
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.005,0.002&l=map"
    await callback.message.bot.send_photo(
        callback.message.chat.id, static_api_request,
        caption=f"Нашёл: https://yandex.ru/maps/11129/chistopol/house/zelyonaya_ulitsa_2a/YUkYcAZpSUQCQFtvfX93d3tmZw==/?ll=50.619704%2C55.366213&z=18.16")


@dp.callback_query(F.data == 'map_school4')
async def map_school4(callback: CallbackQuery):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": 'Чистополь,+улица+Бутлерова+7+А'
    })
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn('Чистополь,+улица+Бутлерова+7+А')
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.005,0.002&l=map"
    await callback.message.bot.send_photo(
        callback.message.chat.id, static_api_request,
        caption=f"Нашёл: https://yandex.ru/maps/11129/chistopol/house/ulitsa_butlerova_7a/YUkYcAFgQEEHQFtvfX95cXhlYw==/?ll=50.661501%2C55.380375&z=17.27")


@dp.message(Command(commands=['maps_of_schools']))
async def schedules_of_classes(message: Message):
    await message.answer('Выберите пункт, который хотите увидеть', reply_markup=keyboard_of_maps)


@dp.message()
async def record(message: Message):
    global flag
    msg = ''
    for i in range(1, 55):
        if f'{i}-' in message.text:
            mess = message.text.split('-')[1]
            for p in mess.split():
                if p.isalpha():
                    if len(mess.split()) == 2:
                        for j in '1234567890':
                            if j not in message.text.split('-')[1]:
                                msg = message.text
                                break
                            else:
                                await message.answer('Не используйте цифры в фамилии и имени')
                    else:
                        await message.answer('Введите ТОЛЬКО фамилию и имя')
                else:
                    await message.answer('Введите правильные фамилию и имя')
    msg = msg.split('-')
    number = msg[0]
    name = msg[1]
    if flag == 1:
        query = f"""UPDATE Class1 SET Student = '{name}' WHERE id = '{number}'"""
        con = sqlite3.connect('project_bd.sqlite')
        cur = con.cursor()
        result = cur.execute(query).fetchall()
        con.commit()
    elif flag == 2:
        query = f"""UPDATE Class2 SET Student = '{name}' WHERE id = '{number}'"""
        con = sqlite3.connect('project_bd.sqlite')
        cur = con.cursor()
        result = cur.execute(query).fetchall()
        con.commit()
    elif flag == 3:
        query = f"""UPDATE Class3 SET Student = '{name}' WHERE id = '{number}'"""
        con = sqlite3.connect('project_bd.sqlite')
        cur = con.cursor()
        result = cur.execute(query).fetchall()
        con.commit()
    await message.answer('Изменение выполнено успешно')
    print(message.text)


async def get_response(url, params):
    logger.info(f"getting {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start', description='Начать работу с ботом'),
        BotCommand(command='/help', description='Справка'),
        BotCommand(command='/lists_of_classes', description='Узнать список одного из 3 классов'),
        BotCommand(command='/schedules_of_classes', description='Узнать расписание одного из 3 классов'),
        BotCommand(command='/maps_of_schools', description='Узнать местоположения одной из школ Чистополя')]
    await bot.set_my_commands(main_menu_commands)


if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)