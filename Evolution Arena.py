import random
import math
import NeuralNetwork
import warnings
#   CLASS : [Attack, Defense, Damage, Health, initative]
CLASSES = {'barbarian': [1, -2, 1, 1, 1], 'ranger': [2, 0, 2, 0, 1], 'rouge':[3, -3, 3, -3, 3], 'bard':[2, 2, -1, 3, 5], 'wizard': [5, -1, 2, 2, -2]}
#   RACE : [Move Towards, Move Away, Prepare]
RACES = {'human': [10,10,10], 'elf':[1,10,1], 'giant':[10,1,10],
         'dwarf':[1,10,10], 'dragonborn': [10,10,1], 'gnome': [1,1,10],
         'orc':[10,1,1]}

FIRST_NAMES = ['Eilaga','Prukain','Krusk','Devis','Jozan','Gimble','Eberk','Vadani','Tordek',
               'Ember','Grog','Percy','Arthur','Alhandra','Soveliss','Lidda','Hennet','Mialee',
               'Ragdar','Dian','Nese','Mae','Valhein','Dol','Earl','Cedria','Azulei','Yun','Cybel',
               'Donnie', 'Parker', 'Motley', 'Edward', 'Brick','Cumulous','Jacob','Bailey','Brock',
               'Caleb','Cathrine','Alexander','Alexandra','Anthony','Blaze','Gordon','Henry','Flexo',
               'Fry', 'Zach', 'Jeff', 'Geoff','Miles','Baker', 'Austin', 'Man','Alexis']

LAST_NAMES = ['Woodsoul','Carter','Licktenstein','Barton','Grimm','Ozul','Arkalis','Armanci','Baldric',
              'Ballard','Bilger','Blackstrand','Brightwater','Carnavon','Coldshore','Coyle','Cresthill',
              'Cuttlescar','Daargen','Drumwind','Dunhall','Fletcher','Fryft','Goldrudder','Lamoth',
              'Van Gandt','Van Hyden','Welfer','Strong', 'Stark', 'Darko', 'Kimera', 'The Short',
              'Coupled', 'Parker', 'Van Halen', 'Crue', 'Van Helsing', 'Cross', 'The Great', 'Lapiz',
              'Bano','Schnitzel','Erginheimer','Hammer','Sledge','Vendil','Causwell','Jeckle','Hyde',
              'Copley','Carroll','Balncila','King','Queen','Weaver','Kent','May','April','June','August',
              'July','Febrary','Septem','Nova','Birlovich','Wesgrovic','Wawrinka','Polit','Cof','Hoffertime',
              'Hammerdinckle','Picklty','Yomper','Winnenberg','Cruise','Trump','Obama','Gates','Jobs',
              'Mercury','Venus','Dirt','Flanders','Cruise','Saturn','Mars','Solar','Lunar','Celestial',
              'Jupiter','Uranas','Neptune','Pluto','Mouse','Kernal','Dink','Schoth','\'Aliah','Mcnaught',
              'McNeel','McPhereson','Skaggs','Scgoth','Heille','Hominer','Of the Night','The Brave',
              'The Mildly Brave','of War','of Camelot','of The Round Table', 'Olip','Cameniele','Texas']

FIGHTER_NUMBER = 50

GENERATION_NUMBER = 0


