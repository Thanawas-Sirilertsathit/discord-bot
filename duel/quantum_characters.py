from duel.character import Character
from duel.element import ElementReaction
from duel.trait import Trait
from duel.dict_finder import dict_finder
import random

class Gatekeeper(Character):
    """Contain gatekeeper information (dynamic and static info) and gatekeeper methods"""
    def __init__(self):
        self.dictionary = dict_finder("Gatekeeper")
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
        self.tempATK = 0

    def passive(self, enemy):
        """Passive skill : Quantum bridge"""
        self.maxHP += 1
        self.HP += 1

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
        """Active skill for gatekeeper : Grant +3 ATK"""
        self.ATK += 3

    def take_turn(self, enemy):
        """Method for taking turn : Combine 2 methods"""
        if self.isdead() == False:
            if not isinstance(enemy,Character):
                raise ValueError("Enemy is not a character object")
            self.passive(enemy) # Passive skill
            self.deal_damage(enemy) # Normal attack to enemy
            self.cooldown(enemy) # Lastly, cooldown the skill and include active skill activation

    def view_info(self):
        return f"Passive skill {self.dictionary['Passive skill name']}: {self.dictionary['Passive skill description']}\nActive skill {self.dictionary['Active skill name']}: {self.dictionary['Active skill description']}\nCooldown : {self.Cooldown}"

class Toykeeper(Character):
    """Contain toykeeper information (dynamic and static info) and toykeeper methods"""
    def __init__(self):
        self.dictionary = dict_finder("Toykeeper")
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
        self.revive = 0

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
        self.tempATK = 0

    def passive(self, enemy):
        """Passive skill : Furby friends"""
        pass

    def die(self, enemy):
        """Method for this character when it dies"""
        if self.revive < 3:
            self.name = "Furby"
            self.maxHP = 30*self.level
            self.ATK = 10 + (5*(self.level-1))
            self.DEF = 5
            self.trait = "Siege"
            self.restore_hp()
            self.revive += 1
            return
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
        """Active skill for toykeeper : Unstable energy"""
        if self.name == "Furby":
            if enemy.maxHP > 10:
                enemy.maxHP -= 10
            else:
                enemy.maxHP = 1
            if enemy.HP > 10:
                enemy.HP -= 10
            else:
                enemy.HP = 1

    def take_turn(self, enemy):
        """Method for taking turn : Combine 3 methods"""
        if self.isdead() == False:
            if not isinstance(enemy,Character):
                raise ValueError("Enemy is not a character object")
            self.passive(enemy) # Passive skill activates first
            self.deal_damage(enemy) # Follow by normal attack to enemy
            self.cooldown(enemy) # Lastly, cooldown the skill and include active skill activation

    def view_info(self):
        return f"Passive skill {self.dictionary['Passive skill name']}: {self.dictionary['Passive skill description']}\nActive skill {self.dictionary['Active skill name']}: {self.dictionary['Active skill description']}\nCooldown : {self.Cooldown}"
