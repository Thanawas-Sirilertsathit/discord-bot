import unittest
from electro_characters import Network_engineer, Nurse, Skateboarder

class ElectroCharacterTest(unittest.TestCase):
    """Test cases for electro characters"""
    def setUp(self):
        self.network1 = Network_engineer()
        self.network2 = Network_engineer()
        self.network3 = Network_engineer()
        self.nurse1 = Nurse()
        self.nurse2 = Nurse()
        self.nurse3 = Nurse()
        self.skateboarder1 = Skateboarder()
        self.skateboarder2 = Skateboarder()
        self.skateboarder3 = Skateboarder()

    def test_nurse_passive_and_nurse_active_skill(self):
        """Nurse decrease enemy ATK when join arena and heal herself with damage she deal every 2 turn"""
        self.nurse2.ATK = 10
        self.nurse1.take_turn(self.nurse2) # Anesthetic injection activate
        self.assertEqual(5, self.nurse2.ATK)
        self.nurse1.maxHP = 12
        self.nurse1.take_turn(self.nurse2)
        self.assertEqual(5, self.nurse2.ATK)
        self.assertEqual(12, self.nurse1.HP) # Bloody knife with exceed amount of healing
        self.nurse1.take_turn(self.nurse2)
        self.nurse1.maxHP = 100
        self.nurse1.take_turn(self.nurse2)
        self.assertEqual(15, self.nurse1.HP) # Bloody knife with most efficient healing

    def test_sister_passive_and_active_skills(self):
        """Skateboarder can dodge enemy attack with passive and gain 2 x ATK for active skill"""
        self.skateboarder1.dodge_chance = [True]
        self.skateboarder2.take_turn(self.skateboarder1)
        self.assertEqual(7, self.skateboarder1.HP) # High agility passive
        self.skateboarder2.take_turn(self.skateboarder1)
        self.skateboarder1.dodge_chance = [False]
        self.skateboarder2.take_turn(self.skateboarder1)
        self.assertEqual(0, self.skateboarder1.HP) # Speedrun activate

    def test_network_engineer(self):
        """Network engineer decrease enemy DEF after attack and gain coin for active skill"""
        self.network2.DEF = 5
        self.assertFalse(self.network1.add_coin)
        self.network1.take_turn(self.network2)
        self.assertEqual(13, self.network2.HP) # Microwave decrease DEF after attack
        self.assertEqual(4, self.network2.DEF) # Microwave decrease DEF
        self.network2.DEF = 0
        self.network1.take_turn(self.network2)
        self.assertFalse(self.network1.add_coin)
        self.assertEqual(6, self.network2.HP)
        self.assertEqual(0, self.network2.DEF) # Microwave can not decrease DEF if it reach 0
        self.network1.take_turn(self.network2)
        self.assertTrue(self.network1.add_coin) # Better network activate (Gain 1 coin)
        self.network1.take_turn(self.network2)
        self.assertFalse(self.network1.add_coin)

if __name__ == '__main__':
    unittest.main(verbosity = 2)