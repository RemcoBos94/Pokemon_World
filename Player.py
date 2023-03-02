class Player:
    """
    Class that represents a player of the game
    """
    def __init__(self, naam, bot):
        """
        Creates a new player with its according name.
        
        """

        self._naam = naam
        self._bot = bot
        self._pokemon = []
        self._activePokemon = None
        self._inventory = ""

    def getName(self):
       
        return self._naam

    def getActivePokemon(self):
        return self._activePokemon

    def getPokemon(self):
        return self._pokemon

    def getInventory(self):
        return self._inventory

    def setActivePokemon(self, pokemon):
        self._activePokemon = pokemon

    def addActivePokemon(self, pokemon):
        self._activePokemon = pokemon
        self._pokemon.append(pokemon)

    def addPokemon(self, pokemon):
        self._pokemon.append(pokemon)

    def addInventory(self, inventory):
        self._inventory = inventory

    def deletePokemon(self, pokemon):  
        self._activePokemon = ""
        self._pokemon.remove(pokemon)
        if(len(self._pokemon) != 0):
            self._activePokemon = self._pokemon[0]
             
        

       

