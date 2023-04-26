import logging
import vk_api
from datetime import datetime
from dateutil import relativedelta
from config import VK_TOKEN_CLIENT


class Search:

    def __init__(self):
        self.data_dict = []
        self.vk_session = vk_api.VkApi(token=VK_TOKEN_CLIENT)
        self.vk = self.vk_session.get_api()

    def search(self, age, sex, city, count=10, offset=0):
        ids = []
        try:
            matches = self.vk.users.search(
                age_from=age-5,
                age_to=age+5,
                sex=sex,
                hometown=city,
                status=1,
                count=count,
                offset=offset,
                is_closed=False,
                has_photo=1)
        except vk_api.ApiError as e:
            logging.error(f"API Error: {e}")
            return ids
        for r in matches.get("items"):
            ids.append(r.get("id"))
        return ids

    def get_user_photos(self, vk_id, count=3):
        link_list = []
        user = self.get_user(vk_id)
        if user.get("can_access_closed"):
            try:
                photos = self.vk.photos.getAll(
                    owner_id=vk_id, photo_sizes=1, extended=1)
            except vk_api.ApiError as e:
                logging.error(f"API Error: {e}")
                return link_list
            photos_sorted = sorted(photos["items"], key=lambda d: d["likes"]
                                   ["count"]+d["reposts"]["count"],
                                   reverse=True)[:count]
            for link in photos_sorted:
                media_id = link["id"]
                link_list.append(f"photo{vk_id}_{media_id}")
        return link_list

    def get_user(self, vk_id):
        try:
            user = self.vk.users.get(user_ids=vk_id, fields=(
                "bdate", "first_name", "last_name", "bdate", "sex", "city"))
        except vk_api.ApiError as e:
            logging.error(f"API Error: {e}")
            return None
        return user[0]

    def search_users(self, vk_id, count=10, offset=0):
        ids = []
        vk_user = self.get_user(vk_id)
        if vk_user:
            age = relativedelta.relativedelta(
                datetime.now(),
                datetime.strptime(vk_user["bdate"], "%d.%m.%Y")).years
            if vk_user["sex"] == 1:
                sex = 2
            elif vk_user["sex"] == 2:
                sex = 1
            else:
                sex = 0
            city = ""
            if vk_user.get("city"):
                city = vk_user.get("city").get("title")
            ids = self.search(age, sex, city, count=count, offset=offset)
        return ids