class Player:

    def __init__(self, kind, race, lastName):
        self.speed = self.movement = 25
        self.firstName = random.choice(FIRST_NAMES)
        self.kind = kind
        self.race = race
        self.range = self.getRange()
        self.minRange = self.getMinRange()
        self.lastName = lastName
        self.isDead = False
        self.isPrepared = False
        self.isPlayable = False
        self.attack = random.randint(-4, 5) + self.add(kind, 0)
        self.defense = random.randint(1, 15) + self.add(kind, 1)
        self.damage = random.randint(-4, 5) + self.add(kind, 2)
        #self.health = random.randint(20, 28) + self.add(kind, 3)
        self.health = random.randint(1, 8)
        self.maxHealth = self.health
        self.generation = GENERATION_NUMBER
        self.children = []
        if self.health <= 0:
            self.health = 1
        self.initative = random.randint(-2, 3) + self.add(kind, 4)
        self.isComment = True
        self.NN = NeuralNetwork.neuralNetwork(7, 6)
        self.goesFirst = False
        self.X = 0
        self.Y = 0
        self.Memory = [0,0,0,0,0,0]

        self.kills = 0
        self.damageDone = 0
        self.attacksTried = 0
        self.attackSuccess = 0
        self.turnsMoving = 0
        self.turnsPreparing = 0
        self.turnsStanding = 0
        self.actionPenaltyArr = [0,0,0,0,0,0]
        self.father = self

    def getAction(self, oppX, oppY):
        """
    Get 8 inputs and run them through the neural network, and make Move based on highest output.
    Inputs are as follows:
        0) isPrepared
        1) self x
        2) self y
        3) opponent X
        4) opponent T
        5) range max
        6) range min

    Outputs are as follows:
        0)Move Up
        1)Move Down
        2)Move Left
        3)Move Right
        4)Attempt an attack
        5)Pepare yourself
        """

        if self.isPrepared:
            prep = 1
        else:
            prep = 0

        self.NN.run([prep ,self.X, self.Y, oppX, oppY, self.range, self.minRange])
        
        if self.isPlayable:
            print('It is your turn!')
            print('The following are the inputs given to each player:')
            print('isPrepared:'+ str(prep))
            print('Self X:'+ str(self.X))
            print('Self Y:'+ str(self.Y))
            print('Opponent X:'+ str(oppX))
            print('Opponent Y:'+ str(oppY))
            print('Max Range:'+ str(self.range))
            print('Min Range:'+ str(self.minRange))
            print('\n\nPlease enter the desired outputs (ranges from 0.0 - 1.0):')
            try:
                up = float(input('Move Up --> '))
                down = float(input('Move Down --> '))
                left = float(input('Move Left --> '))
                right = float(input('Move Right --> '))
                attack = float(input('Attack --> '))
                prepare = float(input('Prepare --> '))
                desiredArr = [up,down,left,right,attack,prepare]
            except:
                desiredArr = [random.random(), random.random(),random.random(),random.random(),random.random(),random.random()]
            self.NN.backprop(desiredArr)
            self.NN.weights[-1] = desiredArr
            maxWeight = -1000.0
            maxNum = 0
            for count, weight in enumerate(desiredArr):
                if maxWeight < weight:
                    maxNum = count
                    maxWeight = weight
                
        #Find most activated neuron
        #Take off 10% for each time an action is used
        else:
            maxWeight = -1000.0
            maxNum = 0
            for count, weight in enumerate(self.NN.getOutput()):
                #Subtract action Penalty from each weight
                weight += -1 * self.actionPenaltyArr[count]

                #Check for maxNum
                if maxWeight < weight:
                    maxNum = count
                    maxWeight = weight

            #Add penalty to max num
            self.actionPenaltyArr[maxNum] += .1


        if maxNum == 0:
            return 'Up'
        elif maxNum == 1:
            return 'Down'
        elif maxNum == 2:
            return 'Left'
        elif maxNum == 3:
            return 'Right'
        elif maxNum == 4:
            return 'Attack'
        elif maxNum == 5:
            return 'Prepare'
        else:
            return 'Stand there Silly'

    def getMove(self, moveRate, direction):
        #The move speed, or total movement is relative to the weight that was outputed by the Neural Network
        #directon signals left or down
        if direction:
            return int(self.speed * -1 * abs(moveRate))
        else:
            return int(self.speed * abs(moveRate))

                
    def reset(self):
        #Resets the Fighters between rounds
        self.isDead = False
        self.isPrepared = False
        self.health = self.maxHealth
        self.bonus = 0
        self.dmgBonus = 0
        self.Memory = [0,0,0,0,0,0]
        self.goesFirst = False
        self.actionPenaltyArr = [0,0,0,0,0,0]


    def getMinRange(self):
        
        if self.kind in ['barbarian', 'knight']:
            return 0
        elif self.kind in ['rouge']:
            return 0
        elif self.kind in ['bard', 'wizard', 'ranger']:
            return 10
        else:
            return 0

    def add(self, kind, arr):
        try:
            return CLASSES[kind][arr]
        except:
            return 0
    def TurnReset(self):
        isPrepared = False

    def getNewName(self):
        self.firstName = random.choice(FIRST_NAMES)

    def getRange(self):
        if self.kind in ['barbarian', 'knight']:
            return 10
        elif self.kind in ['rouge']:
            return 5
        elif self.kind in ['bard', 'wizard', 'ranger']:
            return 30
        else:
            return 5

    def SysOut(self):
        toPrint = str(self.firstName) + ' ' + str(self.lastName) + ' '
        print( toPrint, end = '')

    def getAttack(self, oppX, oppY, AC):
        #Fighter must make 2 requirements to make an attack
        #The opponent must be within the range and minRange requirement
        #The attack roll must be greater than the opponents defense
        self.attacksTried += 1
        inRange = False
        hit = False
        if self.isComment:
            self.SysOut()
            if self.kind in ['barbarian', 'knight']:
                print('swings their greatsword to attack!')
            elif self.kind in ['ranger']:
                print('pulls back their bow\'s arrow and releases!')
            else:
                print('attempts to attack!')

        #First, check for range
        distance = math.sqrt((self.X - oppX)**2 + (self.Y - oppY)**2)
        if distance <= self.range and distance >= self.minRange:
            inRange = True
        else:
            inRange = False

        #Next, check for proper roll
        roll = random.randint(1,20) + self.attack
        if roll >= AC:
            hit = True
        else:
            hit = False

        if inRange and hit:
            return True
        else:
            return False
        

    def getDefense(self):
        return random.randint(5, 20) + self.defense

    def getDamage(self):
        damage = random.randint(1, 8) + self.damage
        self.damageDone += damage
        self.attackSuccess += 1
        #if damage < 0:
        #    damage = 0
        if self.isComment:
            self.SysOut()
            print('deals ' + str(damage) + ' points of damage!')
        return damage

    def setHealth(self, damage):
        self.health = self.health - damage
        self.deathCheck()
        if self.isDead and self.isComment:
            print('###########################################')
            print(str(self.firstName) + ' ' + str(self.lastName) + ' has Fallen! They are Defeated.')
            print('###########################################')

    def deathCheck(self):
        if self.health <= 0:
            self.isDead = True

    def getInitative(self):
        return random.randint(1, 20) + self.initative

    def reproduce(self):
        return self.mutate()

    def ConvertToPer(self):
        total = 0
        for num in self.MoveArr:
            total += num
        PerArr = []
        for num in self.MoveArr:
            PerArr.append(num / total)
        return PerArr

    def toString(self):
        print('%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&')
        self.SysOut()
        children = []
        for child in self.children:
            children.append(child.firstName)
        print('\nAttack: ' + str(self.attack) +
              '\nDamage: ' + str(self.damage) +
              '\nDefense: ' + str(self.defense) +
              '\nHealth: ' + str(self.health) +
              '\nInitative: ' + str(self.initative) +
              '\nRace: ' + str(self.race) +
              '\nClass: ' + str(self.kind) +
              '\nRange: ' + str(self.range) +
              '\nMovement: ' + str(self.movement) +
              '\nGeneration: ' + str(self.generation) +
              '\nChildren: ' + str(children) +
              '\nKills: ' + str(self.kills) +
              '\nDamage Done: ' + str(self.damageDone) +
              '\nTurn Spent Moving: ' + str(self.turnsMoving) +
              '\nTurns Spent Preparing: ' + str(self.turnsPreparing) +
              '\nTurns Spent Standing: ' + str(self.turnsStanding) +
              '\nAttacks Tried: ' + str(self.attacksTried) +
              '\nAttacks Successful: ' + str(self.attackSuccess))
        print('%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&\n')

    def mutate(self):
        """
Three Kinds of Mutations can occur


    1) A mutation that effects the Class Feats
            DONE

    2) A mutation that effects the Race Feats
            DONE
            
    3) A mutation that Changes the range zone... range - minRange
            DONE
        """
        mutant = Player(self.kind, self.race, self.lastName)
        mutant.attack = self.attack
        mutant.generation = GENERATION_NUMBER
        mutant.defense = self.defense
        mutant.health = self.health
        mutant.damage = self.damage
        mutant.initative = self.initative
        mutant.movement = self.movement
        mutant.NN = self.NN.mutate()
        
        roll = random.randint(0,100)
        mutant.getNewName()
        #Health, Attack, Damag, Defense Mutation
        if roll < 10:
            add = 3
            sub = -3
        elif roll < 40:
            add, sub = 2, -2
        else:
            add, sub = 1, -1
        roll = random.randint(1, 4)
        if roll == 1:
            mutant.attack += add
        elif roll == 2:
            mutant.defense += add
        elif roll == 3:
            mutant.damage += add    
        elif roll == 4:
            mutant.initative += add 
        else:
            mutant.health += add
            mutant.maxHealth = mutant.health
            
        roll = random.randint(1, 4)
        if roll == 1:
            mutant.attack += sub
        elif roll == 2:
            mutant.defense += sub
        elif roll == 3:
            mutant.damage += sub   
        elif roll == 4:
            mutant.initative += sub 
        else:
            mutant.health += sub

        roll = random.randint(1,2)
        add = random.randint(0, 6)

        if roll == 1:
            mutant.movement += add
            add = add * -1
            mutant.range += add
            mutant.minRange += add
        else:
            mutant.range += add
            mutant.minRange += add
            add = add * -1
            mutant.movement += add

        mutant.father = self
        self.children.append(mutant)
        
        return mutant
