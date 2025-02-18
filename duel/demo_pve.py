import random
import logging
from character_list import CharacterList

def generate_enemy(floor):
    """Generate a random enemy with scaled stats based on floor number."""
    characters = CharacterList()
    characters.generate_list()
    enemy = random.choice(characters.chars_list)
    enemy.HP += floor * 5  # Increase HP per floor
    enemy.ATK += floor * 2  # Increase ATK per floor
    enemy.DEF += floor * 1  # Increase DEF per floor
    return enemy

def play_pve():
    """Simulate PVE battle arena."""
    logging.basicConfig(level=logging.INFO, filename="pve_battle.log", filemode="w")
    characters = CharacterList()
    characters.generate_list()
    
    char_name = input("Enter your character name: ")
    player = characters.find(char_name)
    if player is None:
        raise ValueError("Input name is not a character name")
    
    floor = 1
    while True:
        print(f"Starting Floor {floor}")
        enemy = generate_enemy(floor)
        print(f"You are fighting {enemy.name}!")
        
        turn = 1
        while True:
            logging.info(f"Turn {turn} - Before attack")
            logging.info(f"{player.name}: HP={player.HP}, ATK={player.ATK}, DEF={player.DEF}")
            logging.info(f"{enemy.name}: HP={enemy.HP}, ATK={enemy.ATK}, DEF={enemy.DEF}")
            
            player.take_turn(enemy)
            logging.info(f"Turn {turn} - After player attack")
            logging.info(f"{enemy.name}: HP={enemy.HP}")
            if enemy.isdead():
                print(f"Enemy {enemy.name} defeated! Moving to next floor.")
                break
            
            enemy.take_turn(player)
            logging.info(f"Turn {turn} - After enemy attack")
            logging.info(f"{player.name}: HP={player.HP}")
            if player.isdead():
                print("You have been defeated! Resetting progress to Floor 1.")
                floor = 1  # Reset progress
                break
            
            turn += 1
            if turn > 1000:
                print("Battle took too long! Ending in a tie.")
                break
        else:
            continue  # Continue to the next floor if player is alive
        break  # Exit the loop if the player died
        floor += 1  # Progress to next floor

if __name__ == '__main__':
    play_pve()
