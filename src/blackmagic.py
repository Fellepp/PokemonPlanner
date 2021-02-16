class Pokemon:

    def __init__(self, name: str, types: list):
        self.name = name
        self.types = types


class PokeType:

    def __init__(self, name: str, strengths: list, weaknesses: list, immunity: list):
        self.name = name
        self.strengths = strengths
        self.weaknesses = weaknesses
        self.immunity = immunity


# init all types
t_fairy = PokeType("Fairy", [], [], [])
t_steel = PokeType("Steel", [], [], [])
t_dark = PokeType("Dark", [], [], [])
t_dragon = PokeType("Dragon", [], [], [])
t_ghost = PokeType("Ghost", [], [], [])
t_rock = PokeType("Rock", [], [], [])
t_bug = PokeType("Bug", [], [], [])
t_psychic = PokeType("Psychic", [], [], [])
t_flying = PokeType("Flying", [], [], [])
t_ground = PokeType("Ground", [], [], [])
t_poison = PokeType("Poison", [], [], [])
t_fight = PokeType("Fight", [], [], [])
t_ice = PokeType("Ice", [], [], [])
t_grass = PokeType("Grass", [], [], [])
t_electric = PokeType("Electric", [], [], [])
t_water = PokeType("Water", [], [], [])
t_fire = PokeType("Fire", [], [], [])
t_normal = PokeType("Normal", [], [], [])

# Fairy
t_fairy.strengths.append(t_fight)
t_fairy.strengths.append(t_dragon)
t_fairy.strengths.append(t_fairy)

t_fairy.weaknesses.append(t_poison)
t_fairy.weaknesses.append(t_steel)

# Steel
t_steel.strengths.append(t_ice)
t_steel.strengths.append(t_rock)
t_steel.strengths.append(t_fairy)

t_steel.weaknesses.append(t_fire)
t_steel.weaknesses.append(t_fight)
t_steel.weaknesses.append(t_ground)

# Dark
t_dark.strengths.append(t_psychic)
t_dark.strengths.append(t_ghost)

t_dark.weaknesses.append(t_fight)
t_dark.weaknesses.append(t_bug)
t_dark.weaknesses.append(t_fairy)

# Dragon
t_dragon.strengths.append(t_dragon)

t_dragon.weaknesses.append(t_ice)
t_dragon.weaknesses.append(t_dragon)
t_dragon.weaknesses.append(t_fairy)

# Ghost
t_ghost.strengths.append(t_psychic)
t_ghost.strengths.append(t_ghost)

t_ghost.weaknesses.append(t_ghost)
t_ghost.weaknesses.append(t_dark)

# Rock
t_rock.strengths.append(t_fire)
t_rock.strengths.append(t_ice)
t_rock.strengths.append(t_flying)
t_rock.strengths.append(t_bug)

t_rock.weaknesses.append(t_fire)


# Bug
# Psychic
# Flying
# Ground
# Poison
# Fight
# Ice
# Gass
# Electric
# Water
# Fire
# Normal

t_normal.weaknesses.append(t_fight)
t_fight.strengths.append(t_normal)
t_water.strengths.append(t_fire)
t_fire.weaknesses.append(t_water)

typeList = [t_normal, t_fight, t_water, t_fire]

pokeDex = []
pokeDex.append(Pokemon("Spearow", [t_normal]))
pokeDex.append(Pokemon("Mudkip", [t_water]))
pokeDex.append(Pokemon("Machop", [t_fight]))
pokeDex.append(Pokemon("Charmander", [t_fire]))
pokeDex.append(Pokemon("Meloetta", [t_normal, t_fight, t_water]))

availablePokemon = pokeDex


def addBestPokemon(availablePokemon, pokeTeam):
    coveredTypes = []
    for pokemon in pokeTeam:
        for t_type in pokemon.types:
            for strength in t_type.strengths:
                coveredTypes.append(strength)

    bestPokemon = (None, -100)
    for pokemon in availablePokemon:
        score = 0
        for t_type in pokemon.types:
            for strength in t_type.strengths:
                if strength not in coveredTypes:
                    score += 1
        if score > bestPokemon[1]:
            bestPokemon = (pokemon, score)
    return bestPokemon[0]


def findBestTeam(availablePokemon, teamSize):
    pokeTeam = []
    while len(pokeTeam) != teamSize and len(availablePokemon) > 0:
        bestPokemon = addBestPokemon(availablePokemon, pokeTeam)
        availablePokemon.remove(bestPokemon)
        pokeTeam.append(bestPokemon)
    return pokeTeam


pokeTeam = findBestTeam(availablePokemon, 2)
for pokemon in pokeTeam:
    print(pokemon.name)
