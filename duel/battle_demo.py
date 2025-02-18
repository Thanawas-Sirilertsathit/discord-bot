from character_list import CharacterList
import logging

def play_demo():
    """Simulate battle arena"""
    logging.basicConfig(level = logging.INFO, filename="battle_demo.log", filemode="w")
    characters = CharacterList()
    char1 = input("Please enter character for player 1 : ")
    characters.generate_list()    
    p1 = characters.find(char1)
    if p1 == None:
        raise ValueError("Input name is not a character name")
    char2 = input("Please enter character for player 2 : ")
    characters.generate_list()
    p2 = characters.find(char2)
    if p2 == None:
        raise ValueError("Input name is not a character name")
    turn = 1
    while True:
        logging.info(f"Turn : {turn} before attack")
        logging.info(f"{p1.name} : Max HP = {p1.maxHP},HP = {p1.HP}, ATK = {p1.ATK}, DEF = {p1.DEF}, Element = {p1.element}")
        logging.info(f"{p2.name} : Max HP = {p2.maxHP},HP = {p2.HP}, ATK = {p2.ATK}, DEF = {p2.DEF}, Element = {p2.element}")
        p1.take_turn(p2)
        logging.info(f"Turn : {turn} after player 1 attack")
        logging.info(f"{p1.name} : Max HP = {p1.maxHP},HP = {p1.HP}, ATK = {p1.ATK}, DEF = {p1.DEF}, Element = {p1.element}")
        logging.info(f"{p2.name} : Max HP = {p2.maxHP},HP = {p2.HP}, ATK = {p2.ATK}, DEF = {p2.DEF}, Element = {p2.element}")
        if p1.isdead() == True:
            print("Player 1 is dead, Player 2 win")
            break
        if p2.isdead() == True:
            print("Player 2 is dead, Player 1 win")
            break
        p2.take_turn(p1)
        logging.info(f"Turn : {turn} after player 2 attack")
        logging.info(f"{p1.name} : Max HP = {p1.maxHP},HP = {p1.HP}, ATK = {p1.ATK}, DEF = {p1.DEF}, Element = {p1.element}")
        logging.info(f"{p2.name} : Max HP = {p2.maxHP},HP = {p2.HP}, ATK = {p2.ATK}, DEF = {p2.DEF}, Element = {p2.element}")
        if p1.isdead() == True:
            print("Player 1 is dead, Player 2 win")
            break
        if p2.isdead() == True:
            print("Player 2 is dead, Player 1 win")
            break
        if turn >= 1000:
            print("It is a tie!")
            break
        turn += 1

if __name__ == '__main__':
    play_demo()
    