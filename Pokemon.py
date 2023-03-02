class Pokemon:
    """
    Class that represents a pokeomon
    """
    def __init__(self, name, primaryType, secondarytype, hp, pp, defense, speed):
        """
        Creates a new pokemon
        """
        
        self._id = 0
        self._name = name
        self._primaryType = primaryType
        self._secondaryType = secondarytype
        self._hp = hp
        self._pp = pp
        self._maxhp = hp
        self._maxpp = pp
        self._defense = defense
        self._speed = speed
        self._aanvallen = []


    def getName(self):
        return self._name

    def getPrimaryType(self):
        return self._primaryType

    def getHP(self):
        return self._hp

    def getPP(self):
        return self._pp

    def getMaxHP(self):
        return self._maxhp

    def getMaxPP(self):
        return self._maxpp

    def getDefense(self):
        return self._defense

    def getSpeed(self):
        return self._speed

    def getAttacks(self):
        return self._aanvallen

    def incrementID(self):
        self._id += 1

    def setHP(self, HP):
        if(HP > int(self._maxhp)):
            self._hp = self._maxhp
        else:
            self._hp = HP

    def setPP(self, PP):
        if(PP > int(self._maxpp)):
            self._pp = self._maxpp
        else:
            self._pp = PP


    def voegAanvalToe(self, aanval):
        self._aanvallen.append(aanval)

    