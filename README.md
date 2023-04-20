# VKinder
Чат-бот для поиска людей подходящих под условия, на основании информации о пользователе ВКонтакте.

## Установка

1. Установить пакеты `pip install -r requirements.txt`
2. Создать файл `.env` из примера `.env.example`
3. Установить PostgreSQL. Указать строку соединения в параметре `DB_URI`
4. Создать группу ВКонтакте и получить токен, [пример](https://github.com/netology-code/py-advanced-diplom/blob/new_diplom/group_settings.md). Токен группы указать в параметре `VK_TOKEN_GROUP`, id группы указать в параметре `VK_GROUP_ID`
5. Получить access_token ВКонтакте и указать в параметре `VK_TOKEN_CLIENT`, [пример](https://oauth.vk.com/authorize?client_id=123456789&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,notify,photos,wall,email,mail,groups,stats&response_type=token&v=5.131&state=123456).
6. Запусить `python main.py`
7. Написать в группе сообщение для регистрации пользователя: "Привет"