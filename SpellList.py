import random

def DamageRoll(times, die):
    dmg = 0
    for i in range(times):
        dmg += random.randint(1,die)

    return dmg

def Swing(attacker, defender):
    if attacker.isComment:
        attacker.SysOut()
        print(' swings at their opponent!')
        
    attackRoll = random.randint(1,20) + attacker.attack + attacker.bonus
    defRoll = random.randint(1,20) + defender.defense
    if attackRoll >= defRoll:
        dmg = DamageRoll(1, 8) + attacker.damage + attacker.dmgBonus
        if attacker.isComment:
            defender.SysOut()
            print('Takes ' + str(dmg) + ' points of damage!')
        defender.setHealth(dmg)
    elif defender.isPrepared or defender.isArmored:
        if attacker.isComment:
            defender.SysOut()
            print('counters the attack!')
            defender.isPrepared = False
        Swing(defender, attacker)
    else:
        if attacker.isComment:
            attacker.SysOut()
            print('misses the swing!')
    return

def AcidSplash(attacker, defender):
    if attacker.isComment:
        attacker.SysOut()
        print('hurls a bubble of acid at their opponent!')
    roll = random.randint(1,20) + defender.initative
    if roll > 10:
        if attacker.isComment:
            defender.SysOut()
            print('dodges the bubble of acid!')
    else:
        dmg = DamageRoll(1, 6)
        if attacker.isComment:
            defender.SysOut()
            print('is struck by the bubble of acid!\nAnd takes '
                  + str(dmg) + ' points of damage!')
        defender.setHealth(dmg)
    return

def ArcaneArmor(attacker, defender):
    if attacker.isComment:
        attacker.SysOut()
        print('casts Arcane Armor!\nA Frost coat of armor covers them!')
    attacker.setHealth(-5)
    attacker.isArmored = True
    return

def ArmsOfHadar(attacker, defender):
    if attacker.isComment:
        print('Dark Tendrels appear around the area and start to grab anyone they can find!')
    roll1 = random.randint(1,20) + attacker.initative
    roll2 = random.randint(1,20) + defender.initative
    if roll1 < 10:
        dmg = DamageRoll(2,6)
        if attacker.isComment:
            attacker.SysOut()
            print('takes ' + str(dmg) + 'from the Tendrels!')
        attacker.setHealth(dmg)
    else:
        attacker.SysOut()
        print('Dodges the Tendrels!')
    if roll2 < 10:
        dmg = DamageRoll(2,6)
        if defender.isComment:
            defender.SysOut()
            print('takes ' + str(dmg) + 'from the Tendrels!')
        defender.setHealth(dmg)
    else:
        defender.SysOut()
        print('Dodges the Tendrels!')
    return

def AuraOfVitality(attacker, defender):
    if attacker.isComment:
        attacker.SysOut()
        print('casts Aura Of Vitality!\nA healing presence is in the air!')
    attacker.setHealth(-1 * (DamageRoll(2, 6)))
    return
