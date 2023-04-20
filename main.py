import vk_api
from database import orm
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk.vk_search import Search
from config import VK_TOKEN_GROUP, VK_GROUP_ID
from random import randrange

API_VERSION = "5.131"
SEARCH_BUTTON = "Найти"
SHOW_BUTTON = "Показать ещё"
START_REQUEST = "Привет"
SEARCH_COUNT = 5


def create_keyboard():
    keybord = VkKeyboard(one_time=False, inline=False)
    keybord.add_button(SEARCH_BUTTON, VkKeyboardColor.PRIMARY)
    keybord.add_button(SHOW_BUTTON, VkKeyboardColor.PRIMARY)
    return keybord


def write_msg(vk_session, user_id, message, keyboard=None, attachments=[]):
    values = {"user_id": user_id, "message": message,
              "random_id": randrange(10 ** 7), }
    if keyboard:
        values["keyboard"] = keyboard.get_keyboard()
    if attachments:
        values["attachment"] = ",".join(filter(None, attachments))
    vk_session.method("messages.send", values)


def main():
    keyboard = create_keyboard()
    vk_session = vk_api.VkApi(token=VK_TOKEN_GROUP, api_version=API_VERSION)
    longpoll = VkLongPoll(vk_session, group_id=VK_GROUP_ID)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text.lower().strip()
            search = Search()

            if request == START_REQUEST.lower():
                user = search.get_user(event.user_id)
                city = None
                if user.get("city"):
                    city = user.get("city").get("title")
                orm.add_user(id_vk=event.user_id, bdate=user["bdate"],
                             sex=user["sex"], city=city)
                write_msg(vk_session, event.user_id,
                          f"Новый поиск: {SEARCH_BUTTON}",
                          keyboard)
            elif request == SEARCH_BUTTON.lower():
                write_msg(vk_session, event.user_id, "Поиск...", keyboard)
                cnt = orm.get_match_count(event.user_id)
                users = search.search_users(
                    event.user_id, count=SEARCH_COUNT, offset=cnt)
                for user in users:
                    photos = search.get_user_photos(user)
                    orm.add_match(id_vk=event.user_id,
                                  id_vk_match=user, photos=photos)
                write_msg(vk_session, event.user_id,
                          f"Добавлено: {len(users)}", keyboard)
            elif request == SHOW_BUTTON.lower():
                match = orm.show_next_match(id_vk=event.user_id)
                if match:
                    write_msg(vk_session, event.user_id,
                              f"https://vk.com/id{match.id_vk_match}",
                              keyboard,
                              [match.photo1, match.photo2, match.photo3])
                    orm.set_match_showed(match.id_match)
                else:
                    write_msg(vk_session, event.user_id,
                              f"Нет записей. Новый поиск: {SEARCH_BUTTON}",
                              keyboard)
            else:
                write_msg(vk_session, event.user_id,
                          "Неизвестный запрос", keyboard)


if __name__ == "__main__":
    main()
