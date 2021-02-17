import json
import requests
import bs4
import pathlib
import re

galar_dex_url = "https://serebii.net/swordshield/galarpokedex.shtml"
type_url = "https://pokemondb.net/type/{}"
all_types = [
    "fairy", "steel", "dark",
    "dragon", "ghost", "rock",
    "bug", "psychic", "flying",
    "ground", "poison", "fighting",
    "ice", "grass", "electric",
    "water", "fire", "normal"
]
"""ATTACK_SE = True
ATTACK_LE = True
ATTACK_NE = True
DEFENSE_SE = True
DEFENSE_LE = True
DEFENSE_NE = True"""


def categories(type_data):
    global ATTACK_SE
    global ATTACK_LE
    global ATTACK_NE
    global DEFENSE_SE
    global DEFENSE_LE
    global DEFENSE_NE

    ATTACK_SE = True
    ATTACK_LE = True
    ATTACK_NE = True
    DEFENSE_SE = True
    DEFENSE_LE = True
    DEFENSE_NE = True

    #print(ATTACK_SE, ATTACK_LE, ATTACK_NE, DEFENSE_SE, DEFENSE_LE, DEFENSE_NE)

    if "moves are super-effective" not in str(type_data):
        ATTACK_SE = False
    if "moves are not very" not in str(type_data):
        ATTACK_LE = False
    if "moves have no effect on" not in str(type_data):
        ATTACK_NE = False
    if "types are super-effective" not in str(type_data):
        DEFENSE_SE = False
    if "types are not very" not in str(type_data):
        DEFENSE_LE = False
    if "types have no effect" not in str(type_data):
        DEFENSE_NE = False

    #print(ATTACK_SE, ATTACK_LE, ATTACK_NE, DEFENSE_SE, DEFENSE_LE, DEFENSE_NE)


def typeScraper(url):
    type_dex = {'types': []}
    for poketype in all_types:
        temp_url = url.format(poketype)
        # print("Retrieving data for ", poketype, " types from url: ", temp_url, "\n")
        # temp_url = url.format("fairy")
        data = requests.get(temp_url)
        soup = bs4.BeautifulSoup(data.text, 'html.parser')
        typeSoup = soup.find_all('p', class_='type-fx-list')

        typeSoupCategories = soup.find_all('span', class_='icon-string')
        categories(typeSoupCategories)

        type_dex['types'].append(typeParse(typeSoup, poketype))
        # print(poketype, len(typeSoup[0].contents))

    return type_dex

    # print(typeSoup[2].contents[1].get('href').split('/')[-1])

    # 0-1,3,5 & 1-1,3,5


def typeParse(type_data, poketype):
    typeparser = {}
    attack_se = []

    # typeSoup[0].contents[1].get('href').split('/')[-1]

    typeparser['type'] = poketype
    print(ATTACK_SE, ATTACK_LE, ATTACK_NE, DEFENSE_SE, DEFENSE_LE, DEFENSE_NE)
    for i in range(1, len(type_data[0].contents) - 1, 2):
        # print(poketype, type_data[0].contents[i].get('href').split('/')[-1])
        attack_se.append(type_data[0].contents[i].get('href').split('/')[-1])
    if ATTACK_SE:
        typeparser["attack_se"] = attack_se
    else:
        typeparser["attack_se"] = []
    # print(typeparser)
    return typeparser


def pokemonScraper(url):
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    pokeSoup = soup.find_all('td', class_='fooinfo')
    galar_dex = {'pokemon': []}

    for i in range(0, 4400):
        if (i % 11) == 0:
            galar_dex['pokemon'].append(pokeParse(pokeSoup[i:i + 11]))
        else:
            continue
    return galar_dex


def pokeParse(pokemon_data):
    pokeparser = {}

    pokeparser['galar_no'] = pokemon_data[0].contents[0].strip()[1:]
    pokeparser['name'] = pokemon_data[2].contents[1].contents[0].strip()
    pokeparser['type'] = getTypes(pokemon_data)
    return pokeparser


def getTypes(pokemon_data):
    types = []
    column = pokemon_data[4].find_all('a')
    for index, type in enumerate(column):
        types.append(re.search("type\/(.*?)\.gif", str(column[index].contents[0])).group(1))
    return types


def saveToFile(galar_dex: dict):
    pathlib.Path("./pokemon_db").mkdir(exist_ok=True)

    with open('./pokemon_db/galar_dex.json', 'w') as pokemon_json:
        json.dump(galar_dex, pokemon_json, indent=4, sort_keys=True)


def saveToFileTypes(type_dex: dict):
    pathlib.Path("./pokemon_db").mkdir(exist_ok=True)

    with open('./pokemon_db/type_dex.json', 'w') as type_json:
        json.dump(type_dex, type_json, indent=4, sort_keys=False)


# print(pokemonScraper(galar_dex_url))
# saveToFile(pokemonScraper(galar_dex_url))
saveToFileTypes(typeScraper(type_url))
#print(typeScraper(type_url))
