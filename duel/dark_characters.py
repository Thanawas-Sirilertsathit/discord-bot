from duel.character import Character
from duel.element import ElementReaction
from duel.trait import Trait
from duel.dict_finder import dict_finder
import random

class Star_collector(Character):
    """Contain star collector information (dynamic and static info) and star collector methods"""
    def __init__(self):
        self.dictionary = dict_finder("Star collector")
        self.maxHP = int(self.dictionary["HP"])
        self.HP = int(self.dictionary["HP"])
        self.ATK = int(self.dictionary["ATK"])
        self.name = self.dictionary["Name"]
        self.DEF = int(self.dictionary["DEF"])
        self.Cooldown = int(self.dictionary["Skill cooldown"])
        self.currentcooldown = 0
        self.tempATK = 0
        self.tempDEF = 0
        self.trait = self.dictionary["Trait"]
        self.element = self.dictionary["Element"]
        self.Cost = int(self.dictionary["Cost"])
        self.elementreaction = ElementReaction()
        self.traitreaction = Trait()
        self.dead = False
        self.add_coin = False
        self.level = 1

    def receive_damage(self, damage_input, enemy):
        """Take damage from enemy"""
        dmg_taken = damage_input - self.DEF
        if dmg_taken <= 0:
            pass
        else:
            self.HP = self.HP - dmg_taken
        if self.HP <= 0:
            self.die(enemy)

    def deal_damage(self, enemy):
        """Deal damage to enemy"""
        if not isinstance(enemy,Character):
            raise ValueError("Enemy is not a character object")
        damage_element_multiplier = self.elementreaction.reaction(self.element, enemy.element)
        damage_trait_multiplier = self.traitreaction.reaction(self.trait, enemy.trait)
        total_damage = (self.tempATK + self.ATK) * damage_element_multiplier * damage_trait_multiplier
        enemy.receive_damage(total_damage, enemy)
        if enemy.isdead() == True:
            self.passive(enemy)
        self.tempATK = 0

    def passive(self, enemy):
        """Passive skill : Part of collection"""
        self.ATK += 2
        self.maxHP += 2
        self.HP += 2

    def die(self, enemy):
        """Method for this character when it dies"""
        self.dead = True

    def isdead(self):
        """Return that character is alive or dead"""
        return self.dead
    
    def cooldown(self, enemy):
        """Cooldown skill for active skill"""
        self.currentcooldown += 1
        if self.currentcooldown == self.Cooldown:
            self.active_skill(enemy)
            self.currentcooldown = 0
    
    def active_skill(self, enemy):
        """Active skill for star collector : Grant +5 max HP"""
        self.maxHP += 2
        self.HP += 2

    def take_turn(self, enemy):
        """Method for taking turn : Combine 2 methods"""
        if self.isdead() == False:
            if not isinstance(enemy,Character):
                raise ValueError("Enemy is not a character object")
            self.deal_damage(enemy) # Normal attack to enemy
            self.cooldown(enemy) # Lastly, cooldown the skill and include active skill activation

    def view_info(self):
        return f"Passive skill {self.dictionary['Passive skill name']}: {self.dictionary['Passive skill description']}\nActive skill {self.dictionary['Active skill name']}: {self.dictionary['Active skill description']}\nCooldown : {self.Cooldown}"

