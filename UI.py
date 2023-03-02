from tkinter import *
from functools import partial
import tkinter as tk
from PIL import ImageTk, Image
import game
import Player
import DATA
import random
import copy


def Main():
    global locationPlayer               # stores tuple that holds the location of the mainplayer
    global gamemap                      # stores matrix that holds data for the different map elements
    global pokedex                      # stores object that contains data from all pokemon in the game
          
    locationPlayer = (3,1)              # setting start location mainplayer
    
    pokedex = DATA.makePokedex()        
    gamemap = game.generateMap() 

    generateUI()
    
    
#### Generate UI

def generateUI():
    """
    Creates all elements of the UI
    => gameFrame (generated with gamemap)
    => buttons (left,right,up,down - buttons + ENTER-button)
    => console that displays game progress
    => textBox where users can write
    """
    global root                         
    global gameFrame
    global go_left
    global go_right
    global go_down
    global go_up
    global console
    global textBox
    global enterButton
    global counter
    

    root = tk.Tk()

    root.geometry("800x800")
    root.title("Pokemon World")
    
    gameFrame = Frame(root, height=390, width=440, borderwidth=5, relief="solid")
    gameFrame.pack()

    # creating brown path on gamemap => symbol path = ;
    for i in range(10):
        gamemap[3][i] = ";"


    # creating full map
    i = 0
    for line in gamemap:
        j = 0
        for element in line:
            # creating pokecenter
            if (i,j) == (2,0):
                symbol = "I"
                image = game.generateImage(symbol) 
            elif (i,j) == (3,0):
                symbol = "II"
                image = game.generateImage(symbol)
            elif (i,j) == (4,0):
                symbol = "III"
                image = game.generateImage(symbol)
            # setting mainplayer on right location
            elif (i,j) == locationPlayer:
                symbol = "x;"
                image = game.generateImage(symbol)
            # creating rest of gamemap
            else:
                image = game.generateImage(element)

            n = i*43
            m = j*38

            imageResized = image.resize((43,38))

            test = ImageTk.PhotoImage(imageResized)

            label = tk.Label(gameFrame, image=test, borderwidth=0, highlightthickness=0)
            label.image = test

            # Position image
            label.place(x = n,y = m)
            j += 1
        i += 1

    # creating controlFrame with buttons

    controlFrame = Frame(root, height=150, width=170)

    leftButton = PhotoImage(file="Images/arrowLeft.png")
    go_left = Button(controlFrame ,command=partial(moveToPosition, move="LEFT"), state=DISABLED, image=leftButton, relief="solid", borderwidth=0)
    go_left.place(x = 0, y = 50)
    rightButton = PhotoImage(file="Images/arrowRight.png")
    go_right = Button(controlFrame, command=partial(moveToPosition, move="RIGHT"), state=DISABLED, image=rightButton, relief="solid", borderwidth=0)
    go_right.place(x = 107, y = 50)
    upButton = PhotoImage(file="Images/arrowUp.png")
    
    go_up = Button(controlFrame, command=partial(moveToPosition, move="UP"), state=DISABLED, image=upButton, relief="solid", borderwidth=0)
    go_up.place(x = 60, y = 0)
    downButton = PhotoImage(file="Images/arrowDown.png")
    go_down = Button(controlFrame, command=partial(moveToPosition, move="DOWN"), state=DISABLED, image=downButton, relief="solid", borderwidth=0)
    go_down.place(x = 60, y = 87)

    controlFrame.pack()
    
    
    console = Text(root, height=12, width=80)

    textBox = Text(root, height=1, width=35)
    console.pack()
    textBox.pack()

    
    enterButton = Button(root, text="ENTER",command=enterText)
    enterButton.pack()

    console.insert(tk.END, "Welcome to the world of Pokemon\nWhat is your name?")
    console.config(state=DISABLED)
    

    # this counter will decide which program paths to take
    counter = 0


    root.mainloop()

#### First Line Game Engine

