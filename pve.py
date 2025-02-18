from duel.character_list import CharacterList
import random
import logging

class PVEGame:
    def __init__(self):
        self.characters = CharacterList()
        self.floor = 1
        self.coins = 15
        self.player = None
        self.enemies = []
        self.shop = []
        self.inventory = []

    def reset_game(self):
        """Reset the game state to the initial conditions."""
        self.floor = 1
        self.coins = 15
        self.inventory.clear()
        self.player = None
        self.enemies = []
        self.shop = []
        self.generate_enemy_lineup()
        self.refresh_shop() 

    def start_game(self):
        self.characters.generate_list()
        self.generate_enemy_lineup()
        self.refresh_shop()
        return f"You will fight the following enemies on Floor {self.floor}: {', '.join([enemy.name for enemy in self.enemies])}" 

    def generate_enemy_lineup(self):
        self.enemies = self.characters.get_random_enemy(self.floor)
    
    def battle_turn(self):
        while self.player.HP > 0 and self.enemies:
            enemy = self.enemies[0]
            self.player.take_turn(enemy)
            
            if enemy.isdead():
                self.enemies.pop(0)
                if not self.enemies:
                    self.floor += 1
                    self.coins = 15
                    self.restore_allies_hp()
                    self.restore_enemies_hp()
                    self.generate_enemy_lineup()
                    self.refresh_shop()
                    return f"All enemies defeated! Moving to Floor {self.floor}: {', '.join([enemy.name for enemy in self.enemies])}"
                return f"Enemy {enemy.name} defeated! Next enemy approaches."
            
            # Enemy's turn
            enemy.take_turn(self.player)
            if self.player.isdead():
                if not self.inventory:  # Check if the player has no more characters in inventory
                    self.floor = 1
                    self.coins = 15
                    self.refresh_shop()
                    return "You have been defeated and have no more characters in your inventory. Resetting to Floor 1."
                # Let the player choose a new character from the inventory
                return "Your character has been defeated. Choose a new character from your inventory using *choose <character_name>."
        
        self.reset_game()
        return "The result turns into draw! Your progress has been reset to floor 1."

    def restore_allies_hp(self):
        """Restore HP for all characters in the player's inventory and the player."""
        for ally in self.inventory:
            ally.restore_hp()

    def restore_enemies_hp(self):
        """Restore HP for all enemies on the floor."""
        for enemy in self.enemies:
            enemy.restore_hp()
    
    def refresh_shop(self):
        self.shop = random.sample(self.characters.chars_list, 5)
    
    def reroll_shop(self):
        if self.coins >= 1:
            self.coins -= 1
            self.refresh_shop()
            return "Shop rerolled! Here are the new characters:", self.shop
        return "Not enough coins to reroll."
    
    def buy_character(self, char_name):
        char = next((c for c in self.shop if c.name == char_name), None)
        if char:
            if self.coins >= char.Cost:
                self.coins -= char.Cost
                self.inventory.append(char)  # Add to inventory instead of just buying one
                return f"You bought {char.name}! Remaining coins: {self.coins}"
            return "Not enough coins to buy this character."
        return "Character not found in shop."

    def choose_character(self, char_name):
        """Allows the player to choose a character from their inventory."""
        char = next((c for c in self.inventory if c.name == char_name), None)
        if char:
            self.player = char  # Set the selected character as the player's active character
            self.inventory.remove(char)  # Remove from inventory
            return f"You selected {char.name}!"
        return "Character not found in inventory."

