import random

class Pokedex:
    """
    Class that creates a pokedex with all pokemon
    A pokedex has a name and a list of all pokemon
    """
    def __init__(self, naam):
        self._naam = naam
        self._pokemon = []

    def addPokemon(self, pokemon):
        self._pokemon.append(pokemon)

    def getPokemon(self, name):
        
        for i in range(len(self._pokemon)):
            if(self._pokemon[i].getName() == name):
                return self._pokemon[i]

    def chooseRandomPokemon(self):
        randomPokemon = random.choice(self._pokemon)
        randomPokemon.incrementID()
        return randomPokemon
    

