class Player:
    """
    Klasse die de spelers van het spel voorstelt
    """
    def __init__(self, naam, bot):
        """
        Maakt een nieuwe speler aan met gegeven naam en toont of de speler het hoofdpersonage of een bot is.
        
        Parameters
        -----
        naam : str
        """
        self._naam = naam
        self._bot = bot
        self._pokemon = []
        self._activePokemon = None
        self._inventory = ""

    def getName(self):
        """
        Geeft de naam terug.
        Returns
        -----
        str
        """
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
        self._activePokemon = None
        self._pokemon.clear(pokemon)
        self._activePokemon = self._pokemon[0]

