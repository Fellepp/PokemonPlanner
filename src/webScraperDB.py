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


def matrixScraper(url):
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    typeSoup = soup.find_all('td')

    typeMatrix = [[0 for i in range(len(all_types))] for j in range(len(all_types))]

    rowCount = 0
    for index, pokeType in enumerate(typeSoup):
        if (index % 18) == 0 and index != 0:
            rowCount += 1
        if "normal effectiveness" in str(pokeType):
            typeMatrix[rowCount][(index % 18)] = 1
        elif "not very effective" in str(pokeType):
            typeMatrix[rowCount][(index % 18)] = 0.5
        elif "super-effective" in str(pokeType):
            typeMatrix[rowCount][(index % 18)] = 2
        elif "no effect" in str(pokeType):
            typeMatrix[rowCount][(index % 18)] = 0

    return typeMatrix


def matrixTranslator(typeMatrix):
    typedict = {'types': {}}
    ase = 'attack_super-effective'
    ale = 'attack_not very effective'
    ane = 'attack_not effective'
    dse = 'defend_super-effective'
    dle = 'defend_not very effective'
    dne = 'defend_not effective'

    for pokeType in all_types:
        tmpdictX = {}
        tmpdictX[ase] = []
        tmpdictX[ale] = []
        tmpdictX[ane] = []
        tmpdictX[dse] = []
        tmpdictX[dle] = []
        tmpdictX[dne] = []
        typedict['types'][pokeType] = tmpdictX

    print(typedict)

    for index, row in enumerate(typeMatrix):
        attackingPlace = len(all_types) - 1 - index
        attackingType = all_types[attackingPlace]
        attack_se = []
        attack_le = []
        attack_ne = []

        tmpdict = {}
        tmpdict['type'] = attackingType

        for indexx, poketype in enumerate(row):
            defendingPlace = len(all_types) - 1 - indexx
            defendingType = all_types[defendingPlace]
            print(attackingType, defendingType)

            if poketype == 0.5:
                typedict['types'][attackingType][ale].append(defendingType)
                typedict['types'][defendingType][dle].append(attackingType)
                print(attackingType, "is not very effective against", defendingType)
            elif poketype == 2:
                typedict['types'][defendingType][dse].append(attackingType)
                typedict['types'][attackingType][ase].append(defendingType)
                print(attackingType, "is super-effective against", defendingType)
            if poketype == 0:
                typedict['types'][defendingType][dne].append(attackingType)
                typedict['types'][attackingType][ane].append(defendingType)
                print(attackingType, "is not effective against", defendingType)
    return typedict

    """
    NO LONGER IN USE
    
        def typeScraper(url): 

        type_dex = {'types': []}

        for poketype in all_types:
            temp_url = url.format(poketype)
            # print("Retrieving data for ", poketype, " types from url: ", temp_url, "\n")
            # temp_url = url.format("fairy")
            data = requests.get(temp_url)
            soup = bs4.BeautifulSoup(data.text, 'html.parser')
            typeSoup = soup.find_all('p', class_='type-fx-list')

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
    return typeparser"""


"""def pokemonScraper(url):
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    pokeSoup = soup.find_all('td', class_='fooinfo')
    galar_dex = {'pokemon': {}}

    for i in range(0, 4400):
        if (i % 11) == 0:
            #galar_dex['pokemon'].append(pokeParse(pokeSoup[i:i + 11]))
            galar_dex['pokemon'] = pokeParse(pokeSoup[i:i + 11])
        else:
            continue
    return galar_dex"""


def pokeScraper(url):
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    pokeSoup = soup.find_all('td', class_='fooinfo')
    galar_dex = {'pokemon': {}}

    for i in range(0, 4400):
        if (i % 11) == 0:
            tmpdict = {}
            tmpdict['name'] = pokeSoup[i:i + 11][2].contents[1].contents[0].strip()
            tmpdict['type'] = getTypes(pokeSoup[i:i + 11])

            gal_nr = pokeSoup[i:i + 11][0].contents[0].strip()[1:]
            galar_dex['pokemon'][gal_nr] = tmpdict
        else:
            continue
    return galar_dex


def pokeParse(pokemon_data):
    galar_dex = {'pokemon': {}}

    galar_dex['pokemon']['galar_no'] = pokemon_data[0].contents[0].strip()[1:]

    pokeparser = {}
    thisPokemon = pokemon_data[0].contents[0].strip()[1:]
    pokeparser['galar_no'] = thisPokemon

    pokeparser[thisPokemon]['name'] = pokemon_data[2].contents[1].contents[0].strip()
    pokeparser[thisPokemon]['type'] = getTypes(pokemon_data)
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


def saveTypes(type_dict: dict):
    pathlib.Path("./pokemon_db").mkdir(exist_ok=True)

    with open('./pokemon_db/type_dex.json', 'w') as type_json:
        json.dump(type_dict, type_json, indent=4, sort_keys=False)


"""def saveToFileTypes(type_dex: dict):
    pathlib.Path("./pokemon_db").mkdir(exist_ok=True)

    with open('./pokemon_db/type_dex.json', 'w') as type_json:
        json.dump(type_dex, type_json, indent=4, sort_keys=False)"""

# print(pokemonScraper(galar_dex_url))
# saveToFile(pokemonScraper(galar_dex_url))
# saveToFileTypes(typeScraper(type_url))
# print(typeScraper(type_url))

saveToFile(pokeScraper(galar_dex_url))
# saveTypes(matrixTranslator(matrixScraper(url="https://pokemondb.net/type")))
