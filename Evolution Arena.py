import random
#   CLASS : [Attack, Defense, Damage, Health, initative]
CLASSES = {'barbarian': [1, 1, 1, 1, 1], 'ranger': [2, 0, 2, 0, 1], 'rouge':[3, -1, 3, -1, 3], 'bard':[0, 2, -1, 3, 0], 'wizard': [1, -1, 2, 2, 0]}
#   RACE : [Move Towards, Move Away, Prepare]
RACES = {'human': [2,2,2], 'elf':[1,2,1], 'giant':[2,1,2],
         'dwarf':[1,2,2], 'dragonborn': [2,2,1], 'gnome': [1,1,2],
         'orc':[2,1,1]}

FIRST_NAMES = ['Eilaga','Prukain','Krusk','Devis','Jozan','Gimble','Eberk','Vadani','Tordek',
               'Ember','Grog','Percy','Arthur','Alhandra','Soveliss','Lidda','Hennet','Mialee',
               'Ragdar','Dian','Nese','Mae','Valhein','Dol','Earl','Cedria','Azulei','Yun','Cybel',
               'Donnie', 'Parker', 'Motley', 'Edward', 'Brick','Cumulous','Jacob','Bailey','Brock',
               'Caleb','Cathrine','Alexander','Alexandra','Anthony','Blaze','Gordon','Henry','Flexo',
               'Fry']

LAST_NAMES = ['Woodsoul','Carter','Licktenstein','Barton','Grimm','Ozul','Arkalis','Armanci','Baldric',
              'Ballard','Bilger','Blackstrand','Brightwater','Carnavon','Coldshore','Coyle','Cresthill',
              'Cuttlescar','Daargen','Drumwind','Dunhall','Fletcher','Fryft','Goldrudder','Lamoth',
              'Van Gandt','Van Hyden','Welfer','Strong', 'Stark', 'Darko', 'Kimera', 'The Short',
              'Coupled', 'Parker', 'Van Halen', 'Crue', 'Van Helsing']

FIGHTER_NUMBER = 50


class Player:

    def __init__(self, kind, race, lastName):
        self.movement = 25
        self.firstName = random.choice(FIRST_NAMES)
        self.MoveArr = list(RACES[race])
        self.kind = kind
        self.race = race
        self.damDie = self.getDamageDie()
        self.range = self.getRange()
        self.minRange = self.getMinRange()
        self.lastName = lastName
        self.isDead = False
        self.isPrepared = False
        self.attack = random.randint(-4, 5) + self.add(kind, 0)
        self.defense = random.randint(-4, 5) + self.add(kind, 1)
        self.damage = random.randint(-4, 5) + self.add(kind, 2)
        self.health = random.randint(25, 32) + self.add(kind, 3)
        self.maxHealth = self.health
        self.generation = 0
        self.children = 0
        self.weapon = self.getWeapon()
        if self.health <= 0:
            self.health = 1
        self.initative = random.randint(-2, 3) + self.add(kind, 4)
        self.Last_Fight = []

    def reset(self):
        self.isDead = False
        self.isPrepared = False
        self.health = self.maxHealth


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
        return

    def getWeapon(self):
        return
        

    def getDamageDie(self):
        if self.kind in ['barbarian', 'knight']:
            return 8
        elif self.kind in ['rouge']:
            return 10
        elif self.kind in ['bard', 'wizard', 'ranger']:
            return 6
        else:
            return 8
        

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

    def getMove(self, distance):
        self.SysOut()
        roll = random.random()
        PerArr = self.ConvertToPer()
        if roll < PerArr[0]:
            #Move Towards Opponent
            print('Dashes towards the enemy!')
            if distance > self.movement:
                return int(-self.movement)
            else:
                return -distance
        elif roll < PerArr[0] + PerArr[1]:
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
            print('prepares for an attack!')
            self.isPrepared = True 
            return 0

    def getAttack(self):
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
        return random.randint(1, 20) + self.attack
    

    def getDefense(self):
        return random.randint(1, 20) + self.defense

    def getDamage(self):
        damage = random.randint(1, self.damDie) + self.damage
        self.SysOut()
        print('deals ' + str(damage) + ' points of damage!')
        return damage

    def setHealth(self, damage):
        self.health = self.health - damage
        self.deathCheck()
        if self.isDead:
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
        roll = random.randint(1, 5)
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
            
        roll = random.randint(1, 5)
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