def moveToPosition(move):
    """
    moves mainplayer to new position on the game map (if position is available)
    
    params
    --------
    str move => value ("LEFT", "RIGHT", "DOWN" or "UP")
    
    """
    global locationPlayer
    global root
    global gameFrame
    global counter
    global playerBattle

    # depending on value of the "move" variable => getting coordinates of new location

    if (move == "LEFT"):
        l = list(locationPlayer)
        l[0] = l[0] - 1
        newLocation = tuple(l)
        
    if (move == "RIGHT"):
        l = list(locationPlayer)
        l[0] = l[0] + 1
        newLocation = tuple(l)

    if (move == "UP"):
        l = list(locationPlayer)
        l[1] = l[1] - 1
        newLocation = tuple(l)

    if (move == "DOWN"):
        l = list(locationPlayer)
        l[1] = l[1] + 1
        newLocation = tuple(l)
    
    # check if new location is walkable => walkable? => change Image of old and new Location to images that matches gamemap symbols (ex. : => long grass)
    
    (i,j) = newLocation
    locations = [0,1,2,3,4,5,6,7,8,9,10,11]
    
    if(gamemap[i][j] == "#" or gamemap[i][j] == "!"):                      # not walkable if new location is rock or other player
        print("no access")
    elif(((i,j) == (2,0)) or ((i,j) == (3,0)) or ((i,j) == (4,0))):        # not walkable if new location is on pokecenter
        print("no access")

    elif(i in locations and j in locations):                               # not walkable if new location is outside the gamemap
        (a,b) = locationPlayer

        # changing image old location

        symbolOldLocation = gamemap[a][b]
    
        image = game.generateImage(symbolOldLocation)

        imageResized = image.resize((43,38))
        test = ImageTk.PhotoImage(imageResized)

        n = a*43
        m = b*38

        label1 = tk.Label(gameFrame, image=test, borderwidth=0, highlightthickness=0)
        label1.image = test

        label1.place(x = n,y = m)

        # changing image new location

        symbol = "x"
        (i,j) = newLocation

        if(gamemap[i][j] == ":"):
            symbol = "x:"
            image = game.generateImage(symbol)
        elif(gamemap[i][j] == ";"):
            symbol = "x;"
            image = game.generateImage(symbol)
        else:
            image = game.generateImage(symbol)

        imageResized = image.resize((43,38))

        test = ImageTk.PhotoImage(imageResized)

        n = i*43
        m = j*38

        label1 = tk.Label(gameFrame, image=test, borderwidth=0, highlightthickness=0)
        label1.image = test

        label1.place(x = n,y = m)

        locationPlayer = newLocation

        # mainplayer Interaction with long grass and other enemy players
        # if mainplayer stands next to ([i + 1][j] or [i - 1][j]) or before ([i][j - 1]) enemy player => User has to fight enemy player

        if(gamemap[i][j - 1] == "!" or gamemap[i + 1][j] == "!" or gamemap[i - 1][j] == "!"):
            playerBattle = True
            counter = 7
            battle()

        # if mainplayer's new location is long grass => player can fight a pokemon (20%), find items (10%) or find nothing

        if(gamemap[i][j] == ":"):
            probItem = .1
            probPokemon = .2
            dice = random.random()
            if (dice < probItem):
                item = game.findItem(mainPlayer)
                console.config(state=NORMAL)
                console.insert(tk.END, f"\nYou found one {item}. This item has been added to your inventory.")
                console.insert(tk.END, "\nCheck your inventory by typing 'BAG'")
                console.insert(tk.END, "\nCheck your pokemon by typing 'POKEMON'")
                console.config(state=DISABLED)
            elif (dice < probItem + probPokemon):
                counter = 6
                playerBattle = False
                battle()

        root.mainloop()
 

def enterText():
    """
    Gets activated when 'Enter' Button is pressed
    Counter variable defines where program needs to go
    -----------
    counter < 3
        => Game startup (asking player name + chosing first pokemon)
    counter > 3 and counter < 6
        => Player can run around and check his inventory / catched pokemons
    counter > 5
        => Player is in battle mode (move buttons doesn't work)
    """
    global counter
    global choice
    global inputText
    inputText = textBox.get(1.0, "end-1c")
    textBox.delete('1.0', END)
    if (counter < 3):
        startGame()
    elif (counter < 6):
        mainGame()
    elif (counter > 5):
        battle()

