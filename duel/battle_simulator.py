from battle_func import battle
from character_list import CharacterList
import logging

def battle_sim():
    """Simulate battle with coin system (Look like Boardgame version)"""
    characters = CharacterList()
    p1_coin = 15
    p2_coin = 15
    p1 = None
    p2 = None
    survive = None
    rounds = 1
    turns = 0
    while True:
        if p1_coin <= 0 and (p1 == None or p1.isdead() == True):
            if p2_coin<= 0 and (p2 == None or p2.isdead() != True):
                print("It is a tie for whole match!")
                break                
            else:
                print(f"Player 2 win in total {turns} turns")
                break
        if p2_coin <= 0 and (p2 == None or p2.isdead() == True):
            if p1_coin <= 0 and (p1 == None or p1.isdead() == True):
                print("It is a tie for whole match!")
                break
            else:
                print(f"Player 1 win in total {turns} turns")
                break
        if p1 == None or p1.isdead() == True:
            print(f"Now, Player 1 has {p1_coin} coins")
            char1 = input("Please enter character for Player 1 : ")
            characters.generate_list()    
            p1 = characters.find(char1)
            if p1 == None:
                raise ValueError("Input name is not a character name")
            if p1_coin - p1.Cost < 0:
                print("Your selected character is higher than your money balance.")
                p1 = None
                continue
            else:
                p1_coin -= p1.Cost
        if p2 == None or p2.isdead() == True:
            print(f"Now, Player 2 has {p2_coin} coins")
            char2 = input("Please enter character for Player 2 : ")
            characters.generate_list()    
            p2 = characters.find(char2)
            if p2 == None:
                raise ValueError("Input name is not a character name")
            if p2_coin - p2.Cost < 0:
                print("Your selected character is higher than your money balance.")
                p2 = None
                continue
            else:
                p2_coin -= p2.Cost
        if p1 != None and p1.isdead != True:
            if p2 != None and p2.isdead != True:
                if survive == None or survive == p2:
                    survive,turn,coin1,coin2 = battle(p1,p2,p1_coin,p2_coin)
                    p1_coin = coin1
                    p2_coin = coin2
                    turns += turn
                    if survive != None:
                        print(f"{survive.name} has survived for {turn} turns in {rounds} rounds")
                    else:
                        p1 = None
                        p2 = None
                    rounds += 1
                else:
                    survive,turn,coin2,coin1 = battle(p2,p1,p2_coin,p1_coin)
                    p2_coin = coin2
                    p1_coin = coin1
                    turns += turn
                    if survive != None:
                        print(f"{survive.name} has survived for {turn} turns in {rounds} rounds")
                    else:
                        p1 = None
                        p2 = None
                    rounds += 1

if __name__ == '__main__':
    battle_sim()
    