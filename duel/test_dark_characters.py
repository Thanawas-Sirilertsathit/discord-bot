import unittest
from dark_characters import Astrologist, Phantom, Star_collector

class DarkCharacterTest(unittest.TestCase):
    """Test cases for dark characters"""
    def setUp(self):
        self.phantom1 = Phantom()
        self.phantom2 = Phantom()
        self.phantom3 = Phantom()
        self.astrologist1 = Astrologist()
        self.astrologist2 = Astrologist()
        self.astrologist3 = Astrologist()
        self.star_collector1 = Star_collector()
        self.star_collector2 = Star_collector()
        self.star_collector3 = Star_collector()

    def test_astrologist_lunar_eclipse_and_active_skill(self):
        """Test for active astrologist skills"""
        self.astrologist1.take_turn(self.astrologist2)
        self.assertEqual(8, self.astrologist2.HP)
        self.astrologist1.take_turn(self.astrologist2)
        self.assertFalse(self.astrologist2.isdead())
        self.assertEqual(4, self.astrologist2.HP)
        self.astrologist3.HP = 11
        self.assertEqual(5, self.astrologist1.tempATK)
        self.astrologist1.take_turn(self.astrologist3) # Lunar eclipse and constellation power
        self.assertEqual(2, self.astrologist3.HP)
        self.assertTrue(self.astrologist3.isdead())

    def test_star_collector_passive_and_active_skill(self):
        """Star collectors buff herself after kill enemy and after skill cooldown, she will have additional max HP"""
        self.star_collector2.HP = 1
        self.star_collector1.take_turn(self.star_collector2)
        self.assertTrue(self.star_collector2.isdead()) # Part of collection passive
        self.assertEqual(12, self.star_collector1.HP)
        self.assertEqual(12, self.star_collector1.maxHP)
        self.assertEqual(7, self.star_collector1.DEF)
        self.assertEqual(9, self.star_collector1.ATK)
        self.star_collector3.HP = 999
        self.star_collector1.take_turn(self.star_collector3)
        self.assertEqual(992, self.star_collector3.HP)
        self.star_collector1.take_turn(self.star_collector3)
        self.assertEqual(17, self.star_collector1.maxHP) # Star shield
        self.assertEqual(17, self.star_collector1.HP)

    def test_phantom_powerup_and_illusion(self):
        """test for illusion master that has a dodge chance and power up that buff ATK"""
        self.phantom1.dodge_chance = [True]
        self.phantom2.element = "Ice"
        self.phantom1.take_turn(self.phantom2)
        self.assertEqual(5, self.phantom2.HP) # Power up passive
        self.phantom2.HP = 50
        self.phantom1.take_turn(self.phantom2)
        self.phantom1.take_turn(self.phantom2)
        self.phantom1.take_turn(self.phantom2) # Illusion master activate
        self.phantom2.take_turn(self.phantom1)
        self.assertEqual(13, self.phantom1.HP) # Dodge success
        self.phantom1.take_turn(self.phantom2)
        self.assertFalse(self.phantom1.active_working) # Illusion master deactivate

if __name__ == '__main__':
    unittest.main(verbosity = 2)