def startGame():
    if(counter < 1):
        createMainPlayer()
    elif(counter < 3):
        chooseFirstPokemon()
    elif(counter == 3):
        mainGame()


def createMainPlayer():
    """
    Creates mainplayer and asks for its name

    """
    global mainPlayer
    global counter
    global savedText
    global inputText
    savedText = "\n"
    if (inputText == ""):
        console.config(state=NORMAL)
        console.insert(tk.END, "\nGive a valid name!")
        console.config(state=DISABLED)
    else:
        savedText += "Hello "
        savedText += inputText
        console.config(state=NORMAL)
        console.insert(tk.END, savedText)
        console.config(state=DISABLED)
        counter += 1
        mainPlayer = Player.Player(inputText, False)
        mainPlayer.addInventory(DATA.createInventoryMainPlayer())
        chooseFirstPokemon()


def chooseFirstPokemon(starters = ['Bulbasaur', 'Charmander', 'Squirtle']):
    """
    Lets mainplayer choose his first pokemon.

    """
    global pokedex
    global counter
    global choice
    global inputText
    if (counter == 1):
        starter = starters[0]
        mainPokemon = pokedex.getPokemon(starter)
        console.config(state=NORMAL)
        console.insert(tk.END, f"\nWhich start Pokemon do you choose?\nYou have the choice between {starters[0]}, {starters[1]} and {starters[2]}")
        console.insert(tk.END, f"\nDo you choose {starter}: HP {mainPokemon.getHP()}, PP {mainPokemon.getPP()} [next or select] ")
        console.config(state=DISABLED)
        counter += 1
        choice = 0
    elif (counter == 2):
        if (inputText.upper() == "SELECT"):
            starter = starters[choice]
            mainPokemon = pokedex.getPokemon(starter)
            mainPlayer.addActivePokemon(mainPokemon)
            console.config(state=NORMAL)
            console.insert(tk.END,f"\nCongrats, You chose {starter} as your first pokemon")
            console.insert(tk.END,"\nClick on Enter to start the game")
            console.config(state=DISABLED)
            counter += 1
        elif (inputText.upper() == "NEXT"):
            choice = (choice + 1) % 3
            starter = starters[choice]
            mainPokemon = pokedex.getPokemon(starter)
            console.config(state=NORMAL)
            console.insert(tk.END, f"\nDo you choose {starter}: HP {mainPokemon.getHP()}, PP {mainPokemon.getPP()} [next or select] ")
            console.config(state=DISABLED)
        else:
            console.config(state=NORMAL)
            console.insert(tk.END, "\nNo valid input, choose 'NEXT' or 'SELECT'")
            console.config(state=DISABLED)

def mainGame():
    """
    Lets mainplayer run around the map with the enabled move buttons

    """
    global counter
    if(counter == 3):
        go_left.config(state=NORMAL)
        go_right.config(state=NORMAL)
        go_down.config(state=NORMAL)
        go_up.config(state=NORMAL)
        console.config(state=NORMAL)
        console.delete('1.0', END)
        console.insert(tk.END, "Welcome to pokemon world, you can start exploring")
        console.insert(tk.END, "\nCheck your inventory by typing 'BAG'")
        console.insert(tk.END, "\nCheck your pokemon by typing 'POKEMON'")
        console.config(state=DISABLED)
        counter += 1
    elif(counter == 4):
        if(inputText.upper() == "BAG"):
            inventory = mainPlayer.getInventory()
            items = inventory.getItems()
            console.config(state=NORMAL)
            console.insert(tk.END, f"\nYour Bag:")
            for item in items:
                if(item == "Fresh Water"):
                    console.insert(tk.END, f"\n-{item}: {inventory.getFreshWater()}")
                if(item == "Elixer"):
                    console.insert(tk.END, f"\n-{item}: {inventory.getElixer()}")
                if(item == "Raspberry"):
                    console.insert(tk.END, f"\n-{item}: {inventory.getRaspberry()}")
                if(item == "Pokebal"):
                    console.insert(tk.END, f"\n-{item}: {inventory.getPokebal()}")
                if(item == "Masterbal"):
                    console.insert(tk.END, f"\n-{item}: {inventory.getMasterbal()}")
            console.insert(tk.END, "\nClick on Enter to go back")
            console.config(state=DISABLED)
            counter += 1
        if(inputText.upper() == "POKEMON"):
            pokemonList = mainPlayer.getPokemon()
            console.config(state=NORMAL)
            console.insert(tk.END, f"\nYour pokemon:")
            for pokemon in pokemonList:
                console.insert(tk.END, f"\n- Name: {pokemon.getName()}, HP: {pokemon.getHP()}, PP: {pokemon.getPP()}, Primary Type: {pokemon.getPrimaryType()}, Speed: {pokemon.getSpeed()}")
            console.insert(tk.END, "\nClick on Enter to go back")
            counter += 1
    elif(counter == 5):
        go_left.config(state=NORMAL)
        go_right.config(state=NORMAL)
        go_down.config(state=NORMAL)
        go_up.config(state=NORMAL)
        console.config(state=NORMAL)
        console.delete('1.0', END)
        console.insert(tk.END, "Check your inventory by typing 'BAG'")
        console.insert(tk.END, "\nCheck your pokemon by typing 'POKEMON'")
        console.config(state=DISABLED)
        counter -= 1

