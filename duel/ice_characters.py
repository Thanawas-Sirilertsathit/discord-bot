from duel.character import Character
from duel.element import ElementReaction
from duel.trait import Trait
from duel.dict_finder import dict_finder

class Glacier(Character):
    """Contain glacier information (dynamic and static info) and glacier methods"""
    def __init__(self):
        self.dictionary = dict_finder("Glacier")
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
        self.tempATK = 0

    def passive(self, enemy):
        """Passive skill : Frozen river"""
        if enemy.element == self.elementreaction.water:
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
        """Active skill for glacier : Deal 7 damage to enemy"""
        damage_element_multiplier = self.elementreaction.reaction(self.element, enemy.element)
        damage_trait_multiplier = self.traitreaction.reaction(self.trait, enemy.trait)
        total_damage = (self.tempATK + 7) * damage_element_multiplier * damage_trait_multiplier
        enemy.receive_damage(total_damage, enemy)

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
    
class Actress(Character):
    """Contain actress information (dynamic and static info) and actress methods"""
    def __init__(self):
        self.dictionary = dict_finder("Actress")
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
        self.tempATK = 0

    def passive(self, enemy):
        """Passive skill : Mirror world"""
        if self.passive_working == False:
            self.passive_working = True
            self.ATK = enemy.ATK

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
        """Active skill for actress : heal herself 5 HP"""
        heal = 5
        if self.maxHP - self.HP <= heal:
            self.HP = self.maxHP
        else:
            self.HP += heal

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
    
class Ice_worker(Character):
    """Contain ice worker information (dynamic and static info) and ice worker methods"""
    def __init__(self):
        self.dictionary = dict_finder("Ice worker")
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
        self.tempATK = 0

    def passive(self, enemy):
        """Passive skill : Cold career"""
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
        """Active skill for Ice worker : Grant +5 temp ATK for 1 turn against Earth enemy"""
        if enemy.element == self.elementreaction.earth:
            self.tempATK = 5

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
