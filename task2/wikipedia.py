from typing import Dict, Set
import requests
from time import sleep


RUSSIAN_LETTERS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def get_all_animals():
    """API reference https://www.mediawiki.org/wiki/API:Categorymembers
    """

    URL = "https://ru.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "cmtitle": "Категория:Животные_по_алфавиту",
        "cmlimit": "500",
        "list": "categorymembers",
        "format": "json",
        "cmtype": "page",
    }

    animals = set()

    while True:
        response = requests.get(URL, params=PARAMS)
        data = dict(response.json())
        for page in data["query"]["categorymembers"]:
            animals.add(page["title"])

        if data.get("continue", False):
            PARAMS["cmcontinue"] = data["continue"].get("cmcontinue")
            sleep(1)  # чтобы не забанили
        else:
            break

    return animals


def parse_animals(animals: Set) -> Dict[str, int]:
    # Условимся, что нужно отобрать только названия на кириллице.
    counter = {k: 0 for k in RUSSIAN_LETTERS}
    for animal in animals:
        if animal[0] in RUSSIAN_LETTERS:
            counter[animal[0]] += 1

    return counter


def main():
    animals = get_all_animals()

    for k, v in parse_animals(animals).items():
        print(f"{k}: {v}\n")


if __name__ == "__main__":
    main()
