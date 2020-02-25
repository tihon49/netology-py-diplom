from config import *
import requests
from pprint import pprint
import threading



access_token = APP_TOKEN        # токен приложения
app_id       = APP_ID           # id приложения
VERSION      = 5.103



# Отдельный поток - обёртка для последующих функций
def thread(my_func):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread (target=my_func, args=args, kwargs=kwargs)
        my_thread.start()

    return wrapper


# Задача №1
class User:
    def __init__(self, id):
        # если указан не id, а строковой аналог, приводим его к числовому id
        try:
            self.id = id
            if str(self.id).isdigit():
                pass
            else:
                url = 'https://api.vk.com/method/users.get'
                params = {'access_token': access_token,
                          'user_ids': self.id,
                          'v': VERSION
                         }

                data = self.get_response(url, params)
                self.id = data['response'][0]['id']
        except:
            print('Not valid data')


    # Задача №3
    # при вызове функции print(user) вывод ссылки на его профиль в VK
    def __str__(self):
        return f'https://vk.com/id{self.id}'


    # Задача №2
    # битовое И (x & y)
    def __and__(self, user2):
        user_1_friends = self.get_friends()
        user_2_friends = user2.get_friends()
        common_friends = []

        for friend in user_1_friends:
            if friend in user_2_friends:
                common_friends.append(User(friend))
        
        if common_friends:
            return common_friends
        else:
            return 'у данных пользователей нет общих групп'


    # отправка request'a / получение response'а
    def get_response(self, url, params):
        response = requests.get(url, params=params)
        data = response.json()
        return data


    # получаем список групп пользователя. type => list
    def get_groups_names(self):
        url = f'https://api.vk.com/method/groups.get' #'users.getSubscriptions'
        params = {'access_token': access_token,
                  'user_id': self.id,
                  'extended': 1,
                  'fields': 'members_count,counters,contacts,city,country',
                  'count': 1000,
                  'v': VERSION
                  }

        data = self.get_response(url, params)
        groups = data['response']['items']
        return groups # [group['name'] for group in groups]


    # получаем список с друзьями. type => list
    def get_friends(self): 
        url = f'https://api.vk.com/method/friends.get'
        params = {'access_token': access_token,
                  'v': VERSION,
                  'user_id': self.id,
                  'order': 'hints',
                  'fields': 'nickname,domain,city,photo_200_orig,online',
                  'name_case': 'nom'
                  }

        data = self.get_response(url, params)
        friends_id = [friend['id'] for friend in data['response']['items']]
        return friends_id


    # получаем список групп в ктороых состоит только данный пользователь
    def get_uniq_grous(self):
        self.groups = self.get_groups_names()
        counter = len(self.get_friends())

        for friend in self.get_friends():
            print(f'осталось обработать {counter} друзей')
            counter -= 1
            friend = User(friend)
            
            for group in self.groups:
                try:
                    if group in friend.get_groups_names():
                        try:
                            self.groups.remove(group)
                        except:
                            pass
                except:
                    pass

        return self.groups


    # получаем список друзей онлайн. type => dict
    def get_friends_online(self):
        url = 'https://api.vk.com/method/friends.getOnline'
        params = {
                 'access_token': access_token,
                 'v': VERSION,
                 'user_id': self.id
                 }

        data = self.get_response(url, params=params)
        return data['response']


    # найти друга с которым больше всего общих друзей
    @thread
    def get_most_of_common_friends(self):
        max_count_of_friends = 0
        max_friends_id = 0

        friends_list = self.get_friends()

        for friend in friends_list:
            try:
                common_f_count = len(User(self.id) & User(friend))
                friend_id = User(friend).id

                if common_f_count > max_count_of_friends:
                    max_count_of_friends = common_f_count
                    max_friends_id = friend_id
            except:
                pass
            else:
                print('.', end='')

        print(f'\nбольше всего общих друзей с пользователем: id{max_friends_id} - {max_count_of_friends}')


# функция к домашнему заданию
def homeWork():
    try:
        user_input = input('введите два id номера через пробел для поиска общих друзей: ').split()
        user1 = User(int(user_input[0]))
        user2 = User(int(user_input[1]))

        # вывод общих друзей в виде экземпляров класса с помощью метода  __and__(self, other)
        pprint(user1 & user2)

        # выводим ссылку на профиль пользователя с помощью метода  __str__(self)
        print(f'\nссылка на пользователя №1: {user1}')
        print(f'ссылка на пользователя №2: {user2}')

    except Exception as e:
        print(f'error: {e}')


def main():
    Evgeniy = User('eshmargunov')
    Evgeniy_uniq_groups = Evgeniy.get_uniq_grous()
    list_to_return = []

    for group in Evgeniy_uniq_groups:
        data = {'name': group['name'],
                'gid' : group['id'],
                'members_count': group['members_count']}
        list_to_return.append(data)

    with open('out.json', 'w') as f:
        f.write(str(list_to_return))

    print('Done')



    

if __name__ == '__main__':
    main()