import random
import SpellList
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
               'Fry', 'Zach', 'Jeff', 'Geoff']

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
              'The Mildly Brave','of War','of Camelot','of The Round Table',
              'Olip','Cameniele']

FIGHTER_NUMBER = 50


class Player:

    def __init__(self, kind, race, lastName):
        self.movement = 25
        self.firstName = random.choice(FIRST_NAMES)
        self.MoveArr = list(RACES[race])
        self.kind = kind
        self.race = race
        self.range = self.getRange()
        self.minRange = self.getMinRange()
        self.lastName = lastName
        self.isDead = False
        self.isPrepared = False
        self.attack = random.randint(-4, 5) + self.add(kind, 0)
        self.defense = random.randint(-4, 5) + self.add(kind, 1)
        self.damage = random.randint(-4, 5) + self.add(kind, 2)
        self.health = random.randint(20, 28) + self.add(kind, 3)
        self.maxHealth = self.health
        self.generation = 0
        self.children = 0
        self.weapon = self.getWeapon()
        if self.health <= 0:
            self.health = 1
        self.initative = random.randint(-2, 3) + self.add(kind, 4)
        self.isComment = True
        self.isArmored = False
        self.bonus = 0
        self.dmgBonus = 0

    def reset(self):
        self.isDead = False
        self.isPrepared = False
        self.health = self.maxHealth
        self.bonus = 0
        self.dmgBonus = 0


    def getMinRange(self):
        
        if self.kind in ['barbarian', 'knight']:
            return 0
        elif self.kind in ['rouge']:
            return 0
        elif self.kind in ['bard', 'wizard', 'ranger']:
            return 10
        else:
            return 0

    def getAction(self):
        PerArr = self.ConvertToPer()
        Per = random.random()
        if self.kind in ['barbarian']:
            if Per < PerArr[0]:
                return 'rage'
            elif Per< PerArr[0] + PerArr[1]:
                return 'attack'
            else:
                return 'prepare'
        elif self.kind in ['rouge']:
            if Per < PerArr[0]:
                return 'throat'
            elif Per< PerArr[0] + PerArr[1]:
                return 'attack'
            else:
                return 'prepare'
        elif self.kind in ['bard']:
            if Per < PerArr[0]:
                return 'inspire'
            elif Per< PerArr[0] + PerArr[1]:
                return 'attack'
            else:
                return 'prepare'

        elif self.kind in ['wizard']:
            if Per < PerArr[0]:
                return 'lightning'
            elif Per< PerArr[0] + PerArr[1]:
                return 'attack'
            else:
                return 'prepare'

        elif self.kind in ['ranger']:
            if Per < PerArr[0]:
                return 'deadshot'
            elif Per< PerArr[0] + PerArr[1]:
                return 'attack'
            else:
                return 'prepare'
        else:
            return 'attack'

    def getWeapon(self):
        return
        

    def getDamageDie(self, action):
        if action in ['rage']:
            if random.randint(1,20) >= 17:
                return 12
            else:
                return 4
        elif action in ['throat']:
            if random.randint(1,20) >= 15:
                return 10
            else:
                return 4
        elif action in ['inspire', 'attack']:
            return 6
        elif self.kind in ['lighting', 'deadshot']:
            if random.randint(1,20) >= 17:
                return 15
            else:
                return 6
        else:
            return 3

    def add(self, kind, arr):
        return CLASSES[kind][arr]

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

    def getMovement(self, distance):
        return -5

    def getMove(self, distance):
        if self.isComment:
            self.SysOut()
        roll = random.random()
        PerArr = self.ConvertToPer()
        if roll < PerArr[0]:
            #Move Towards Opponent
            if self.isComment:
                print('Dashes towards the enemy!')
            if distance > self.movement:
                return int(-self.movement)
            else:
                return -distance
        elif roll < PerArr[0] + PerArr[1]:
            if self.isComment:
                print('attempts to keep the enemy at range!')
            #Move Away From Opponent But Keep Opponent Inside Range
            if self.range > distance: #Move Away
                if self.movement > self.range - distance:
                    return self.range - distance
                else:
                    return self.movement

            else: #Move Forward In Range
                if distance - self.range > self.movement:
                    return -self.movement
                else:
                    return -(distance - self.range)
        else:
            #Prepare
            if self.isComment:
                print('prepares for an attack!')
            self.isPrepared = True 
            return 0

    def getAttack(self, action):
        if self.isComment:
            self.SysOut()
            if self.kind in ['barbarian', 'knight']:
                print('swings their greatsword to attack!')
            elif self.kind in ['rouge']:
                print('attemps to slice with their dagger!')
            elif self.kind in ['bard', 'wizard']:
                print('casts a spell to attack!')
            elif self.kind in ['ranger']:
                print('pulls back their bow\'s arrow and releases!')
            else:
                print('attempts to attack!')
        if action in ['rage', 'inspire']:
            return random.randint(13, 20) + self.attack
        else:
            return random.randint(1, 20) + self.attack
    

    def getDefense(self):
        return random.randint(1, 20) + self.defense

    def getDamage(self, action):
        damage = random.randint(1, self.getDamageDie(action)) + self.damage
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
        print('\nAttack: ' + str(self.attack) +
              '\nDamage: ' + str(self.damage) +
              '\nDefense: ' + str(self.defense) +
              '\nHealth: ' + str(self.health) +
              '\nInitative: ' + str(self.initative) +
              '\nRace: ' + str(self.race) +
              '\nClass: ' + str(self.kind) +
              '\nRange: ' + str(self.range) +
              '\nMovement: ' + str(self.movement) +
              '\nMovement Array: ' + str(self.MoveArr) +
              '\nGeneration: ' + str(self.generation) +
              '\nChildren: ' + str(self.children) )
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
        self.children += 1
        mutant.attack = self.attack
        mutant.generation = self.generation + 1
        mutant.defense = self.defense
        mutant.health = self.health
        mutant.damage = self.damage
        mutant.MoveArr = self.MoveArr
        mutant.initative = self.initative
        mutant.movement = self.movement
        
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
        #elif roll == 4:
        #    mutant.initative += add 
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
        #elif roll == 4:
        #    mutant.initative += sub 
        else:
            mutant.health += sub

        roll = random.randint(0, 2)
        add = random.randint(0,4)
        mutant.MoveArr[roll] += add

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

            
        return mutant
