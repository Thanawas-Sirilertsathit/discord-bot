from duel.character_list import CharacterList
import random
import logging

class PVEGame:
    def __init__(self):
        self.characters = CharacterList()
        self.players = {}  # Store individual player states
        logging.basicConfig(level=logging.INFO, filename="battle_log.log", filemode="w")

    def reset_game(self, player_id):
        """Reset the game state for a specific player."""
        self.players[player_id] = {
            'floor': 1,
            'coins': 15,
            'inventory': [],
            'player': None,
            'enemies': [],
            'shop': []
        }
        self.generate_enemy_lineup(player_id)
        self.refresh_shop(player_id)

    def start_game(self, player_id):
        self.characters.reset()
        self.characters.generate_list()
        self.reset_game(player_id)
        return f"You will fight the following enemies on Floor 1: {', '.join([enemy.name for enemy in self.players[player_id]['enemies']])}"

    def generate_enemy_lineup(self, player_id):
        self.players[player_id]['enemies'] = self.characters.get_random_enemy(self.players[player_id]['floor'])

    def battle_turn(self, player_id):
        player_data = self.players[player_id]
        turn = 1
        if not player_data['player']:
            return "Please *choose <character_name> first to put a character into battle."
        if player_data['player'].isdead():
            return "Your selected character is dead. Please select another character."
        logging.info(f"{player_data['player'].name} VS {player_data['enemies'][0].name} in floor {player_data['floor']}")
        while player_data['player'].HP > 0 and player_data['enemies'] and turn <= 1000:
            enemy = player_data['enemies'][0]
            # Player's turn
            player_data['player'].take_turn(enemy)
            logging.info(f"After player attacks in turn {turn}")
            logging.info(f"Player: {player_data['player'].name}, HP: {player_data['player'].HP}, ATK: {player_data['player'].ATK}, DEF: {player_data['player'].DEF}")
            logging.info(f"Enemy: {enemy.name}, HP: {enemy.HP}, ATK: {enemy.ATK}, DEF: {enemy.DEF}")
            # Check if the enemy is defeated
            if enemy.isdead():
                player_data['enemies'].pop(0)
                if not player_data['enemies']:
                    player_data['floor'] += 1
                    player_data['coins'] = 15
                    self.restore_allies_hp(player_id)
                    self.restore_enemies_hp(player_id)
                    self.generate_enemy_lineup(player_id)
                    self.refresh_shop(player_id)
                    return f"All enemies defeated! Moving to Floor {player_data['floor']}: {', '.join([enemy.name for enemy in player_data["enemies"]])}."
                return f"Enemy {enemy.name} defeated! Next enemy approaches."
            # Enemy's turn
            enemy.take_turn(player_data['player'])
            logging.info(f"After enemy attacks in turn {turn}")
            logging.info(f"Player: {player_data['player'].name}, HP: {player_data['player'].HP}, ATK: {player_data['player'].ATK}, DEF: {player_data['player'].DEF}")
            logging.info(f"Enemy: {enemy.name}, HP: {enemy.HP}, ATK: {enemy.ATK}, DEF: {enemy.DEF}")
            # Check if the player is defeated
            if player_data['player'].isdead():
                if not player_data['inventory']:
                    self.reset_game(player_id)
                    self.refresh_shop(player_id)
                    return "You have been defeated and have no more characters in your inventory. Resetting to Floor 1."
                return "Your character has been defeated. Choose a new character from your inventory using *choose <character_name>."
            turn += 1
        
        # Turn limit reached - force both player and enemy to 0 HP
        player_data['player'].HP = 0
        player_data['enemies'][0].HP = 0
        
        # Check if the player has more characters in inventory
        if player_data['inventory']:
            return "The battle reached the turn limit. Your character has fallen. Choose a new character from your inventory."
        
        # If no more characters, reset the game
        self.reset_game(player_id)
        return "The battle reached the turn limit. No characters left. Resetting to Floor 1."


    def restore_allies_hp(self, player_id):
        """Restore HP for all characters in the player's inventory and the player."""
        self.players[player_id]['player'].restore_hp()

    def restore_enemies_hp(self, player_id):
        """Restore HP for all enemies on the floor."""
        for enemy in self.players[player_id]['enemies']:
            enemy.restore_hp()
    
    def refresh_shop(self, player_id):
        self.characters.reset()
        self.characters.generate_list()
        self.players[player_id]['shop'] = random.sample(self.characters.chars_list, 5)
    
    def reroll_shop(self, player_id):
        if self.players[player_id]['coins'] >= 1:
            self.players[player_id]['coins'] -= 1
            self.refresh_shop(player_id)
            return f"Shop rerolled! Here are the new characters: {', '.join(c.name for c in self.players[player_id]['shop'])}. Remaining coins: {self.players[player_id]['coins']}"
        return f"Not enough coins to reroll. You have {self.players[player_id]['coins']} coins."
    
    def buy_character(self, player_id, char_name):
        player_data = self.players[player_id]
        char = next((c for c in player_data['shop'] if c.name == char_name), None)
        if not char:
            return "Character not found in shop."
        if player_data['coins'] < char.Cost:
            return "Not enough coins to buy this character."
        owned_char = next((c for c in player_data['inventory'] if c.name == char_name), None)
        if player_data['player'] and player_data['player'].name == char_name:
            owned_char = player_data['player']
        if owned_char:
            owned_char.level_up()
            player_data['coins'] -= char.Cost
            return f"{owned_char.name} leveled up to Level {owned_char.level}! Remaining coins: {player_data['coins']}"
        player_data['inventory'].append(char)
        player_data['coins'] -= char.Cost
        player_data['shop'].remove(char)
        return f"You bought {char.name}! Remaining coins: {player_data['coins']}"

    def choose_character(self, player_id, char_name):
        char = next((c for c in self.players[player_id]['inventory'] if c.name == char_name), None)
        if char:
            self.players[player_id]['player'] = char
            self.players[player_id]['inventory'].remove(char)
            return f"You selected {char.name}!"
        return "Character not found in inventory."
