import json
import requests
import bs4
import lxml
import pathlib

galar_dex_url = "https://serebii.net/swordshield/galarpokedex.shtml"


def pokeParse(pokemon_data):
    pokeparser = {}

    pokeparser['galar_no'] = pokemon_data[0].contents[0].strip()[1:]
    pokeparser['name'] = pokemon_data[2].contents[1].contents[0].strip()
    return pokeparser


def pokemonScrapper(url):
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')  # 'lxml'
    pokeSoup = soup.find_all('td', class_='fooinfo')
    galar_dex = {'pokemon': []}

    for i in range(0, 4400):
        if (i % 11) == 0:
            galar_dex['pokemon'].append(pokeParse(pokeSoup[i:i + 11]))
        else:
            continue
    return galar_dex


def saveToFile(galar_dex: dict):
    pathlib.Path("./pokemon_db").mkdir(exist_ok=True)

    with open('./pokemon_db/galar_dex.json', 'w') as pokemon_json:
        json.dump(galar_dex, pokemon_json, indent=4, sort_keys=True)


saveToFile(pokemonScrapper(galar_dex_url))
