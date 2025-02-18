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
        logging.basicConfig(level=logging.INFO, filename="battle_log.log", filemode="w")

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
        turn = 1
        if not self.player:
            return "Please *choose <character_name> first to put character into battle."
        logging.info(f"{self.player.name} VS {self.enemies[0].name} in floor {self.floor}")
        while self.player.HP > 0 and self.enemies and turn <= 1000:
            enemy = self.enemies[0]
            self.player.take_turn(enemy)
            logging.info(f"==================================")
            logging.info(f"After player attacks in turn {turn}")
            logging.info(f"Player: {self.player.name}, HP: {self.player.HP}, ATK: {self.player.ATK}, DEF: {self.player.DEF}")
            logging.info(f"Enemy: {enemy.name}, HP: {enemy.HP}, ATK: {enemy.ATK}, DEF: {enemy.DEF}")
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
            logging.info(f"==================================")
            logging.info(f"After enemy attacks in turn {turn}")
            logging.info(f"Player: {self.player.name}, HP: {self.player.HP}, ATK: {self.player.ATK}, DEF: {self.player.DEF}")
            logging.info(f"Enemy: {enemy.name}, HP: {enemy.HP}, ATK: {enemy.ATK}, DEF: {enemy.DEF}")
            
            if self.player.isdead():
                if not self.inventory:  # Check if the player has no more characters in inventory
                    self.reset_game()
                    self.refresh_shop()
                    return "You have been defeated and have no more characters in your inventory. Resetting to Floor 1."
                # Let the player choose a new character from the inventory
                return "Your character has been defeated. Choose a new character from your inventory using *choose <character_name>."
            
            # Draw condition: both the player and all enemies are dead
            if self.player.isdead() and not self.enemies:
                if len(self.inventory) == 0:
                    self.reset_game()
                    return "Both you and the enemies have been defeated. It's a draw! Resetting to Floor 1."
                elif len(self.enemies) == 1:
                    self.floor += 1
                    self.coins = 15
                    self.restore_allies_hp()
                    self.restore_enemies_hp()
                    self.generate_enemy_lineup()
                    self.refresh_shop()
                    return f"The enemy was the last one standing! Moving to Floor {self.floor}."
            turn += 1
        if self.player.isdead() and self.enemies:
            if not self.inventory:
                self.reset_game()
                self.refresh_shop()
                return "You have been defeated and have no more characters in your inventory. Resetting to Floor 1."
            return "Your character has been defeated. Choose a new character from your inventory using *choose <character_name>."
        if self.player.isdead() and not self.enemies:
            if len(self.inventory) == 0:
                self.reset_game()
                return "Both you and the enemies have been defeated. It's a draw! Resetting to Floor 1."
        elif len(self.enemies) == 1:
            self.floor += 1
            self.coins = 15
            self.restore_allies_hp()
            self.restore_enemies_hp()
            self.generate_enemy_lineup()
            self.refresh_shop()
            return f"The enemy was the last one standing! Moving to Floor {self.floor}."
        self.reset_game()
        return "The result turns into draw! Your progress has been reset to floor 1."


    def restore_allies_hp(self):
        """Restore HP for all characters in the player's inventory and the player."""
        self.player.restore_hp()

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
            return f"Shop rerolled! Here are the new characters: {', '.join(c.name for c in self.shop)}. Remaining coins: {self.coins}"
        return f"Not enough coins to reroll. You have {self.coins} coins."
    
    def buy_character(self, char_name):
        """Buy a character from the shop. If the character is already owned, level it up instead."""
        char = next((c for c in self.shop if c.name == char_name), None)
        if not char:
            return "Character not found in shop."
        if self.coins < char.Cost:
            return "Not enough coins to buy this character."
        # Check if player already owns this character (either in inventory or as selected)
        owned_char = next((c for c in self.inventory if c.name == char_name), None)
        if self.player and self.player.name == char_name:
            owned_char = self.player  # If the player is using the character, level it up instead
        if owned_char:
            owned_char.level_up()
            self.coins -= char.Cost
            return f"{owned_char.name} leveled up to Level {owned_char.level}! Remaining coins: {self.coins}"
        # If not owned, add to inventory
        self.inventory.append(char)
        self.coins -= char.Cost
        self.shop.remove(char)
        return f"You bought {char.name}! Remaining coins: {self.coins}"

    def choose_character(self, char_name):
        """Allows the player to choose a character from their inventory."""
        char = next((c for c in self.inventory if c.name == char_name), None)
        if char:
            self.player = char
            self.inventory.remove(char)  # Remove from inventory
            return f"You selected {char.name}!"
        return "Character not found in inventory."

