import json
from time import sleep
import random
import requests
from Wykop import Wykop
from datetime import datetime


def get_random_object():
    with open('jsons/objects.json', 'r') as f:
        list_of_men = json.load(f)

    random_man = random.choice(list_of_men)
    return random_man


def add_user_to_list_and_file(list_of_users, login):
    list_of_users.append(login)
    with open('jsons/users.json', 'w') as file:
        json.dump(list_of_users, file)


def remove_object_from_file(man):
    with open('jsons/objects.json', 'r') as f:
        list_of_objects = json.load(f)

    list_of_objects.remove(man)

    with open('jsons/objects.json', 'w') as f:
        json.dump(list_of_objects, f)


def get_current_date():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
    return date


def get_sex(author):
    try:
        return author['sex']
    except KeyError:
        return 'male'


def start():
    with open('jsons/users.json', 'r') as file:
        list_of_users = json.load(file)

    wykop = Wykop()
    entry_id = ''
    while True:
        try:
            print(get_current_date() + ' - Trying get up voters')
            up_voters = wykop.get_up_voters(entry_id)['data']
            print(get_current_date() + ' - Up voters were get')

            females = [upvoter for upvoter in up_voters if
                            'sex' in upvoter['author'].keys() and upvoter['author']['sex'] == 'female']

            for x in females:
                login = x['author']['login']

                if login not in list_of_users:
                    try:
                        man = get_random_object()

                    except IndexError:
                        print('The list of objects is empty')
                        break
                        exit()

                    object_name = man['name']
                    object_img_url = man['img_url']

                    msg = f'@{login} here is message for user - {object_name}'

                    request = wykop.add_comment(entry_id, msg, object_img_url)
                    request_data = request['data']

                    if request_data is not None:
                        current_date = get_current_date()

                        print(current_date + ' - Comment added!')
                        print(request)

                        add_user_to_list_and_file(list_of_users, login)
                        remove_object_from_file(man)
                        sleep(2)

                    else:
                        date_now = get_current_date()
                        print(date_now + ' - ' + request['error']['message_pl'])
                        sleep(40)

            sleep(10)
        except requests.exceptions.ReadTimeout as e:
            print(get_current_date() + ' - BummConnectionTimeout - ' + str(e))
        except requests.exceptions.ConnectionError as e:
            print(get_current_date() + ' - ' + str(e))


start()
