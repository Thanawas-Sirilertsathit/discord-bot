from duel.character import Character
from duel.element import ElementReaction
from duel.trait import Trait
from duel.dict_finder import dict_finder

class Sakura(Character):
    """Contain sakura information (dynamic and static info) and sakura methods"""
    def __init__(self):
        self.dictionary = dict_finder("Sakura")
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
        """Passive skill : Capture (Change element to enemy element)"""
        self.element = enemy.element

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
        """Active skill for elemental mastery : Grant +4 max HP and +2 ATK"""
        self.maxHP += 4
        self.HP += 4
        self.ATK +=2

    def take_turn(self, enemy):
        """Method for taking turn : Combine 2 methods"""
        if self.isdead() == False:
            if not isinstance(enemy,Character):
                raise ValueError("Enemy is not a character object")
            self.deal_damage(enemy) # Normal attack to enemy
            self.cooldown(enemy) # Lastly, cooldown the skill and include active skill activation

    def view_info(self):
        return f"Passive skill {self.dictionary['Passive skill name']}: {self.dictionary['Passive skill description']}\nActive skill {self.dictionary['Active skill name']}: {self.dictionary['Active skill description']}\nCooldown : {self.Cooldown}"
    
class Paladin(Character):
    """Contain paladin information (dynamic and static info) and paladin methods"""
    def __init__(self):
        self.dictionary = dict_finder("Paladin")
        self.maxHP = int(self.dictionary["HP"])
        self.HP = int(self.dictionary["HP"])
        self.name = self.dictionary["Name"]
        self.ATK = int(self.dictionary["ATK"])
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
        self.passive_working = 3
        self.add_coin = False
        self.level = 1

    def receive_damage(self, damage_input, enemy):
        """Take damage from enemy"""
        dmg_taken = damage_input - self.DEF - self.tempDEF
        if dmg_taken <= 0:
            pass
        else:
            self.HP = self.HP - dmg_taken
        if self.HP <= 0:
            self.die(enemy)     

    def deal_damage(self, enemy):
        """Deal damage to enemy"""
        self.tempDEF = 0
        if not isinstance(enemy,Character):
            raise ValueError("Enemy is not a character object")
        damage_element_multiplier = self.elementreaction.reaction(self.element, enemy.element)
        damage_trait_multiplier = self.traitreaction.reaction(self.trait, enemy.trait)
        total_damage = (self.tempATK + self.ATK) * damage_element_multiplier * damage_trait_multiplier
        enemy.receive_damage(total_damage, enemy)

    def passive(self, enemy):
        """Passive skill : Holy blade"""
        self.tempATK = 0
        if self.passive_working > 0:
            self.passive_working -= 1
            self.tempATK += 3

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
        """Active skill for paladin : gain +10 DEF for 1 turn"""
        self.tempDEF += 10

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
    
class Sister(Character):
    """Contain sister information (dynamic and static info) and sister methods"""
    def __init__(self):
        self.dictionary = dict_finder("Sister")
        self.maxHP = int(self.dictionary["HP"])
        self.HP = int(self.dictionary["HP"])
        self.name = self.dictionary["Name"]
        self.ATK = int(self.dictionary["ATK"])
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
        """Passive skill : Regeneration (Heal 2 HP every turn)"""
        if self.HP < self.maxHP:
            if self.maxHP - self.HP < 2:
                self.HP = self.maxHP
            else:
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
        """Active skill for sister : Grant +10 temp ATK for 1 turn"""
        self.tempATK += 10

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
    