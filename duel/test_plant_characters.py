import unittest
from plant_characters import Entomologist, Florist, Huntress

class PlantCharacterTest(unittest.TestCase):
    """Test cases for plant characters"""
    def setUp(self):
        self.entomologist1 = Entomologist()
        self.entomologist2 = Entomologist()
        self.entomologist3 = Entomologist()
        self.florist1 = Florist()
        self.florist2 = Florist()
        self.florist3 = Florist()
        self.huntress1 = Huntress()
        self.huntress2 = Huntress()
        self.huntress3 = Huntress()

    def test_entomologist_passive_and_entomologist_active_skill(self):
        """Entomologist attack plant characters with 3 x ATK and active skill turn enemy to 1 HP"""
        self.entomologist2.HP = 100
        self.entomologist1.take_turn(self.entomologist2)
        self.assertEqual(92, self.entomologist2.HP) # Herbivore activates
        self.entomologist1.take_turn(self.entomologist2)
        self.entomologist1.take_turn(self.entomologist2)
        self.entomologist1.take_turn(self.entomologist2)
        self.entomologist1.take_turn(self.entomologist2)
        self.assertEqual(1, self.entomologist2.HP) # Scorpion poison activates

    def test_florist_passive_and_florist_active_skill(self):
        """Florist can attack water enemy with additional damage and deal damage when active skill cooldown is finished"""
        self.florist2.element = "Water"
        self.florist1.take_turn(self.florist2)
        self.assertEqual(-2, self.florist2.HP) # Petal drop activate
        self.florist3.HP = 100
        self.florist1.take_turn(self.florist3)
        self.assertEqual(98, self.florist3.HP)
        self.florist1.take_turn(self.florist3)
        self.assertEqual(92, self.florist3.HP) # Full decorated vase activate

    def test_huntress_passive_and_huntress_active_skill(self):
        """Huntress ignores enemy DEF and deal additional damage for 1 turn"""
        self.huntress2.DEF = 100
        self.huntress1.take_turn(self.huntress2)
        self.assertEqual(0, self.huntress2.DEF) # Poison activate
        self.assertEqual(7, self.huntress2.HP)
        self.huntress1.take_turn(self.huntress2)
        self.assertEqual(5, self.huntress2.HP)
        self.huntress2.element = "Electro"
        self.huntress1.take_turn(self.huntress2)
        self.assertEqual(1, self.huntress2.HP)
        self.assertEqual(5, self.huntress1.tempATK) # Poison arrow activate
        self.huntress1.take_turn(self.huntress2)
        self.assertEqual(-13, self.huntress2.HP)
        self.assertEqual(0, self.huntress2.DEF)
        self.huntress1.take_turn(self.huntress3)
        self.assertEqual(0, self.huntress3.DEF) # Poison activate again

if __name__ == '__main__':
    unittest.main(verbosity = 2)