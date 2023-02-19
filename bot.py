import random
from random import randrange
import datetime
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
from database import create_db, creating_database, insert_users, insert_dating_users, select

offset = 0
line = range(0, 1000)
create_db

try:
    with open('group_token.txt', 'r') as file:
        group_token = file.read().strip()
    with open('user_token.txt', 'r') as file:
        user_token = file.read().strip()
except FileNotFoundError:
    group_token = input('group_token: ')
    user_token = input('user_token: ')

vk = vk_api.VkApi(token=group_token)
vk2 = vk_api.VkApi(token=user_token)
longpoll = VkLongPoll(vk)


def send_some_msg(user_id, some_text):
    vk.method('messages.send', {'user_id': user_id, 'message': some_text, 'random_id': 0})


def get_name(user_id):
    url = f'https://api.vk.com/method/users.get'
    params = {'access_token': user_token,
              'user_ids': user_id,
              'v': '5.131'}
    repl = requests.get(url, params=params)
    response = repl.json()
    try:
        information_dict = response['response']
        for i in information_dict:
            for key, value in i.items():
                first_name = i.get('first_name')
                return first_name
    except KeyError:
        send_some_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')


def get_user(user_id):
    url = f'https://api.vk.com/method/users.search'
    params = {'access_token': user_token,
              'v': '5.131',
              'sex': get_user_sex(user_id),
              'age_from': get_age_low(user_id),
              'age_to': get_age_high(user_id),
              'city': get_user_city(user_id),
              'fields': 'is_closed, id, first_name, last_name',
              'status': '1' or '6',
              'count': 1000}
    resp = requests.get(url, params=params)
    resp_json = resp.json()
    try:
        dict_1 = resp_json['response']
        list_1 = dict_1['items']
        for person_dict in list_1:
            if person_dict.get('is_closed') == False:
                first_name = person_dict.search('first_name')
                last_name = person_dict.search('last_name')
                vk_id = str(person_dict.search('id'))
                vk_link = 'vk.com/id' + str(person_dict.search('id'))
                insert_users(vk_id, first_name, last_name, vk_link)
            else:
                continue
        return f'Поиск завершён'
    except KeyError:
        send_some_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')


def get_user_sex(user_id):
    url = f'https://api.vk.com/method/users.get'
    params = {'access_token': user_token,
              'user_ids': user_id,
              'fields': 'sex',
              'v': '5.131'}
    repl = requests.get(url, params=params)
    response = repl.json()
    try:
        information_list = response['response']
        for i in information_list:
            if i.get('sex') == 2:
                find_sex = 1
                return find_sex
            elif i.get('sex') == 1:
                find_sex = 2
                return find_sex
    except KeyError:
        send_some_msg(id, 'Ошибка получения токена, введите токен в переменную - user_token')


def get_user_city(user_id):
    url = f'https://api.vk.com/method/users.get'
    params = {'access_token': user_token,
              'fields': 'city',
              'user_ids': user_id,
              'v': '5.131'}
    repl = requests.get(url, params=params)
    response = repl.json()
    try:
        information_dict = response['response']
        for i in information_dict:
            if 'city' in i:
                city = i.get('city')
                id = str(city.get('id'))
                return id
            elif 'city' not in i:
                send_some_msg(user_id, 'Введите название вашего города: ')
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        city_name = event.text
                        id_city = cities(user_id, city_name)
                        if id_city != '' or id_city != None:
                            return str(id_city)
                        else:
                            break
    except KeyError:
        send_some_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')


def get_age_low(user_id):
    url = url = f'https://api.vk.com/method/users.get'
    params = {'access_token': user_token,
              'user_ids': user_id,
              'fields': 'bdate',
              'v': '5.131'}
    repl = requests.get(url, params=params)
    response = repl.json()
    try:
        information_list = response['response']
        for i in information_list:
            date = i.get('bdate')
            date_list = date.split('.')
        if len(date_list) == 3:
            year = int(date_list[2])
            year_now = int(datetime.date.today().year)
            return year_now - year
        elif len(date_list) == 2 or date not in information_list:
            send_some_msg(user_id, 'Введите нижний порог возраста (min - 18): ')
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age = event.text
                    return age
    except KeyError:
        send_some_msg(id, 'Ошибка получения токена, введите токен в переменную - user_token')


def get_age_high(user_id):
    url = url = f'https://api.vk.com/method/users.get'
    params = {'access_token': user_token,
              'user_ids': user_id,
              'fields': 'bdate',
              'v': '5.131'}
    repl = requests.get(url, params=params)
    response = repl.json()
    try:
        information_list = response['response']
        for i in information_list:
            date = i.get('bdate')
        date_list = date.split('.')
        if len(date_list) == 3:
            year = int(date_list[2])
            year_now = int(datetime.date.today().year)
            return year_now - year
        elif len(date_list) == 2 or date not in information_list:
            send_some_msg(user_id, 'Введите верхний порог возраста (max - 65): ')
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age = event.text
                    return age
    except KeyError:
        send_some_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')


