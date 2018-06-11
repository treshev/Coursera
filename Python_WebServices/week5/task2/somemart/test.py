import requests


def test_post_item_auth(user_name, password):
    """/api/v1/goods/ (POST) сохраняет товар в базе."""
    url = 'http://127.0.0.1:8000/api/v1/goods/'
    data = {
        'title': 'Сыр "Российский5"',
        'description': 'Очень вкусный сыр, да еще и российский5.',
        'price': 999
    }
    response = requests.post(url, data=data, auth=(user_name, password))

    # Объект был сохранен в базу
    print(response.status_code, response.content)

def test_post_item():
    """/api/v1/goods/ (POST) сохраняет товар в базе."""
    url = 'http://127.0.0.1:8000/api/v1/goods/'
    data = {
        'title': 'Сыр "Российский2"',
        'description': 'Очень вкусный сыр, да еще и российский2.',
        'price': 100000
    }
    response = requests.post(url, data=data)

    # Объект был сохранен в базу
    print(response.content)


def test_post_rewiew(item_id, iter, grade):
    """/api/v1/goods/ (POST) сохраняет товар в базе."""
    url = 'http://127.0.0.1:8000/api/v1/goods/{}/reviews/'.format(item_id)
    data = {
        'text': 'Новый отзыв ' + str(iter),
        'grade': grade
    }
    response = requests.post(url, data=data)
    print(response.content)


def test_get_rewiew(id):
    """/api/v1/goods/ (POST) сохраняет товар в базе."""
    url = 'http://127.0.0.1:8000/api/v1/goods/{}/'.format(id)
    response = requests.get(url)
    print(response.json())


if __name__ == '__main__':
    test_post_item_auth("user1", 'world')
    test_post_item_auth("hello", 'world')
    test_post_item_auth("hello2", 'world')
    # test_post_rewiew(88, 88,5)
    # test_post_rewiew(6,6)
    # test_post_rewiew(7,7)
    # test_post_rewiew(8,8)
    # test_get_rewiew(3)
