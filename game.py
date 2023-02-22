import random
from tkinter import *
from functools import partial
import tkinter as tk
from PIL import ImageTk, Image
import copy



def findItem(mainPlayer):
    probFreshWater = .3
    probElixer = .2
    probRaspberry = .2
    probPokebal = .2
    dice = random.random()
    inventory = mainPlayer.getInventory()

    if(dice < probFreshWater):
        item = "Fresh Water"
        inventory.addFreshWater(1)
    elif(dice < (probFreshWater + probElixer)):
        item = "Elixer"
        inventory.addElixer(1)
    elif(dice < (probFreshWater + probElixer + probRaspberry)):
        item = "Raspberry"
        inventory.addRaspberry(1)
    elif(dice < (probFreshWater + probElixer + probRaspberry + probPokebal)):
        item = "Pokebal"
        inventory.addPokebal(1)
    else:
        item = "Masterbal"
        inventory.addMasterbal(1)
    return item

def generateImage(symbol):
    if(symbol == ":"):
        image = Image.open("Images/longGrass2.jpg")
    if(symbol == "!"):
        image = Image.open("Images/enemy.png")
    if(symbol == "."):
        image = Image.open("Images/smallGrass2.jpg")
    if(symbol == "#"):
        image = Image.open("Images/stone2.jpg")
    if(symbol == ";"):
        image = Image.open("Images/path.png")
    if(symbol == "x"):
        image = Image.open("Images/Player.jpg")
    if(symbol == "x:"):
        image = Image.open("Images/playerInPlant.png")
    if(symbol == "x;"):
        image = Image.open("Images/playerOnPath.png")
    if(symbol == "I"):
        image = Image.open("Images/entryPointLeft.png")
    if(symbol == "II"):
        image = Image.open("Images/entryPointMiddle.png")
    if(symbol == "III"):
        image = Image.open("Images/entryPointRight.png")
    return image


def generateMap(length_map = 10, width_map = 10, prob_stone = .20, prob_player = .05):
    """
    Genereer de speelkaart
    Parameters
    ----------
    length_map: int
        Lengte van de kaart
    width_map: int
        Breedte van de kaart
    prob_stone: float
        Kans om steen te genereren
    Returns
    -------
    De gegenereerde kaart
    """
    game_map = []
    for i in range(length_map):
        game_map_row = []
        for j in range(width_map):
            # Kijk of de buur lang gras is
            prob_long_gras = .25
            if j > 0:
                if game_map_row[-1] == ':':
                    prob_long_gras = .5
            if i > 0:
               
                if game_map[-1][i] == ':':
                    prob_long_gras = .5
            
            dice = random.random()
            if dice < prob_player:
                game_map_row.append("!")
            elif dice < prob_player + prob_stone:
                game_map_row.append("#")
            elif dice < prob_long_gras + prob_stone:
                game_map_row.append(":")
            else:
                game_map_row.append(".")
        game_map.append(game_map_row)
    return game_map

      
def changeBool(reverse):
    if reverse == True:
        reverse = False
    elif reverse == False:
        reverse = True
    return reverse


def findBestAction():
    global dataSet
    bestAction = 0
    bestResult = 0
    bestResultFatal = 0
    winningResult = True
    fatalResult = False
    print(len(dataSet))
    print(dataSet[len(dataSet)-1])
    print(dataSet)

    for action, result, winning, fatal in dataSet:
        if fatalResult == False:
            if(bestResult < result):
                bestAction = action
                bestResult = result
                winningResult = winning
            if(fatal == True):
                fatalResult = True
        if fatalResult == True:
            if(bestResultFatal < result):
                bestAction = action
                bestResultFatal = result
                winningResult = winning

    """
    if(winningResult == False):
        chanceAIRuns = 0.3
        dice = random.random()
        if(dice < chanceAIRuns):
            bestAction = "Run"
    """
    return bestAction


