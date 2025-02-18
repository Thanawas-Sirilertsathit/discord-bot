import unittest
from earth_characters import Clocktower, Swordman, Estelle_forge, Tailor

class EarthCharacterTest(unittest.TestCase):
    """Test cases for earth characters"""
    def setUp(self):
        self.clocktower1 = Clocktower()
        self.clocktower2 = Clocktower()
        self.clocktower3 = Clocktower()
        self.swordman1 = Swordman()
        self.swordman2 = Swordman()
        self.swordman3 = Swordman()
        self.estelle1 = Estelle_forge()
        self.estelle2 = Estelle_forge()
        self.estelle3 = Estelle_forge()
        self.tailor1 = Tailor()
        self.tailor2 = Tailor()
        self.tailor3 = Tailor()

    def test_clocktower_passive_and_clocktower_active_skill(self):
        """599-Clocktower passive increase damage up to 12 and active deal 30 damage to wind character"""
        self.clocktower1.take_turn(self.clocktower2)
        self.assertEqual(2, self.clocktower1.ATK) # Time flies activate
        self.clocktower2.element = "Wind"
        self.clocktower1.take_turn(self.clocktower2)
        self.assertEqual(3, self.clocktower1.ATK)
        self.assertEqual(36, self.clocktower2.HP) # Secret anti air activate
        self.clocktower2.element = "Earth"
        self.clocktower2.HP = 999
        for i in range(4, 13):
            self.clocktower1.take_turn(self.clocktower2)
            self.assertEqual(i, self.clocktower1.ATK)
        self.clocktower1.take_turn(self.clocktower2)
        self.assertEqual(12, self.clocktower1.ATK)

    def test_swordman_passive_and_swordman_active_skill(self):
        """Swordman passive increase damage against earth enemy and active gain coin after kill enemy in active skill turn"""
        self.swordman2.HP = 100
        self.swordman1.take_turn(self.swordman2) # Sharp sword activate
        self.assertEqual(86, self.swordman2.HP)
        self.swordman1.take_turn(self.swordman2)
        self.swordman3.HP = 1
        self.swordman1.take_turn(self.swordman3)
        self.assertTrue(self.swordman1.add_coin) # Golden sword success
        self.swordman1.take_turn(self.swordman2)
        self.swordman1.take_turn(self.swordman2)
        self.assertFalse(self.swordman1.add_coin) # Golden sword fail

    def test_estelle_forge_passive_and_estelle_forge_active_skill(self):
        """Estelle forge passive increase ATK and active increase DEF"""
        self.estelle2.HP = 100
        self.estelle1.take_turn(self.estelle2)
        self.assertEqual(9, self.estelle1.ATK) # Swordsmith activate
        self.estelle1.take_turn(self.estelle2)
        self.assertEqual(11, self.estelle1.ATK)
        self.estelle1.take_turn(self.estelle2)
        self.assertEqual(13, self.estelle1.ATK)
        self.assertEqual(10, self.estelle1.DEF) # Iron forge activate

    def test_tailor_passive_and_tailor_active_skill(self):
        """Tailor passive increase DEF and active increase temp DEF"""
        self.tailor1.take_turn(self.tailor2)
        self.assertEqual(4, self.tailor1.DEF) # Metallic thread activate
        self.tailor1.take_turn(self.tailor2)
        self.assertEqual(5, self.tailor1.DEF)
        self.tailor1.take_turn(self.tailor2)
        self.assertEqual(6, self.tailor1.DEF)
        self.assertEqual(3, self.tailor1.tempDEF) # Dress up activate
        self.tailor1.take_turn(self.tailor2)
        self.assertEqual(7, self.tailor1.DEF)
        self.assertEqual(3, self.tailor1.tempDEF)
        self.tailor1.take_turn(self.tailor2)
        self.assertEqual(8, self.tailor1.DEF)
        self.assertEqual(3, self.tailor1.tempDEF)
        self.tailor1.take_turn(self.tailor2)
        self.assertEqual(8, self.tailor1.DEF)
        self.assertEqual(3, self.tailor1.tempDEF)
        self.tailor1.take_turn(self.tailor2)
        self.assertEqual(8, self.tailor1.DEF)
        self.assertEqual(3, self.tailor1.tempDEF)


if __name__ == '__main__':
    unittest.main(verbosity = 2)