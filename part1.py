import requests

if __name__ == '__main__':
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