"""
        End of Player Class
    Now its time for the fun stuff!
"""
    

    
def getPlayers(numOfPlayers, arrOfPlay):
    for i in range(len(arrOfPlay), numOfPlayers):
        arrOfPlay.append(Player(random.choice(list(CLASSES.keys())), random.choice(list(RACES.keys())),random.choice(list(LAST_NAMES))))
    return arrOfPlay

def Fight(player1, player2):
    print('\n\n\n$$$$$$$$$$$$$ A NEW FIGHT IS STARTING $$$$$$$$$$$$$')
    player1.reset()
    player2.reset()
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
            print('The Fighters are now ' + str(distance) + ' feet away from each other!')
            
            if fightArr[i].range >= distance and fightArr[i].minRange <= distance:
                attackRoll = fightArr[i].getAttack()
                defRoll = fightArr[i-1].getDefense()
                if fightArr[i-1].isPrepared:
                    defRoll += 5
                if attackRoll > defRoll:
                    fightArr[i-1].setHealth(fightArr[i].getDamage())
                    fightArr[i-1].SysOut()
                    print('is at ' + str(fightArr[i-1].health) + ' points of Health!')
                    if fightArr[i-1].isDead:
                        fightArr[i].reset()
                        return fightArr[i]
                elif fightArr[i-1].isPrepared:
                    fightArr[i-1].SysOut()
                    print(' blocked and countered the incoming attack by ' + fightArr[i].firstName + ' ' + fightArr[i].lastName + '!')
                    attackRoll = fightArr[i-1].getAttack()
                    defRoll = fightArr[i].getDefense()
                    fightArr[i-1].isPrepared = False
                    if attackRoll > defRoll:
                        fightArr[i].setHealth(fightArr[i-1].getDamage())
                        fightArr[i].SysOut()
                        
                        print('is at ' + str(fightArr[i].health) + ' points of Health!')
                        if fightArr[i].isDead:
                            fightArr[i-1].reset()
                            return fightArr[i-1]
                    else:
                        print('The counter Attack was Blocked!')
                else:
                    print('The Attack Attempt is Blocked!')

            else:
                fightArr[i].SysOut()
                if fightArr[i].range < distance:
                    print('is too far away from his opponent to attack!')
                else:
                    print('is to close to his opponent to attack!')

            print('It is now ' + fightArr[i-1].firstName + ' ' + fightArr[i-1].lastName + '\'s turn!')
            
        counter += 1
    if player1.health < player2.health:
        player2.reset()
        player1.SysOut()
        print('falls over from exhaustion')
        player2.SysOut()
        print('is victorious!')
        return player2
    else:
        player1.reset()
        player2.SysOut()
        print('falls over from exhaustion')
        player1.SysOut()
        print('is victorious!')
        return player1

def main():
    ArrOfPlay = getPlayers(FIGHTER_NUMBER, [])
    while True:
        inparr = input('What do you want to do?\n-->')
        inp = inparr.split(' ')
        if inp[0] == 'step':
            try:
                steps = int(inp[1])
            ArrOfPlay = evolve(ArrOfPlay, True)

        elif inp[0] == 'list':
            listPlayers(ArrOfPlay)

        elif inp[0] == 'help':
            print('Accepted Commands:\n' +
                  'step,\nlist,\n exit\n')
        elif inp == 'exit':
            print('Goodbye')
            break

def listPlayers(Arr):
    names = {}
    for player in Arr:
        player.SysOut()
        names.setdefault(player.firstName, player.lastName)
        print('')
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
        player = Fight(ArrOfPlay[i], ArrOfPlay[i+1])
        newArr.append(player)
        newArr.append(player.mutate())
        fightnum += 1
    newArr = shuffle(list(newArr))
    print('There were ' + str(fightnum) + ' fights!')
    return list(newArr)

def shuffle(Arr):
    newArr = []
    while Arr:
        place = random.randint(0, len(Arr) - 1)
        newArr.append(Arr[place])
        Arr.remove(Arr[place])
    return newArr
        
    
main()
