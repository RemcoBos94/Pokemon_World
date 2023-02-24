class Attack:
    def __init__(self, Name, Type, PP_Cost, Effect):
        
        self._Name = Name
        self._Type = Type
        self._PP_Cost = PP_Cost
        self._Effect = Effect

    def getName(self):
        return self._Name

    def getType(self):
        return self._Type

    def getPPCost(self):
        return self._PP_Cost

    def getEffect(self):
        return self._Effect