#############################################
"""
        End of Player Class
    Now its time for the fun stuff!
"""
#############################################

    
def getPlayers(numOfPlayers, arrOfPlay):
    for i in range(numOfPlayers):
        arrOfPlay.append(Player(random.choice(list(CLASSES.keys())), random.choice(list(RACES.keys())),random.choice(list(LAST_NAMES))))
    return arrOfPlay


def Battle(player1, player2, isComment):
    #Battle is same as fight command, just refactored to be cleaner, and adds the Neural Network
    #Runs through the figth array of 2 players and Has them fight till timer runs out or someone dies.
    if player1.isPlayable or player2.isPlayable:
        isComment = True
    player1.isComment = isComment
    player2.isComment = isComment
    player1.reset()
    player2.reset()
    if isComment:
        print('\n\n\n$$$$$$$$$$$$$ A NEW FIGHT IS STARTING $$$$$$$$$$$$$')
        player1.toString()
        player2.toString()
    init1 = player1.getInitative()
    init2 = player2.getInitative()
    fightArr = []
    if init1 > init2:
        player1.goesFirst = True
        fightArr.append(player1)
        fightArr.append(player2)
        player1.X = -25
        player1.Y = -25
        player2.X = 25
        player2.Y = 25
    else:
        player2.goesFirst = True
        fightArr.append(player2)
        fightArr.append(player1)
        player2.X = -25
        player2.Y = -25
        player1.X = 25
        player1.Y = 25
    counter = 0
    

    while counter < 300:
        for i in range(len(fightArr)):
            action = fightArr[i].getAction(fightArr[i-1].X, fightArr[i-1].Y)
            if action == 'Up':
                fightArr[i].turnsMoving += 1
                distance = fightArr[i].getMove(fightArr[i].NN.weights[-1][0], False)
                fightArr[i].Y += distance
                if isComment:
                    fightArr[i].SysOut()
                    print('Moves up ' + str(abs(distance)) + ' feet!\n')
                
            elif action =='Down':
                fightArr[i].turnsMoving += 1
                distance = fightArr[i].getMove(fightArr[i].NN.weights[-1][1], True)
                fightArr[i].Y += distance
                if isComment:
                    fightArr[i].SysOut()
                    print('Moves down ' + str(abs(distance)) + ' feet!\n')
                    
            elif action =='Left':
                fightArr[i].turnsMoving += 1
                distance = fightArr[i].getMove(fightArr[i].NN.weights[-1][2], True)
                fightArr[i].X += distance
                if isComment:
                    fightArr[i].SysOut()
                    print('Moves left ' + str(abs(distance)) + ' feet!\n')
                    
            elif action =='Right':
                fightArr[i].turnsMoving += 1
                distance = fightArr[i].getMove(fightArr[i].NN.weights[-1][3], False)
                fightArr[i].X += distance
                if isComment:
                    fightArr[i].SysOut()
                    print('Moves right ' + str(abs(distance)) + ' feet!\n')
                
            elif action =='Attack':
                fightArr[i].attacksTried += 1
                if fightArr[i].getAttack(fightArr[i-1].X, fightArr[i-1].Y, fightArr[i-1].defense):
                    fightArr[i-1].setHealth(fightArr[i].getDamage())
                    if player1.isDead:
                        player2.kills += 1
                        player2.reset()
                        return player2
                    elif player2.isDead:
                        player1.kills += 1
                        player1.reset()
                        return player1
                else:
                    if isComment:
                        print('They miss the attack!')
                    if fightArr[i-1].isPrepared and fightArr[i-1].getAttack(fightArr[i].X, fightArr[i].Y, fightArr[i].defense):
                        if isComment:
                            fightArr[i-1].SysOut()
                            print('Counter Attacks and attacks!')
                        fightArr[i].setHealth(fightArr[i-1].getDamage())
                        if player1.isDead:
                            player2.kills += 1
                            player2.reset()
                            return player2
                        elif player2.isDead:
                            player1.kills += 1
                            player1.reset()
                            return player1
                    fightArr[i-1].isPrepared = False
                    
            elif action =='Prepare':
                if isComment:
                    fightArr[i].SysOut()
                    print('Prepares themselves!')
                fightArr[i].isPrepared = True
                fightArr[i].turnsPreparing += 1
            else:
                print('uh oh')
                fightArr[i].turnsStanding += 1
                if isComment:
                    print('They just stand there silly.')

        if isComment:
            print('\n')
        counter += 1
        #End of While Loop

    
    #If neither player can kill the other, scrap both players and return a new child of the father of this fighter.
    #If neither fighter has a father then return a brand new fighter
    for fighter in fightArr:
        if fighter.father != fighter:
            return fighter.father.mutate()
        else:
            continue
        
    newPlayer = (Player(random.choice(list(CLASSES.keys())), random.choice(list(RACES.keys())),random.choice(list(LAST_NAMES))))
    return newPlayer
            
            
