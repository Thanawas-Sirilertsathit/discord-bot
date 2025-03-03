class Character:
    """Abstract base class for all character types in the game."""
    
    def __init__(self, name="None", maxHP=1, ATK=1, DEF=1, Cost=1):
        self.name = name
        self.HP = maxHP
        self.maxHP = maxHP
        self.ATK = ATK
        self.DEF = DEF
        self.Cost = Cost
        self.dead = False
        self.level = 1
        self.coin_bonus = 0

    def restore_hp(self):
        """Restore the character's HP to full after ascending the floor."""
        self.HP = self.maxHP
        self.dead = False

    def take_turn(self, opponent):
        """Define the actions a character takes during a battle turn."""
        pass

    def isdead(self):
        """Check if the character's HP is 0 or less."""
        return self.HP <= 0

    def take_damage(self, damage):
        """Character takes damage, factoring in defense."""
        effective_damage = max(damage - self.DEF, 0)  # Ensure damage doesn't go below 0
        self.HP -= effective_damage
        return effective_damage

    def heal(self, amount):
        """Heal the character."""
        self.HP = min(self.HP + amount, self.max_HP)  # Ensure HP doesn't exceed max_HP
        return self.HP
    
    def attack(self, opponent):
        """Character attacks another character."""
        damage = self.ATK
        actual_damage = opponent.take_damage(damage)
        return actual_damage

    def __str__(self):
        return f"{self.name} (HP: {self.HP}, ATK: {self.ATK}, DEF: {self.DEF}, Cost: {self.Cost})"

    def view_info(self):
        return f"Abilities information"
    
    def level_up(self):
        self.level += 1
        self.maxHP += 10
        self.ATK += 5
        self.DEF += 1
        self.restore_hp()