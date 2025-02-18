from character_list import CharacterList
from character import Character
import logging

def battle(first_player, second_player, coin1, coin2):
    """Battle arena"""
    logging.basicConfig(level = logging.INFO, filename="battle.log", filemode="w")
    p1 = first_player
    if not isinstance(p1, Character):
        raise ValueError("Input parameter is not a character object")
    p2 = second_player
    if not isinstance(p2, Character):
        raise ValueError("Input parameter is not a character object")
    turn = 1
    logging.info(f"The battle round started between {p1.name} and {p2.name}")
    while True:
        logging.info(f"Turn : {turn} before attack")
        logging.info(f"{p1.name} : Max HP = {p1.maxHP},HP = {p1.HP}, ATK = {p1.ATK}, DEF = {p1.DEF}, Element = {p1.element}")
        logging.info(f"{p2.name} : Max HP = {p2.maxHP},HP = {p2.HP}, ATK = {p2.ATK}, DEF = {p2.DEF}, Element = {p2.element}")
        p1.take_turn(p2)
        logging.info(f"Turn : {turn} after player 1 attack")
        logging.info(f"{p1.name} : Max HP = {p1.maxHP},HP = {p1.HP}, ATK = {p1.ATK}, DEF = {p1.DEF}, Element = {p1.element}")
        logging.info(f"{p2.name} : Max HP = {p2.maxHP},HP = {p2.HP}, ATK = {p2.ATK}, DEF = {p2.DEF}, Element = {p2.element}")
        if p1.isdead() == True:
            print(f"{p1.name} is dead, {p2.name} is the winner in this match")
            return p2,turn,coin1,coin2
        if p2.isdead() == True:
            print(f"{p2.name} is dead, {p1.name} is the winner in this match")
            return p1,turn,coin1,coin2
        if p1.add_coin == True:
            coin1 += 1
        p2.take_turn(p1)
        logging.info(f"Turn : {turn} after player 2 attack")
        logging.info(f"{p1.name} : Max HP = {p1.maxHP},HP = {p1.HP}, ATK = {p1.ATK}, DEF = {p1.DEF}, Element = {p1.element}")
        logging.info(f"{p2.name} : Max HP = {p2.maxHP},HP = {p2.HP}, ATK = {p2.ATK}, DEF = {p2.DEF}, Element = {p2.element}")
        if p1.isdead() == True:
            print(f"{p1.name} is dead, {p2.name} is the winner in this match")
            return p2,turn,coin1,coin2
        if p2.isdead() == True:
            print(f"{p2.name} is dead, {p1.name} is the winner in this match")
            return p1,turn,coin1,coin2
        if p2.add_coin == True:
            coin2 += 1        
        if turn >= 1000:
            print("It is a tie!")
            return None,turn,coin1,coin2
        turn += 1

    