def battle():
    """
    Mainplayer is in battle mode with 
        => Pokemon in grass OR
        => Pokemon of enemy player

    """
    global counter
    global playerBattle
    go_left.config(state=DISABLED)
    go_right.config(state=DISABLED)
    go_down.config(state=DISABLED)
    go_up.config(state=DISABLED)
    if(counter < 17):
        attackMainPlayer()
    else:
        if(playerBattle == True):
            attackEnemyPlayer()
        else:
            attackEnemyPokemon()


def attackMainPlayer():
    global counter
    global enemyPokemon
    global playerPokemon
    global enemyPlayer
    global enemyPokemonNoCopy
    global playerPokemonNoCopy
    """
    Mainplayer's move, there are two main paths
        => Mainplayer <=> Pokemon in grass [playerbattle = False]
        => Mainplayer <=> Pokemon of enemy player [playerbattle = True] 
    """
    
    if(counter == 6):
        playerPokemonNoCopy = mainPlayer.getActivePokemon()
        enemyPokemonNoCopy = pokedex.chooseRandomPokemon()
        playerPokemon = copy.deepcopy(playerPokemonNoCopy)
        enemyPokemon = copy.deepcopy(enemyPokemonNoCopy)        
        console.config(state=NORMAL)
        console.insert(tk.END, f"\nWauw, a wild {enemyPokemon.getName()} showed up.\nDo you want to fight? (active pokemon = {playerPokemon.getName()})\nType 'Fight' to fight or type 'Run' to run away")
        console.config(state=DISABLED)
        counter = 8
    elif(counter == 7):
        names = ["Garry","Brock","Ash","Misty","Dirk","Josch","Melina","Jade"]
        enemyPlayer = Player.Player(random.choice(names), True)
        enemyPlayer.addInventory(DATA.createInventoryMainPlayer())
        playerPokemonNoCopy = mainPlayer.getActivePokemon()
        enemyPokemonNoCopy = pokedex.chooseRandomPokemon()  
        playerPokemon = copy.deepcopy(playerPokemonNoCopy)
        enemyPokemon = copy.deepcopy(enemyPokemonNoCopy)
        enemyPlayer.addActivePokemon(enemyPokemon)        
        console.config(state=NORMAL)
        console.insert(tk.END, f"\n{enemyPlayer.getName()} wants to battle!\n{enemyPlayer.getName()} chooses {enemyPokemon.getName()}\nPress Enter to continue")
        console.config(state=DISABLED)
        counter = 8
    elif(counter == 8):
        if(playerBattle == True):
            counter = 9
        elif(inputText.upper() == "FIGHT"):
            counter = 9
        elif(inputText.upper() == "RUN"):
            counter = 15
    if(counter == 9):
        console.config(state=NORMAL)
        console.delete('1.0', END)
        console.insert(tk.END, f"Battle with {enemyPokemon.getName()}. Stats = HP: {enemyPokemon.getHP()}/{enemyPokemon.getMaxHP()}, PP: {enemyPokemon.getPP()}/{enemyPokemon.getMaxPP()}, Primary Type: {enemyPokemon.getPrimaryType()}, Speed: {enemyPokemon.getSpeed()}")
        console.insert(tk.END, f"\nYour active pokemon: {playerPokemon.getName()}. Stats = HP: {playerPokemon.getHP()}/{playerPokemon.getMaxHP()}, PP: {playerPokemon.getPP()}/{playerPokemon.getMaxPP()}, Primary Type: {playerPokemon.getPrimaryType()}, Speed: {playerPokemon.getSpeed()}")
        console.insert(tk.END, "\n-Type 'attack' to perform an attack with your pokemon")
        console.insert(tk.END, "\n-Type 'change' to change your active pokemon")
        console.insert(tk.END, "\n-Type 'bag' to use item from inventory")
        console.insert(tk.END, "\n-Type 'run' to run away")
        console.config(state=DISABLED)
        counter = 10
    
    elif(counter == 10):
        if(inputText.upper() == "ATTACK"):
            console.config(state=NORMAL)
            console.delete('1.0', END)
            console.insert(tk.END, f"Battle with {enemyPokemon.getName()}. Stats = HP: {enemyPokemon.getHP()}/{enemyPokemon.getMaxHP()}, PP: {enemyPokemon.getPP()}/{enemyPokemon.getMaxPP()}, Primary Type: {enemyPokemon.getPrimaryType()}, Speed: {enemyPokemon.getSpeed()}")
            console.insert(tk.END, f"\nYour active pokemon: {playerPokemon.getName()}. Stats = HP: {playerPokemon.getHP()}/{playerPokemon.getMaxHP()}, PP: {playerPokemon.getPP()}/{playerPokemon.getMaxPP()}, Primary Type: {playerPokemon.getPrimaryType()}, Speed: {playerPokemon.getSpeed()}")
            attacks = playerPokemon.getAttacks()
            for attack in attacks:
                console.config(state=NORMAL)
                console.insert(tk.END, f"\nType '{attack.getName()}' to perform attack [PP Cost: {attack.getPPCost()}]")
            console.insert(tk.END, f"\nType 'Back' to go back to the previous menu")
            console.config(state=DISABLED)    
            counter = 11

        if(inputText.upper() == "CHANGE"):
            pokemonList = mainPlayer.getPokemon()
            console.config(state=NORMAL)
            console.insert(tk.END, f"\nYour pokemon:")
            for pokemon in pokemonList:
                console.insert(tk.END, f"\n- Name: {pokemon.getName()}, HP: {pokemon.getHP()}/{pokemon.getMaxHP()}, PP: {pokemon.getPP()}/{pokemon.getMaxPP()}, Primary Type: {pokemon.getPrimaryType()}, Speed: {pokemon.getSpeed()}")    
            console.insert(tk.END, "\nType in the name of your pokemon, like 'Name Pokemon' to change your active pokemon")
            console.insert(tk.END, "\nType in 'Back' to go back to the previous menu")
            console.config(state=DISABLED)
            counter = 12
                
        if(inputText.upper() == "BAG"):
            inventory = mainPlayer.getInventory()
            items = inventory.getItems()
            console.config(state=NORMAL)
            console.insert(tk.END, f"\nYour Bag:")
            for item in items:
                if(item == "Fresh Water"):
                    console.insert(tk.END, f"\n-{item}: {inventory.getFreshWater()}")
                if(item == "Elixer"):
                    console.insert(tk.END, f"\n-{item}: {inventory.getElixer()}")
                if(item == "Raspberry"):
                    console.insert(tk.END, f"\n-{item}: {inventory.getRaspberry()}")
                if(item == "Pokebal"):
                    console.insert(tk.END, f"\n-{item}: {inventory.getPokebal()}")
                if(item == "Masterbal"):
                    console.insert(tk.END, f"\n-{item}: {inventory.getMasterbal()}")
            console.insert(tk.END, "\nType in 'back' to go back")
            console.insert(tk.END, "\nType in the name of the item, like 'name item', to use item")
            console.config(state=DISABLED)
            counter = 13
        if(inputText.upper() == "RUN"):
            counter = 15
     
    elif(counter == 11):
        attacks = playerPokemon.getAttacks()
        for attack in attacks:
            if(inputText.upper() == attack.getName().upper()):
                effect = attack.getEffect()
                PPCost = attack.getPPCost()
                if((int(playerPokemon.getPP()) - int(PPCost)) >= 0): 
                    playerPokemon.setPP(int(playerPokemon.getPP()) - int(PPCost))
                    enemyPokemon.setHP(int(enemyPokemon.getHP()) - int(effect))
                    console.config(state=NORMAL)
                    console.insert(tk.END, f"\n{playerPokemon.getName()} uses {attack.getName()}. Damage: {effect} HP")
                    console.insert(tk.END, f"\nResult: {enemyPokemon.getName()} has {enemyPokemon.getHP()} HP left")
                    console.config(state=DISABLED)
                else:
                    console.config(state=NORMAL)
                    console.insert(tk.END, f"\nYour pokemon doesn't have enough PP")
                    console.config(state=DISABLED)
                counter = 14
            elif(inputText.upper() == "BACK"):
                console.config(state=NORMAL)
                console.insert(tk.END, f"\nPress enter to continue")
                console.config(state=DISABLED)
                counter = 9
                attackMainPlayer()
    elif(counter == 12):
        pokemonList = mainPlayer.getPokemon()
        for pokemon in pokemonList:
            if(pokemon.getName().upper() == inputText.upper()):
                mainPlayer.setActivePokemon(pokemon)
                console.config(state=NORMAL)
                console.insert(tk.END, f"\nYour active pokemon has changed to {mainPlayer.getActivePokemon().getName()}")
                console.config(state=DISABLED)
                playerPokemonNoCopy = mainPlayer.getActivePokemon()
                playerPokemon = copy.deepcopy(playerPokemonNoCopy)
                counter = 14
        if(inputText.upper() == "BACK"):
            counter = 9
            attackMainPlayer()

    elif(counter == 13):
        inventory = mainPlayer.getInventory()  
        if("FRESH WATER" == inputText.upper()):
            if(inventory.getFreshWater() > 0):
                console.config(state=NORMAL)
                console.insert(tk.END, f"\nYou used one Fresh Water on {playerPokemon.getName()}")
                console.config(state=DISABLED)
                playerPokemon.setHP(int(playerPokemon.getHP()) + 15)
                inventory.deleteFreshWater(1)
            else:
                console.config(state=NORMAL)
                console.insert(tk.END, f"\nYou don't have any Fresh Water anymore")
                console.config(state=DISABLED)
            counter = 14
        if("ELIXER" == inputText.upper()):
            if(inventory.getElixer() > 0):
                console.config(state=NORMAL)
                console.insert(tk.END, f"\nYou used one Elixer on {playerPokemon.getName()}")
                playerPokemon.setPP(int(playerPokemon.getPP()) + 10)
                console.config(state=DISABLED)
                inventory.deleteElixer(1)
            else:
                console.config(state=NORMAL)
                console.insert(tk.END, f"\nYou don't have any Elixers anymore")
                console.config(state=DISABLED)
            counter = 14
        if("RASPBERRY" == inputText.upper()):
            if(inventory.getRaspberry() > 0):
                console.config(state=NORMAL)
                console.insert(tk.END, f"\nYou used one Raspberry on {playerPokemon.getName()}")
                playerPokemon.setPP(int(playerPokemon.getPP()) + 5)
                playerPokemon.setHP(int(playerPokemon.getHP()) + 5)
                console.config(state=DISABLED)
                inventory.deleteRaspberry(1)
            else:
                console.config(state=NORMAL)
                console.insert(tk.END, f"\nYou don't have any Raspberry's anymore")
                console.config(state=DISABLED)
            counter = 14
        if("POKEBAL" == inputText.upper()):
            if(inventory.getPokebal() > 0):
                console.config(state=NORMAL)
                console.insert(tk.END, f"\nYou throw a Pokebal to {enemyPokemon.getName()}")
                if(int(enemyPokemon.getHP() < 10)):
                    console.insert(tk.END, f"You catched {enemyPokemon.getName()}, your newly catched pokemon has been added to your collection.")
                    console.insert(tk.END, "\nYou win the game")
                    console.insert(tk.END, f"\nPress Enter to continue")
                    mainPlayer.addPokemon(enemyPokemon)
                    counter = 5
                else:
                    console.insert(tk.END, f"\nYou couldn't catch {enemyPokemon.getName()}, this pokemon is still too strong")
                    counter = 14
                inventory.deletePokebal(1)
                console.config(state=DISABLED)
            else:
                console.config(state=NORMAL)
                console.insert(tk.END, f"\nYou don't have any Pokebals anymore")
                console.config(state=DISABLED)
                counter = 14
        if("MASTERBAL" == inputText.upper()):
            if(inventory.getMasterbal() > 0):
                console.config(state=NORMAL)
                console.insert(tk.END, f"\nYou throw a Masterbal to {enemyPokemon.getName()}")
                if(int(enemyPokemon.getHP() < 20)):
                    console.insert(tk.END, f"\nYou catched {enemyPokemon.getName()}, your newly catched pokemon has been added to your collection.")
                    console.insert(tk.END, "\nYou win the game")
                    console.insert(tk.END, f"\nPress Enter to continue")
                    mainPlayer.addPokemon(enemyPokemon)
                    counter = 5
                else:
                    console.insert(tk.END, f"\nYou couldn't catch {enemyPokemon.getName()}, this pokemon is still too strong")
                    counter = 15
                inventory.deleteMasterbal(1)
                console.config(state=DISABLED)
            else:
                console.config(state=NORMAL)
                console.insert(tk.END, f"\nYou don't have any Masterbals anymore")
                console.config(state=DISABLED)
                counter = 14
        if("BACK" == inputText.upper()):
            counter = 9
            attackMainPlayer()  

    if (counter == 14):
        if(int(enemyPokemon.getHP()) <= 0):
            console.config(state=NORMAL)
            console.insert(tk.END, "\nYou win the game")
            console.insert(tk.END, "\nPress Enter to continue")
            console.config(state=DISABLED)
            counter = 5
        else:
            console.config(state=NORMAL)
            console.insert(tk.END, f"\n{enemyPokemon.getName()}'s turn!")
            console.insert(tk.END, "\nPress Enter to continue")
            console.config(state=DISABLED)
            counter = 17   
    
    if(counter == 15):
        if(playerBattle == True):
            speedEnemy = enemyPokemon.getSpeed()
            speedPlayer = playerPokemon.getSpeed()
            if(speedEnemy >= speedPlayer):
                console.config(state=NORMAL)
                console.insert(tk.END, "\nYou can't run away, the enemy pokemon is faster than yours")
                console.insert(tk.END, "\nPress Enter to continue")
                console.config(state=DISABLED)
                counter = 17
            else:
                console.config(state=NORMAL)
                console.insert(tk.END, "\nYou ran away succesfully")
                console.insert(tk.END, "\nPress Enter to continue")
                console.config(state=DISABLED)
                counter = 5
        else:
            console.config(state=NORMAL)
            console.insert(tk.END, "\nYou ran away succesfully")
            console.insert(tk.END, "\nPress Enter to continue")
            console.config(state=DISABLED)
            counter = 5
    if(counter == 16):
        if(mainPlayer.getActivePokemon() == ""):
            console.config(state=NORMAL)
            console.delete('1.0', END)
            console.insert(tk.END, "You have no pokemon anymore")
            console.insert(tk.END, "\nGame Over!!!")
            console.config(state=DISABLED)
        else:
            counter = 5
            console.delete('1.0', END)
            console.insert(tk.END, "You still have pokemon.\nYou can continue the game!")
            console.config(state=DISABLED)