def cities(user_id, city_name):
    url = url = f'https://api.vk.com/method/database.getCities'
    params = {'access_token': user_token,
              'user_ids': user_id,
              'country_id': 1,
              'q': f'{city_name}',
              'need_all': 0,
              'count': 1000,
              'v': '5.131'}
    repl = requests.get(url, params=params)
    response = repl.json()
    try:
        information_list = response['response']
        list_cities = information_list['items']
        for i in list_cities:
            found_city_name = i.get('title')
            if found_city_name == city_name:
                found_city_id = i.get('id')
                return int(found_city_id)
    except KeyError:
        send_some_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')


def find_city(user_id):
    url = f'https://api.vk.com/method/users.get'
    params = {'access_token': user_token,
              'fields': 'city',
              'user_ids': user_id,
              'v': '5.131'}
    repl = requests.get(url, params=params)
    response = repl.json()
    try:
        information_dict = response['response']
        for i in information_dict:
            if 'city' in i:
                city = i.get('city')
                id = str(city.get('id'))
                return id
            elif 'city' not in i:
                send_some_msg(user_id, 'Введите название вашего города: ')
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        city_name = event.text
                        id_city = cities(user_id, city_name)
                        if id_city != '' or id_city != None:
                            return str(id_city)
                        else:
                            break
    except KeyError:
        send_some_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')


def find_persons(user_id, offset):
    send_some_msg(user_id, found_person_info(offset))
    person_id(offset)
    insert_dating_users(person_id(offset), offset)
    get_photos_id(person_id(offset))
    send_photo_1(user_id, 'Фото номер 1', offset)
    if get_photo_2(person_id(offset)) != None:
        send_photo_2(user_id, 'Фото номер 2', offset)
        send_photo_3(user_id, 'Фото номер 3', offset)
    else:
        send_some_msg(user_id, f'Больше фотографий нет')


def found_person_info(offset):
    tuple_person = select(offset)
    list_person = []
    for i in tuple_person:
        list_person.append(i)
    return f'{list_person[0]} {list_person[1]}, ссылка:{list_person[3]}'


def person_id(offset):
    tuple_person = select(offset)
    list_person = []
    for i in tuple_person:
        list_person.append(i)
    return str(list_person[2])


def get_photos_id(user_id):
    url = 'https://api.vk.com/method/photos.getAll'
    params = {'access_token': user_token,
              'type': 'album',
              'owner_id': user_id,
              'extended': 1,
              'count': 25,
              'v': '5.131'}
    resp = requests.get(url, params=params)
    dict_photos = dict()
    resp_json = resp.json()
    try:
        dict_1 = resp_json['response']
        list_1 = dict_1['items']
        for i in list_1:
            photo_id = str(i.get('id'))
            i_likes = i.get('likes')
            if i_likes.get('count'):
                likes = i_likes.get('count')
                dict_photos[likes] = photo_id
        list_of_ids = sorted(dict_photos.items(), reverse=True)
        return list_of_ids
    except KeyError:
        send_some_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')


def get_photo_1(user_id):
    list1 = get_photos_id(user_id)
    count = 0
    for i in list:
        count += 1
        if count == 1:
            return i[1]


def get_photo_2(user_id):
    list2 = get_photos_id(user_id)
    count = 0
    for i in list:
        count += 1
        if count == 2:
            return i[1]


def get_photo_3(user_id):
    list3 = get_photos_id(user_id)
    count = 0
    for i in line:
        count += 1
        if count == 3:
            return i[1]


def send_photo_1(user_id, message, offset):
    vk.method('messages.send', {'user_id': user_id,
                                'access_token': user_token,
                                'message': message,
                                'attachment': f'photo{person_id(offset)}_{get_photo_1(person_id(offset))}',
                                'random_id': 0})


def send_photo_2(user_id, message, offset):
    vk.method('messages.send', {'user_id': user_id,
                                'access_token': user_token,
                                'message': message,
                                'attachment': f'photo{person_id(offset)}_{get_photo_2(person_id(offset))}',
                                'random_id': 0})


def send_photo_3(user_id, message, offset):
    vk.method('messages.send', {'user_id': user_id,
                                'access_token': user_token,
                                'message': message,
                                'attachment': f'photo{person_id(offset)}_{get_photo_3(person_id(offset))}',
                                'random_id': 0})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        request = event.text.lower()
        user_id = str(event.user_id)
        if msg == 'hi':
            send_some_msg(user_id, f'Hi, {get_name(user_id)}, if you want to pick up a pair - type  "start search"')
        elif request == 'привет':
            send_some_msg(user_id, f'Привет, {get_name(user_id)}! Если хочешь подобрать пару - набери "начать поиск"')
        elif request == 'start search':
            send_some_msg(user_id, f'Start searching')
        elif request == 'начать поиск':
            creating_database()
            send_some_msg(user_id, f'{get_name(user_id)}, начинаю поиск')
            get_user(user_id)
            send_some_msg(user_id, f'{get_name(user_id)}, нашел для тебя пару, набери "покажи"')
            find_persons(user_id, offset)
        elif msg == 'покажи':
            for i in line:
                offset += 1
                find_persons(user_id, 0)
                break
        else:
            send_some_msg(user_id, f'{get_name(user_id)}, твое сообщение не понятно')