def enemyAI(player1, pokemonPlayer1, player2, pokemonPlayer2, maxlevel, reverse = False, startAction = "", level = 1, result = 0):    
    global dataSet

    if(level == 1):
        dataSet = []

    if(reverse == False):        # mainPlayer is the enemy player (main player in eye of AI)
        mainPlayer = copy.deepcopy(player1) 
        playerPokemon = copy.deepcopy(pokemonPlayer1)
        enemyPlayer= copy.deepcopy(player2)
        enemyPokemon = copy.deepcopy(pokemonPlayer2)     
    else:
        mainPlayer = copy.deepcopy(player2) 
        playerPokemon = copy.deepcopy(pokemonPlayer2)
        enemyPlayer = copy.deepcopy(player1)
        enemyPokemon = copy.deepcopy(pokemonPlayer1)
    
    playerPP = int(playerPokemon.getPP())
    playerHP = int(playerPokemon.getHP())
    playerMaxHP = int(playerPokemon.getMaxHP())
    playerMaxPP = int(playerPokemon.getMaxPP())
    
    enemyPP= int(enemyPokemon.getPP())
    enemyHP = int(enemyPokemon.getHP())
    enemyMaxHP = int(enemyPokemon.getMaxHP())
    enemyMaxPP = int(enemyPokemon.getMaxPP())
    
    reverse = changeBool(reverse)

    possibleActions = ["Attack","Bag"]
    
    fatal = False
    counter = 0

    #change in HP for output

    if(level == 1):
        resultOutput = []

    for action in possibleActions:
        counter += 1
        if (action == "Attack"):
            attacks = playerPokemon.getAttacks()
           
            for attack in attacks:
                cost = int(attack.getPPCost())
                if(cost <= playerPP):
                    counter += 1
                    effect = int(attack.getEffect())
                    
                    resultPPPlayer = playerPP - cost
                    resultHPEnemy = enemyHP - effect
                    if (resultHPEnemy <= 0):
                        resultHPEnemy = 0
                        if(reverse == True):
                            fatal = True
                    profitAttack = enemyHP - resultHPEnemy
                    
                    result += profitAttack
                    
                    
                    if(level == 1):
                        startAction = attack.getName()
                        resultOutput.append((startAction, resultHPEnemy, resultPPPlayer))

                    if(level == maxlevel or fatal == True):
                        if(playerHP > resultHPEnemy):
                            if(reverse == False):
                                winning = True
                            else:
                                winning = False
                        else:
                            if(reverse == False):
                                winning = False
                            else:
                                winning = True
                        
                        actionProfit = (startAction, result, winning, fatal)
                        dataSet.append(actionProfit)
                    else:
                        enemyPokemon.setHP(resultHPEnemy)
                        playerPokemon.setPP(playerPP - cost)
                        enemyAI(mainPlayer, playerPokemon, enemyPlayer, enemyPokemon, maxlevel, reverse, startAction, level + 1, result)
                        enemyPokemon.setHP(enemyHP)
                        playerPokemon.setPP(playerPP)
                    result -= profitAttack
    
        if (action == "Bag"):
            inventory = mainPlayer.getInventory()
            items = inventory.getItems()
            for item in items:
                HPChange = 0
                PPChange = 0
                if (item == "Fresh Water"):
                    freshWater = inventory.getFreshWater()
                    if (freshWater > 0):
                        HPChange = 15
                        inventory.deleteFreshWater(1)
                    else:
                        continue
                if (item == "Elixer"):
                    elixer = inventory.getElixer()
                    if (elixer > 0):
                        HPChange = 0
                        PPChange = 10
                        inventory.deleteElixer(1)
                    else:
                        continue
                if (item == "Raspberry"):
                    raspberry = inventory.getRaspberry()
                    if (raspberry > 0):
                        HPChange = 5
                        PPChange = 5
                        inventory.deleteRaspberry(1)
                    else:
                        continue
                if (item == "Pokebal"):
                    pokebal = inventory.getPokebal()
                    if (pokebal > 0 and playerHP < 10):
                        HPChange = enemyMaxHP
                        inventory.deletePokebal(1)
                        fatal = True
                    else:
                        continue
                if (item == "Masterbal"):
                    masterbal = inventory.getMasterbal()
                    if (masterbal > 0 and enemyHP < 20):
                        HPChange = enemyMaxHP
                        inventory.deleteMasterbal(1)
                        fatal = True
                    else:
                        continue   
                playerHP2 = playerHP
                playerPP2 = playerPP

                playerHP2 += HPChange
                playerPP2 += PPChange

                if (playerHP2 > playerMaxHP):
                    playerHP2 = playerMaxHP
            
                profitItem = playerHP2 - playerHP
                
                if (playerPP2 > playerMaxPP):
                    playerPP2 = playerMaxPP

                result += profitItem
                    
                if(level == 1):
                    startAction = item
                    resultOutput.append((startAction, playerHP2, playerPP2))

                if(level == maxlevel):
                    if(playerHP > resultHPEnemy):
                        if(reverse == False):
                            winning = True
                        else:
                            winning = False
                    else:
                        if(reverse == False):
                            winning = False
                        else:
                            winning = True
                    actionProfit = (startAction, result, winning, fatal)
                    dataSet.append(actionProfit)
                else:
                    playerPokemon.setHP(playerHP2)
                    playerPokemon.setPP(playerPP2)
                    enemyAI(mainPlayer, playerPokemon, enemyPlayer, enemyPokemon, maxlevel, reverse, startAction, level + 1, result)
                    playerPokemon.setHP(playerHP)
                    playerPokemon.setPP(playerPP)
                
                result -= profitItem     
    if(level == 1):
        return resultOutput
    
