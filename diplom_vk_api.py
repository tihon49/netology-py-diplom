from config import *
import requests
from pprint import pprint
import time
import json



access_token = APP_TOKEN    # токен приложения
app_id       = APP_ID       # id приложения
VERSION      = 5.103


############################# ОПИСАНИЕ КЛАССА ###############################
# Задача №1
class User:
    def __init__(self, u_id):
        # если указан не id, а строковой аналог, приводим его к числовому id
        try:
            self.id = u_id
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
        try:
            user_1_friends = self.get_friends()
            user_2_friends = user2.get_friends()
            common_friends = []

            for friend in user_1_friends:
                if friend in user_2_friends:
                    common_friends.append(User(friend))
            
            if common_friends:
                return common_friends
            else:
                return 'у данных пользователей нет общих друзей'
        except:
            pass


    # отправка request'a / получение response'а
    def get_response(self, url, params):
        response = requests.get(url, params=params)
        data = response.json()
        return data


    # получаем количество друзей из группы. type => int
    def get_group_contacts_count(self, g_id):
        url = 'https://api.vk.com/method/groups.getMembers'
        params = {'access_token': access_token,
                  'group_id': g_id,
                  'filter': 'friends',
                  'v': VERSION
                  }

        data = self.get_response(url, params=params)
        return data['response']['count']

    # получаем список групп в ктороых состоит только данный пользователь. typy => dict
    def get_uniq_groups(self):
        groups_list = self.get_groups_names()
        uniq_groups = []
        print(f'всего групп найдено: {len(groups_list)}')

        try:
            for group in groups_list:
                print('.', end='')
                time.sleep(1)
                count_of_friends = self.get_group_contacts_count(group['id'])

                if count_of_friends == 0:
                    g_data = {'name': group['name'],
                              'gid' : group['id'],
                              'members_count': group['members_count']
                              }
                    uniq_groups.append(g_data)
        except: 
            pass

        if len(uniq_groups) == 0:
            print('Done')
            print('данный пользователь не состоит ни в одной "уникальной" группе')
        else:
            with open('groups.json', 'w', encoding='utf8') as f:
                json.dump(uniq_groups, f, ensure_ascii=False)

            print('Done')
            print(f'всего "уникальных" групп найдено: {len(uniq_groups)}')
            print('В папке со скриптом появился файл "groups.json"\nв котором записаны уникальные группы пользователя.')


    # получаем список групп пользователя. type => list
    def get_groups_names(self):
        try:
            url = f'https://api.vk.com/method/groups.get' #'users.getSubscriptions'
            params = {'access_token': access_token,
                      'user_id': self.id,
                      'extended': 1,
                      'fields': 'members_count,counters,contacts,city,country',
                      'count': 1000,
                      'v': VERSION
                      }

            data = self.get_response(url, params)
            try:
                groups = data['response']['items']
            except:
                pass
            return groups
        except:
            print('не удалось найти пользователя с указанным id')


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
        url = 'https://api.vk.com/method/friends.getOnline'
        params = {
                 'access_token': access_token,
                 'v': VERSION,
                 'user_id': self.id
                 }

        data = self.get_response(url, params=params)
        return data['response']


    # найти друга с которым больше всего общих друзей
    def get_most_of_common_friends(self):
        print('просьба набраться терпения, это может занять несколько минут.')
        max_count_of_friends = 0
        max_friends_id = 0

        friends_list = self.get_friends()

        for friend in friends_list:
            time.sleep(1)
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
################################### КОНЕЦ ОПИСАНИЯ КЛАССА ################################################


# функция к домашнему заданию
def homeWork():
    try:
        user_input = input('введите два id номера через пробел для поиска общих друзей: ').split()
        if len(user_input) > 2:
            print('введено больше двух id номеров')
        else:
            user1 = User(user_input[0])
            user2 = User(user_input[1])

            # вывод общих друзей в виде экземпляров класса с помощью метода  __and__(self, other)
            pprint(user1 & user2)

    except:
        print('введены не верные данные')



# функция получения экземпляра класса с указанным id
def get_profile():
    user_input = input('введите id полтзователя: ')
    return User(user_input)



def main(u_input, info):
    try:
        if u_input not in range(10):
            print('введена не верная команда')
        elif u_input == 0:
            print(info)
        elif u_input == 1:
            homeWork()
        elif u_input == 2:
            print(get_profile())
        elif u_input == 3:
            pprint([group['name'] for group in get_profile().get_groups_names()])
        elif u_input == 4:
            pprint(get_profile().get_friends())
        elif u_input == 5:
            pprint(get_profile().get_friends_online())
        elif u_input == 6:
            get_profile().get_uniq_groups()
        elif u_input == 7:
            get_profile().get_most_of_common_friends()

    except ValueError:
        print('просьба вводить только цифры')



if __name__ == '__main__':
    info = '''
вызвать данное меню еще раз ............................. : 0
получить список общих друзей у двух пользователей (ДЗ)... : 1
получить ссылку на профиль в вк ..................(ДЗ)... : 2
получить список названий всех групп пользователя ........ : 3
получить список id всех друзей .......................... : 4
получить список id друзей онлайн ........................ : 5
получить список уникальных групп пользователя (ДИПЛОМ) .. : 6
получить id пользователя с кем больше всего общих друзей  : 7
#############################################################
      [!]    ДЛЯ ВЫХОДА ИЗ ПРОГРАММЫ НАЖМИТЕ: q    [!]
'''
    print(info)

    while True:
        try:
            user_input = input('\nваш выбор: ')
            if user_input.lower() == 'q':
                break
            else:
                try:
                    main(int(user_input), info)
                except ValueError:
                    print('просьба вводить только цифры')
        except:
            pass