#############################################
"""
        End of Player Class
    Now its time for the fun stuff!
"""
#############################################

    
def getPlayers(numOfPlayers, arrOfPlay):
    for i in range(len(arrOfPlay), numOfPlayers):
        arrOfPlay.append(Player(random.choice(list(CLASSES.keys())), random.choice(list(RACES.keys())),random.choice(list(LAST_NAMES))))
    return arrOfPlay

def Battle(player1, player2, isComment):
    #Initalize the fight, create fight sequence
    player1.isComment = isComment
    player2.isComment = isComment
    player1.reset()
    player2.reset()
    if isComment:
        print('\n\n\n$$$$$$$$$$$$$ A NEW FIGHT IS STARTING $$$$$$$$$$$$$')
        player1.toString()
        player2.toString()
    distance = 50
    init1 = player1.getInitative()
    init2 = player2.getInitative()
    fightArr = []
    if init1 > init2:
        fightArr.append(player1)
        fightArr.append(player2)
    else:
        fightArr.append(player2)
        fightArr.append(player1)
    counter = 0

    #Start the fight!
    """
Each Turn consists of Movement, Attack, Bonus action
Movement is to be determined by a linear equation that has distance and range as its inputs
Attack will be selected from a statistics block that is gegnerated for each player.
Bonus actions will be added to a bonus action array and will be used up as they come.
    """

    while counter < 50:
        for i in range(len(fightArr)):
            distance += fightArr[i].getMovement()
            