class Phantom(Character):
    """Contain phantom information (dynamic and static info) and phantom methods"""
    def __init__(self):
        self.dictionary = dict_finder("Phantom")
        self.maxHP = int(self.dictionary["HP"])
        self.HP = int(self.dictionary["HP"])
        self.ATK = int(self.dictionary["ATK"])
        self.name = self.dictionary["Name"]
        self.DEF = int(self.dictionary["DEF"])
        self.Cooldown = int(self.dictionary["Skill cooldown"])
        self.currentcooldown = 0
        self.tempATK = 0
        self.tempDEF = 0
        self.trait = self.dictionary["Trait"]
        self.element = self.dictionary["Element"]
        self.Cost = int(self.dictionary["Cost"])
        self.elementreaction = ElementReaction()
        self.traitreaction = Trait()
        self.dead = False
        self.active_working = False
        self.dodge_chance = [True, True, False]
        self.add_coin = False
        self.level = 1

    def receive_damage(self, damage_input, enemy):
        """Take damage from enemy"""
        if self.active_working == False:
            dmg_taken = damage_input - self.DEF
            if dmg_taken <= 0:
                pass
            else:
                self.HP = self.HP - dmg_taken
            if self.HP <= 0:
                self.die(enemy)
        else:
            dodge = random.choice(self.dodge_chance) # 2/3 chance that can dodge attack
            if dodge == True:
                pass
            else:
                dmg_taken = damage_input - self.DEF
                if dmg_taken <= 0:
                    pass
                else:
                    self.HP = self.HP - dmg_taken
                if self.HP <= 0:
                    self.die(enemy)

    def deal_damage(self, enemy):
        """Deal damage to enemy"""
        self.active_working = False
        if not isinstance(enemy,Character):
            raise ValueError("Enemy is not a character object")
        damage_element_multiplier = self.elementreaction.reaction(self.element, enemy.element)
        damage_trait_multiplier = self.traitreaction.reaction(self.trait, enemy.trait)
        total_damage = (self.tempATK + self.ATK) * damage_element_multiplier * damage_trait_multiplier
        enemy.receive_damage(total_damage, enemy)
        self.tempATK = 0

    def passive(self, enemy):
        """Passive skill : Power up"""
        if enemy.element in [self.elementreaction.electro, self.elementreaction.fire, self.elementreaction.water, self.elementreaction.ice]:
            self.tempATK += 5

    def die(self, enemy):
        """Method for this character when it dies"""
        self.dead = True

    def isdead(self):
        """Return that character is alive or dead"""
        return self.dead
    
    def cooldown(self, enemy):
        """Cooldown skill for active skill"""
        self.currentcooldown += 1
        if self.currentcooldown == self.Cooldown:
            self.active_skill(enemy)
            self.currentcooldown = 0
    
    def active_skill(self, enemy):
        """Active skill for phantom : 2/3 chance to dodge enemy attack 1 turn"""
        self.active_working = True

    def take_turn(self, enemy):
        """Method for taking turn : Combine 3 methods"""
        if self.isdead() == False:
            if not isinstance(enemy,Character):
                raise ValueError("Enemy is not a character object")
            self.passive(enemy) # Passive works first
            self.deal_damage(enemy) # Normal attack to enemy
            self.cooldown(enemy) # Lastly, cooldown the skill and include active skill activation
    
    def view_info(self):
        return f"Passive skill {self.dictionary['Passive skill name']}: {self.dictionary['Passive skill description']}\nActive skill {self.dictionary['Active skill name']}: {self.dictionary['Active skill description']}\nCooldown : {self.Cooldown}"

class Astrologist(Character):
    """Contain astrologist information (dynamic and static info) and astrologist methods"""
    def __init__(self):
        self.dictionary = dict_finder("Astrologist")
        self.maxHP = int(self.dictionary["HP"])
        self.HP = int(self.dictionary["HP"])
        self.ATK = int(self.dictionary["ATK"])
        self.name = self.dictionary["Name"]
        self.DEF = int(self.dictionary["DEF"])
        self.Cooldown = int(self.dictionary["Skill cooldown"])
        self.currentcooldown = 0
        self.tempATK = 0
        self.tempDEF = 0
        self.trait = self.dictionary["Trait"]
        self.element = self.dictionary["Element"]
        self.Cost = int(self.dictionary["Cost"])
        self.elementreaction = ElementReaction()
        self.traitreaction = Trait()
        self.dead = False
        self.passive_working = False
        self.add_coin = False
        self.level = 1

    def receive_damage(self, damage_input, enemy):
        """Take damage from enemy"""
        dmg_taken = damage_input - self.DEF
        if dmg_taken <= 0:
            pass
        else:
            self.HP = self.HP - dmg_taken
        if self.HP <= 0:
            self.die(enemy)

    def deal_damage(self, enemy):
        """Deal damage to enemy"""
        if not isinstance(enemy,Character):
            raise ValueError("Enemy is not a character object")
        damage_element_multiplier = self.elementreaction.reaction(self.element, enemy.element)
        damage_trait_multiplier = self.traitreaction.reaction(self.trait, enemy.trait)
        total_damage = (self.tempATK + self.ATK) * damage_element_multiplier * damage_trait_multiplier
        enemy.receive_damage(total_damage, enemy)
        if enemy.isdead() == True:
            self.passive_working = False
        self.tempATK = 0

    def passive(self, enemy):
        """Passive skill : Lunar Eclipse"""
        if enemy.HP <= 2:
            enemy.die(self)

    def die(self, enemy):
        """Method for this character when it dies"""
        self.dead = True

    def isdead(self):
        """Return that character is alive or dead"""
        return self.dead
    
    def cooldown(self, enemy):
        """Cooldown skill for active skill"""
        self.currentcooldown += 1
        if self.currentcooldown == self.Cooldown:
            self.active_skill(enemy)
            self.currentcooldown = 0
    
    def active_skill(self, enemy):
        """Active skill for astrologist : Grant +5 temp ATK for 1 turn"""
        self.tempATK += 5

    def take_turn(self, enemy):
        """Method for taking turn : Combine 3 methods"""
        if self.isdead() == False:
            if not isinstance(enemy,Character):
                raise ValueError("Enemy is not a character object")
            self.passive(enemy) # Passive skill activates first
            self.deal_damage(enemy) # Follow by normal attack to enemy
            self.passive(enemy) # Passive skill activates after attack enemy too
            self.cooldown(enemy) # Lastly, cooldown the skill and include active skill activation
    
    def view_info(self):
        return f"Passive skill {self.dictionary['Passive skill name']}: {self.dictionary['Passive skill description']}\nActive skill {self.dictionary['Active skill name']}: {self.dictionary['Active skill description']}\nCooldown : {self.Cooldown}"