def listPlayers(Arr):
    for count, player in enumerate(Arr):
        print(str(count + 1) + ')', end = '' )
        player.SysOut()
        print('')
    print('\nThere are ' + str(len(Arr)) + ' players!\n')
                
def evolve(ArrOfPlay, isComment):
    newArr = []
    finalArr = []
    fightnum = 0        
    for i in range(0, len(ArrOfPlay) - 1, 2):
        j = len(ArrOfPlay)
        player = Battle(ArrOfPlay[i], ArrOfPlay[i+1], isComment)
        newArr.append(player)
        newArr.append(player.mutate())
        fightnum += 1
    newArr = shuffle(list(newArr))
    if isComment:
        print('There were ' + str(fightnum) + ' fights!')
    return list(newArr)

def shuffle(Arr):
    newArr = []
    while Arr:
        place = random.randint(0, len(Arr) - 1)
        newArr.append(Arr[place])
        Arr.remove(Arr[place])
    return newArr

def getStats(ArrOfPlay):
    """
    Gets the min, avg, and max of all stats.
    """
    totalStatsArr = [0, 0, 0, 0, 0, 0, 0, 0]
    maxStatsArr = minStatsArr = [ArrOfPlay[0].movement, ArrOfPlay[0].range, ArrOfPlay[0].minRange,
                           ArrOfPlay[0].attack, ArrOfPlay[0].defense, ArrOfPlay[0].damage,
                           ArrOfPlay[0].maxHealth, ArrOfPlay[0].initative] 
    
    for fighter in ArrOfPlay:
        fightStats = [fighter.movement, fighter.range, fighter.minRange, fighter.attack,
                      fighter.defense, fighter.damage, fighter.maxHealth, fighter.initative]

        #Tally for total to get average
        for i in range(len(fightStats)):
            totalStatsArr[i] += int(fightStats[i])

        #Check for a min
        for count, mini in enumerate(minStatsArr):
            if int(mini) > fightStats[count]:
                minStatsArr[count] = fightStats[count]
                
        #Check for a max
        for count, maxi in enumerate(maxStatsArr):
            if int(maxi) < fightStats[count]:
                maxStatsArr[count] = fightStats[count]
                
    print('Minimum Movement: ' + str(minStatsArr[0]) + '\n' +
          'Minimum Range: ' + str(minStatsArr[1]) + '\n' +
          'Minimum MinRange: ' + str(minStatsArr[2]) + '\n' +
          'Minimum Attack: ' + str(minStatsArr[3]) + '\n' +
          'Minimum Defense: ' + str(minStatsArr[4]) + '\n' +
          'Minimum Damage: ' + str(minStatsArr[5]) + '\n' +
          'Minimum Max Health: ' + str(minStatsArr[6]) + '\n' +
          'Minimum Initative: ' + str(minStatsArr[7]) + '\n')
    
    print('Average Movement: ' + str(totalStatsArr[0] / len(ArrOfPlay)) + '\n' +
          'Average Range: ' + str(totalStatsArr[1] / len(ArrOfPlay)) + '\n' +
          'Average MinRange: ' + str(totalStatsArr[2] / len(ArrOfPlay)) + '\n' +
          'Average Attack: ' + str(totalStatsArr[3] / len(ArrOfPlay)) + '\n' +
          'Average Defense: ' + str(totalStatsArr[4] / len(ArrOfPlay)) + '\n' +
          'Average Damage: ' + str(totalStatsArr[5] / len(ArrOfPlay)) + '\n' +
          'Average Max Health: ' + str(totalStatsArr[6] / len(ArrOfPlay)) + '\n' +
          'Average Initative: ' + str(totalStatsArr[7] / len(ArrOfPlay)) + '\n')

    print('Maximum Movement: ' + str(maxStatsArr[0]) + '\n' +
          'Maximum Range: ' + str(maxStatsArr[1]) + '\n' +
          'Maximum MinRange: ' + str(maxStatsArr[2]) + '\n' +
          'Maximum Attack: ' + str(maxStatsArr[3]) + '\n' +
          'Maximum Defense: ' + str(maxStatsArr[4]) + '\n' +
          'Maximum Damage: ' + str(maxStatsArr[5]) + '\n' +
          'Maximum Max Health: ' + str(maxStatsArr[6]) + '\n' +
          'Maximum Initative: ' + str(maxStatsArr[7]) + '\n')

    return #End of getStats
        
        

