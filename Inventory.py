class Inventory:
    """
    Class that creates a new inventory 
    """
    def __init__(self, freshWater, elixer, raspberry, pokebal, masterbal):
       
        self._freshWater = freshWater
        self._elixer = elixer
        self._raspberry = raspberry
        self._pokebal = pokebal
        self._masterbal = masterbal
        self._items = ["Fresh Water", "Elixer", "Raspberry", "Pokebal", "Masterbal"]

    def getFreshWater(self):
        return self._freshWater

    def getElixer(self):
        return self._elixer

    def getRaspberry(self):
        return self._raspberry

    def getPokebal(self):
        return self._pokebal

    def getMasterbal(self):
        return self._masterbal

    def getItems(self):
        return self._items

   









    def addFreshWater(self, amount):
        self._freshWater += amount

    def addElixer(self, amount):
        self._elixer += amount

    def addRaspberry(self, amount):
        self._raspberry += amount

    def addPokebal(self, amount):
        self._pokebal += amount

    def addMasterbal(self, amount):
        self._masterbal += amount

    def deleteFreshWater(self, amount):
        self._freshWater -= amount

    def deleteElixer(self, amount):
        self._elixer -= amount

    def deleteRaspberry(self, amount):
        self._raspberry -= amount

    def deletePokebal(self, amount):
        self._pokebal -= amount

    def deleteMasterbal(self, amount):
        self._masterbal -= amount

