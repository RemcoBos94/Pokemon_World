import Pokedex
import Pokemon
import Attack
import Inventory




def makePokedex():
    
    pokedex = Pokedex.Pokedex("pokemonDB")
    

    pokeDB = "Data/pokedex.csv"
    fid = open(pokeDB, "r")
    pokeLijnen = fid.readlines()
    fid.close()

    for i in range(1, len(pokeLijnen)):
        pokemonLijn = pokeLijnen[i].strip().split(',')
        pokemon = Pokemon.Pokemon(pokemonLijn[1], pokemonLijn[2], pokemonLijn[3], pokemonLijn[4], pokemonLijn[5], pokemonLijn[6], pokemonLijn[7])
        
        aanvallenDB = "Data/aanvallen.csv"
        fid = open(aanvallenDB, "r")
        aanvalLijnen = fid.readlines()
        fid.close()
        for j in range(1, len(aanvalLijnen) - 1):
            aanvalLijn = aanvalLijnen[j].strip().split(',')
            aanval = Attack.Attack(aanvalLijn[0], aanvalLijn[1], aanvalLijn[2], aanvalLijn[3])
            if (pokemon.getPrimaryType() == aanval.getType()):
                pokemon.voegAanvalToe(aanval)
            if (aanval.getType() == "NORMAL"):
                pokemon.voegAanvalToe(aanval)
        pokedex.addPokemon(pokemon)
        print("pokecheck")
        
    return pokedex

    #aanval_per_type_db = dict()
    # Bestanden uitlezen kunnen we doen met behulp van de open/close functies.
    

def createInventoryMainPlayer():
    """
    Initialiseerd de inventory
    Returns
    -------
    dict:
        inventory in dictionary met als keys pokeball, masterball, health potions en raspberries
    """
    inventory = Inventory.Inventory(5,5,5,5,0)
    return inventory

    