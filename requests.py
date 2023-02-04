import requests


def best_superhero():
    base_url = "https://akabab.github.io/superhero-api/api"
    res = requests.get(base_url + "/all.json").json()
    intelligence = 0
    smartest_hero = ""
    for superhero in res:
        if superhero["name"] in ["Hulk", "Captain America", "Thanos"]:
            if superhero["powerstats"]["intelligence"] > intelligence:
                intelligence = superhero["powerstats"]["intelligence"]
                smartest_hero = superhero["name"]
    print(f"{smartest_hero} has intelligence {intelligence}")


class YaUploader:
    YANDEX_HOST = "https://cloud-api.yandex.net:443"

    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str, file_name: str):
        auth_headers = {"Authorization": self.token}
        file_request = self.YANDEX_HOST + f"/v1/disk/resources/upload?path=%2Ftest_folder%2F{file_name}&overwrite=true"
        res = requests.get(file_request, headers=auth_headers).json()
        requests.put(res["href"], data=open(file_path, 'rb'), headers=auth_headers)


if __name__ == '__main__':
    best_superhero()

    path_to_file = "test.txt"
    token = "XXXX"
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file, "hello.txt")