def EnterTournament(ArrOfPlay):
    #Everyone fights eachother until there is one victor. If odd number of people during one round, someone gets a bye.
    newArr = []
    if len(ArrOfPlay) <= 3:
        isComment = True
    else:
        isComment = False
    if len(ArrOfPlay)%2 == 0:
        start = 0
    else:
        start = 1
    for i in range(start, len(ArrOfPlay) - 1, 2):
        player = Battle(ArrOfPlay[i], ArrOfPlay[i+1], isComment)
        newArr.append(player)

    finArr = shuffle(newArr)
    if len(finArr) == 1:
        print('\n\nWe Have a Champion!\n')
        finArr[0].toString()
        return finArr
    else:
        return EnterTournament(finArr)

def createPlayer():
    try:
        print('Enter the following information for your fighter?')
        lastName = input('\nLast Name? -->')
        firstName = input('\nFirst Name? -->')
        race = input('\nRace? -->')
        kind = input('\nClass? -->')
        player = Player(kind, race, lastName)
        player.firstName = firstName
        player.range = int(input('\nMax Range? -->'))
        player.minRange = int(input('\nMin Range? -->'))
        player.attack = int(input('\nAttack Bonus? -->'))
        player.defense = int(input('\nDefense? -->'))
        player.damage = int(input('\nDamage Bonus? -->'))
        player.health = int(input('\nMax Health? -->'))
        player.speed = int(input('\nMax Move Distance? -->'))
        player.isPlayable = bool(input('\nIs the character playable? (True/False) -->'))
        return player
    except:
        print('Error entering player info. A random Player has been made to enter the Arena.')
        return Player(random.choice(list(CLASSES.keys())), random.choice(list(RACES.keys())),random.choice(list(LAST_NAMES)))

    
