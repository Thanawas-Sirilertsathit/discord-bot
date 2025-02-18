import unittest
from fire_characters import Archer, Speedster, Cannon_cart

class FireCharacterTest(unittest.TestCase):
    """Test cases for fire characters"""
    def setUp(self):
        self.archer1 = Archer()
        self.archer2 = Archer()
        self.archer3 = Archer()
        self.archer4 = Archer()
        self.speedster1 = Speedster()
        self.speedster2 = Speedster()
        self.speedster3 = Speedster()
        self.speedster4 = Speedster()
        self.speedster5 = Speedster()
        self.cannon_cart1 = Cannon_cart()
        self.cannon_cart2 = Cannon_cart()
        self.cannon_cart3 = Cannon_cart()

    def test_archer_vs_archer(self):
        """Test for active skill of archer and passive that should not be activated"""
        self.archer1.take_turn(self.archer2)
        self.assertEqual(3, self.archer2.HP)
        self.assertEqual(0, self.archer2.DEF)
        self.assertEqual(1, self.archer1.currentcooldown)
        self.archer1.take_turn(self.archer2)
        self.assertEqual(-1, self.archer2.HP)
        self.assertTrue(self.archer2.isdead())
        self.assertEqual(2, self.archer1.currentcooldown)
        self.archer1.take_turn(self.archer3)
        self.assertEqual(0, self.archer1.currentcooldown)
        self.assertEqual(3, self.archer1.tempATK)
        self.assertEqual(3, self.archer3.HP)
        self.archer1.take_turn(self.archer3)
        self.assertEqual(-4, self.archer3.HP) # Flame arrow activate
        self.assertTrue(self.archer3.isdead())
        self.assertEqual(0, self.archer1.tempATK)

    def test_insane_flame_and_active_skill_of_speedster(self):
        """Try simulate insane flame passive for speedster and active skill for speedster"""
        self.archer1.element = "Ice" # This gonna causes melt reaction so damage is two times
        self.speedster1.take_turn(self.archer1) # Insane flame
        self.assertEqual(-5, self.archer1.HP) 
        self.archer2.element = "Ice"
        self.speedster1.take_turn(self.archer2)
        self.assertEqual(-5, self.archer2.HP)
        self.archer3.element = "Ice"
        self.speedster1.take_turn(self.archer3)
        self.assertEqual(-5, self.archer3.HP)
        self.archer4.element = "Ice"
        self.speedster1.take_turn(self.archer4) # Furious flame + insane flame
        self.assertEqual(-11, self.archer4.HP) 

    def test_piercing_arrow(self):
        """Try passive skill of archer that gonna ignore 1 DEF of enemy"""
        self.archer1.take_turn(self.speedster1) # Piercing arrow
        self.assertEqual(0, self.speedster1.DEF)
        self.assertEqual(0, self.speedster1.HP)

    def test_cannon_cart_passive_and_active_skill(self):
        """Try passive skill of cannon cart and active skill of cannon cart"""
        self.cannon_cart1.take_turn(self.speedster1)
        self.assertEqual(0, self.speedster1.DEF) # Shattering shell
        self.assertEqual(-1, self.speedster1.HP)
        self.cannon_cart1.take_turn(self.speedster2)
        self.assertEqual(0, self.speedster2.DEF)
        self.assertEqual(-1, self.speedster2.HP) # Overload fail enemy is not electro
        self.speedster3.element = "Electro"
        self.cannon_cart1.take_turn(self.speedster3)
        self.assertEqual(0, self.speedster3.DEF)
        self.assertEqual(-1, self.speedster3.HP)
        self.speedster4.element = "Electro"
        self.cannon_cart1.take_turn(self.speedster4)
        self.assertEqual(0, self.speedster4.DEF)
        self.assertEqual(-1, self.speedster4.HP) 
        self.assertEqual(6, self.cannon_cart1.tempATK) 
        self.cannon_cart1.take_turn(self.speedster5)
        self.assertEqual(0, self.speedster5.DEF)
        self.assertEqual(-1, self.speedster5.HP) # Overload fail enemy is not electro
        self.assertEqual(0, self.cannon_cart1.tempATK)
        
    def test_dead_character_can_not_attack(self):
        """Dead character should not be able to take actions"""
        self.archer1.take_turn(self.archer2)
        self.archer1.take_turn(self.archer2)
        self.assertTrue(self.archer2.isdead())
        self.archer2.take_turn(self.archer1)
        self.assertEqual(self.archer1.maxHP, self.archer1.HP)

    def test_siege_cannon_cart(self):
        """Assume there is a building and test siege trait of cannon cart"""
        self.archer1.trait = "Building"
        self.cannon_cart1.take_turn(self.archer1)
        self.assertEqual(-5, self.archer1.HP)

    def test_error_for_non_character(self):
        """An enemy input is not a character object"""
        with self.assertRaises(ValueError):
            self.archer1.take_turn("Archer")

if __name__ == '__main__':
    unittest.main(verbosity = 2)