def attackEnemyPokemon():
    """
    Attack of enemy pokemon (mainplayer <=> pokemon in grass)
    Enemy pokemon chooses random attack from the attack list

    """
    global counter
    global enemyPokemon
    global playerPokemon
    
    attacks = enemyPokemon.getAttacks()
    attack = random.choice(attacks)
    effect = attack.getEffect()
    PPCost = attack.getPPCost()
    if(int(enemyPokemon.getPP()) - int(PPCost) > 0):
        enemyPokemon.setPP(int(enemyPokemon.getPP()) - int(PPCost))
        playerPokemon.setHP(int(playerPokemon.getHP()) - int(effect))
        console.config(state=NORMAL)
        console.insert(tk.END, f"\n{enemyPokemon.getName()} uses {attack.getName()}. Damage: {effect} HP")
        console.insert(tk.END, f"\nResult: {playerPokemon.getName()} has {playerPokemon.getHP()} HP left")
        
        if(int(playerPokemon.getHP()) <= 0):
                console.insert(tk.END, "\nYou lose the game")
                console.insert(tk.END, f"\nPress Enter to continue")
                console.config(state=DISABLED)
                playerPokemon.setHP(1)
                counter = 5
        else:
            console.insert(tk.END, f"\nPress Enter to continue")
            console.config(state=DISABLED)
            counter = 9
    else:
        console.config(state=NORMAL)
        console.insert(tk.END, f"\nThe enemy pokemon doesn't have enough PP")
        console.insert(tk.END, f"\nPress Enter to continue")
        console.config(state=DISABLED)
        counter = 9