def main():
    global GENERATION_NUMBER
    ArrOfPlay = getPlayers(FIGHTER_NUMBER, [])
    names = {}
    isComment = False
    selectedPlayers = []
    for player in ArrOfPlay:
        names.setdefault(player.firstName.lower(), player.lastName.lower())
    while True:
        inparr = input('\nWhat do you want to do?\n-->')
        inp = inparr.split(' ')
        
        if inp[0] == 'step':
            """
            Begins the evolutionary process.
            All of the fighters battle, the ones that survive reproduce to repopulate the array.
            The reproductions have small mutations. This keeps happening until optimization.

            NEW: You are now able to play as a fighter and teach the fighter to fight properly through backPropagation!
            """
            selectedPlayers = []
            if len(ArrOfPlay)%2 == 0:
                try:
                    steps = int(inp[1])
                    try:
                        if inp[2][0].lower() == 't':
                            isComment = True
                        else:
                            isComment = False
                    except:
                        isComment = isComment
                    for i in range(steps):
                        GENERATION_NUMBER += 1
                        j = steps
                        if (i==int(j/4) or i == int(j*3 / 4)):
                            print('@', end = ' ')
                        elif (i== int(j/2)) or (i == j - 2):
                            print('#', end = ' ')
                        ArrofPlay = evolve(ArrOfPlay, isComment)
                        
                        
                except:
                    ArrOfPlay = evolve(ArrOfPlay, isComment)
            else:
                print('Make sure to make the number of players wanted an even number!')

        elif inp[0] == 'list':
            #List all players in Array of Players
            listPlayers(ArrOfPlay)

        elif inp[0] == 'stats':
            #Shows stats of all players
            getStats(ArrOfPlay)

        elif inparr.lower() in names.keys() or inparr.lower() in names.values():
            #Prints players being selected
            for player in ArrOfPlay:
                if inparr.lower() == player.firstName.lower() or inparr.lower() == player.lastName.lower():
                    player.SysOut()
                    print('was added to Selected.\n')
                    player.toString()
                    selectedPlayers.append(player)
        
        elif inp[0] in ['kill', 'delete']:
            #removes a player from the list
            #TODO: write this method
            continue

        elif inp[0] == 'new':
            #Creates a new group of players
            try:
                ArrOfPlay = getPlayers(int(inp[1]), [])
                print('New Fighters have entered the arena!')
            except:
                print('Make sure to state how many players you want to enter the Arena!')

        elif inp[0] == 'add':
            #Adds on new players to the preexisting Array of players
            try:
                ArrOfPlay = getPlayers(int(inp[1]), ArrOfPlay)
                print('New Fighters have joined the arena!')
            except:
                print('Make sure to specify how many fighters you want to join the Arena!')

        elif inp[0] == 'create':
            #Creates a new player to add to the group
            ArrOfPlay.append(createPlayer())
                

        elif inp[0] == 'sample':
            #Prints a random sample of the array of players
            ArrOfPlay[random.randint(0,len(ArrOfPlay) - 1)].toString()

        elif inp[0] == 'help':
            #prints all valid commands:
            #TODO make this more helpful
            print('Accepted Commands:\n' +
                  'step #,\nlist,\nnew #,\nadd #,\ncreate,\nsample,\ntournament,\nexit\n')
        elif inp[0][0:3] == 'tou':
            #Enters a tournament to decided who the ultimate fighter really is
            ArrOfPlay = EnterTournament(ArrOfPlay)

        elif inp[0].lower()[0:6] == 'select':
            #print selected list
            #change selection
            #change values of all players in the selected list
            selectedNames = {}
            for player in selectedPlayers:
                selectedNames.setdefault(player.firstName.lower(), player.lastName.lower())
            try:
                try:
                    #Single out selected player in selectedPlayer array
                    arrNum = int(inp[1]) - 1
                    if arrNum < 0:
                        continue
                    else:
                        selectPlay = selectedPlayer[arrNum]
                        selectedPlayers.clear()
                        selectedPlayers.append(selectPlay)

                except:
                    #change or print stat of all selected players
                    stat = str(inp[1]).lower()

                    if stat == 'clear':
                        selectedPlayers = []
                            
                        continue

                    elif stat in ['playable','isplayable']:
                            for player in selectedPlayers:
                                if player.isPlayable:
                                    player.isPlayable = False
                                    player.SysOut()
                                    print('is no longer Playable.')
                                else:
                                    player.isPlayable = True
                                    player.SysOut()
                                    print('is now a Playable Character!')

                    elif stat == 'all':
                        selectedPlayers = ArrOfPlay
                    
                    else:
                        try:
                            statNum = int(inp[2])
                            if stat in ['movement','speed']:
                                for player in selectedPlayers:
                                    player.speed = statNum

                            elif stat == 'range':
                                for player in ArrOfPlay:
                                    if player in selectedPlayers:
                                        player.range = statNum
                                    
                            elif stat == 'minrange':
                                for player in ArrOfPlay:
                                    if player in selectedPlayers:
                                        player.minRange = statNum
                                    
                            elif stat == 'attack':
                                for player in ArrOfPlay:
                                    if player in selectedPlayers:
                                        player.attack = statNum
                                    
                            elif stat == 'defense':
                                for player in ArrOfPlay:
                                    if player in selectedPlayers:
                                        player.defense = statNum
                    
                            elif stat == 'damage':
                                for player in ArrOfPlay:
                                    if player in selectedPlayers:
                                        player.damage = statNum
                                    
                            elif stat == 'health':
                                for player in ArrOfPlay:
                                    if player in selectedPlayers:
                                        player.health = statNum
                                    
                            elif stat == 'initative':
                                for player in ArrOfPlay:
                                    if player in selectedPlayers:
                                        player.initative = statNum
                                    
                                    
                        except:
                            #Print the given stats of the selecetd players
                            if stat == 'movement':
                                for player in selectedPlayers:
                                    player.SysOut()
                                    print( str(stat) + ' --> ' + str(player.movement))

                            elif stat == 'range':
                                for player in selectedPlayers:
                                    player.SysOut()
                                    print( str(stat) + ' --> ' + str(player.range))
                                    
                            elif stat == 'minrange':
                                for player in selectedPlayers:
                                    player.SysOut()
                                    print( str(stat) + ' --> ' + str(player.minRange))
                                    
                            elif stat == 'attack':
                                for player in selectedPlayers:
                                    player.SysOut()
                                    print( str(stat) + ' --> ' + str(player.attack))
                                    
                            elif stat == 'defense':
                                for player in selectedPlayers:
                                    player.SysOut()
                                    print( str(stat) + ' --> ' + str(player.defense))
                    
                            elif stat == 'damage':
                                for player in selectedPlayers:
                                    player.SysOut()
                                    print( str(stat) + ' --> ' + str(player.damage))
                                    
                            elif stat == 'health':
                                for player in selectedPlayers:
                                    player.SysOut()
                                    print( str(stat) + ' --> ' + str(player.maxHealth))
                                    
                            elif stat == 'initative':
                                for player in selectedPlayers:
                                    player.SysOut()
                                    print( str(stat) + ' --> ' + str(player.initative))
                                    
                    
            except:
                #Print selected players
                listPlayers(selectedPlayers)
            
        elif inp[0] == 'exit':
            #Closes the program
            print('Goodbye')
            break
        
        else:
            #Prints the player by the number they are in the list
            try:
                listNum = int(inp[0]) - 1
                if listNum < 0:
                    continue
                else:
                    ArrOfPlay[listNum].SysOut()
                    print('was added to Selected.\n')
                    ArrOfPlay[listNum].toString()
                    selectedPlayers.append(ArrOfPlay[listNum])
            except:
                continue
                
        
if __name__ == '__main__':        
    warnings.simplefilter("ignore")   
    main()
