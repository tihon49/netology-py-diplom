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
        self.id = id


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
 
        return common_friends


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
                  'count': 1000,
                  'v': VERSION
                  }

        data = self.get_response(url, params)
        groups = data['response']['items']
        return [group['name'] for group in groups]


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


    # получаем список друзей онлайн. type => dict
    def get_friends_online(self):
        url = 'https://api.vk.com/method/friends.getOnline?v=5.52&access_token='
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



def main():
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



if __name__ == '__main__':
    # main()
    Evgeniy = User(171691064)

    Evgeniy.get_most_of_common_friends()