def attackEnemyPlayer():
    """
    Attack of enemy player (mainplayer <=> pokemon of enemy player)
    Enemy player chooses best possible action with the enemyAI function
    
    """
    global counter
    global playerBattle
    global mainPlayer
    global playerPokemonNoCopy
    global enemyPokemonNoCopy
    
    maxlevel = 4
    resultOutput = game.enemyAI(mainPlayer, playerPokemon, enemyPlayer, enemyPokemon, maxlevel)
    bestAction = game.findBestAction()
    print(bestAction)
    print(resultOutput)
    print("counter is")
    print(counter)

    for action, HP, PP in resultOutput:
        attacks = enemyPokemon.getAttacks()
        for attack in attacks:
            if (bestAction == action and bestAction == attack.getName()):
                print("checkkkk")
                playerPokemon.setHP(HP)
                enemyPokemon.setPP(PP)
                console.config(state=NORMAL)
                console.insert(tk.END, f"\n{enemyPokemon.getName()} uses {attack.getName()}. Damage: {attack.getEffect()}")
                console.insert(tk.END, f"\nResult: {playerPokemon.getName()} has {playerPokemon.getHP()} HP left")
                console.config(state=DISABLED)

        inventory = enemyPlayer.getInventory()
        items = inventory.getItems()
        for item in items:
            if ((item == "Masterbal" and bestAction == action and action == "Masterbal") or (item == "Pokebal" and bestAction == action and action == "Pokebal")):
                print("counter")
                console.config(state=NORMAL)
                console.insert(tk.END, f"\nThe enemy catched your {playerPokemon.getName()}")
                console.insert(tk.END, "\nYou lost the game")
                console.insert(tk.END, f"\nPress Enter to continue")
                console.config(state=DISABLED)
                mainPlayer.deletePokemon(playerPokemonNoCopy)
                counter = 16
            elif (bestAction == item and bestAction == action):
                print("checkk 3")
                enemyPokemon.setHP(HP)
                enemyPokemon.setPP(PP)
                console.config(state=NORMAL)
                console.insert(tk.END, f"\n{enemyPlayer.getName()} uses one {item}.")
                console.config(state=DISABLED)
        if(action == "Run"):
            console.config(state=NORMAL)
            console.insert(tk.END, "\nThe enemy player ran away!")
            console.insert(tk.END, "\nPress Enter to continue")
            console.config(state=DISABLED)
            counter = 5

    if(int(playerPokemon.getHP()) <= 0):
            console.config(state=NORMAL)
            console.insert(tk.END, "\nYou lose the game")
            console.insert(tk.END, "\nPress Enter to continue")
            console.config(state=DISABLED)
            counter = 5
    elif(counter == 17):
        console.config(state=NORMAL)
        console.insert(tk.END, f"\nPress Enter to continue")
        console.config(state=DISABLED)
        counter = 9
        playerBattle = True


Main()