def Fight(player1, player2, isComment):
    player1.isComment = isComment
    player2.isComment = isComment
    player1.reset()
    player2.reset()
    if isComment:
        print('\n\n\n$$$$$$$$$$$$$ A NEW FIGHT IS STARTING $$$$$$$$$$$$$')
        player1.toString()
        player2.toString()
    distance = 50
    init1 = player1.getInitative()
    init2 = player2.getInitative()
    fightArr = []
    if init1 > init2:
        fightArr.append(player1)
        fightArr.append(player2)
    else:
        fightArr.append(player2)
        fightArr.append(player1)
    counter = 0
    

    while counter < 50:
        for i in range(len(fightArr)):
            move = fightArr[i].getMove(distance)
            distance = distance + move
            if isComment:
                print('The Fighters are now ' + str(distance) + ' feet away from each other!')
            
            if fightArr[i].range >= distance and fightArr[i].minRange <= distance:
                action1 = fightArr[i].getAction()
                action2 = 'attack'
                attackRoll = fightArr[i].getAttack(action1)
                defRoll = fightArr[i-1].getDefense()
                if fightArr[i-1].isPrepared:
                    defRoll += 5
                if attackRoll > defRoll:
                    fightArr[i-1].setHealth(fightArr[i].getDamage(action1))
                    if isComment:
                        fightArr[i-1].SysOut()
                        print('is at ' + str(fightArr[i-1].health) + ' points of Health!')
                    if fightArr[i-1].isDead:
                        fightArr[i].reset()
                        return fightArr[i]
                elif fightArr[i-1].isPrepared or fightArr[i-1].isArmored:
                    if isComment:
                        fightArr[i-1].SysOut()
                        print(' blocked and countered the incoming attack by ' + fightArr[i].firstName + ' ' + fightArr[i].lastName + '!')
                    attackRoll = fightArr[i-1].getAttack(action2)
                    defRoll = fightArr[i].getDefense()
                    fightArr[i-1].isPrepared = False
                    if attackRoll > defRoll:
                        fightArr[i].setHealth(fightArr[i-1].getDamage(action2))
                        if isComment:
                            fightArr[i].SysOut()                        
                            print('is at ' + str(fightArr[i].health) + ' points of Health!')
                        if fightArr[i].isDead:
                            fightArr[i-1].reset()
                            return fightArr[i-1]
                    else:
                        if isComment:
                            print('The counter Attack was Blocked!')
                else:
                    if isComment:
                        print('The Attack Attempt is Blocked!')

            else:
                if isComment:
                    fightArr[i].SysOut()
                if fightArr[i].range < distance:
                    if isComment:
                        print('is too far away from his opponent to attack!')
                else:
                    if isComment:
                        print('is to close to his opponent to attack!')
            if isComment:
                print('It is now ' + fightArr[i-1].firstName + ' ' + fightArr[i-1].lastName + '\'s turn!')
            
        counter += 1
    if player1.health < player2.health:
        player2.reset()
        if isComment:
            player1.SysOut()
            print('falls over from exhaustion')
            player2.SysOut()
            print('is victorious!')
        return player2
    else:
        player1.reset()
        if isComment:
            player2.SysOut()
            print('falls over from exhaustion')
            player1.SysOut()
            print('is victorious!')
        return player1

def listPlayers(Arr):
    names = {}
    for player in Arr:
        player.SysOut()
        names.setdefault(player.firstName, player.lastName)
        print('')
    print('\nThere are ' + str(len(Arr)) + ' players!\n')
    while True:
        inp = input('-->')
        if inp == 'back' or inp == 'exit':
            break
        elif inp in names.keys() or inp in names.values():
            for player in Arr:
                if inp == player.firstName or inp == player.lastName:
                    player.toString()
                
def evolve(ArrOfPlay, isComment):
    newArr = []
    finalArr = []
    fightnum = 0        
    for i in range(0, len(ArrOfPlay) - 1, 2):
        j = len(ArrOfPlay)
        player = Fight(ArrOfPlay[i], ArrOfPlay[i+1], isComment)
        player.isArmored = False
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

def EnterTournament(ArrOfPlay):
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
        player = Fight(ArrOfPlay[i], ArrOfPlay[i+1], isComment)
        newArr.append(player)

    finArr = shuffle(newArr)
    if len(finArr) == 1:
        print('\n\nWe Have a Champion!\n')
        finArr[0].toString()
        return finArr
    else:
        return EnterTournament(finArr)

def main():
    ArrOfPlay = getPlayers(FIGHTER_NUMBER, [])
    while True:
        inparr = input('\nWhat do you want to do?\n-->')
        inp = inparr.split(' ')
        if inp[0] == 'step':
            try:
                steps = int(inp[1])
                for i in range(steps):
                    j = steps
                    if (i>j/4-1 and i<j/4+1) or (i>j/2-1 and i<j/2+1) or (i>3*j/4-1 and i<3*j/4+1) or (i <= j and i >= j-1):
                        print('@', end = ' ')
                    if inp[2][0].lower() == 't':
                        ArrOfPlay = evolve(ArrOfPlay, True)
                    else:
                        ArrOfPlay = evolve(ArrOfPlay, False)
                    

            except:
                ArrOfPlay = evolve(ArrOfPlay, False)

        elif inp[0] == 'list':
            listPlayers(ArrOfPlay)

        elif inp[0] == 'new':
            try:
                if int(inp[1])%2 == 0:
                    ArrOfPlay = getPlayers(int(inp[1]), [])
                    print('New Fighters have joined the arena!')
            except:
                print('Make sure to make the number of players wanted an even number!')

        elif inp[0] == 'sample':
            ArrOfPlay[random.randint(0,len(ArrOfPlay) - 1)].toString()

        elif inp[0] == 'help':
            print('Accepted Commands:\n' +
                  'step,\nlist,\nnew,\ntournament,\nexit\n')
        elif inp[0][0:3] == 'tou':
            ArrOfPlay = EnterTournament(ArrOfPlay)
            
        elif inp[0] == 'exit':
            print('Goodbye')
            break
        
    
main()
