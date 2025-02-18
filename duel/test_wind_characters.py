import unittest
from wind_characters import Sakura, Sister, Paladin

class WindCharacterTest(unittest.TestCase):
    """Test cases for wind characters"""
    def setUp(self):
        self.sakura1 = Sakura()
        self.sakura2 = Sakura()
        self.sakura3 = Sakura()
        self.sister1 = Sister()
        self.sister2 = Sister()
        self.sister3 = Sister()
        self.paladin1 = Paladin()
        self.paladin2 = Paladin()
        self.paladin3 = Paladin()

    def test_sakura_passive_and_active_skills(self):
        """Test for changing element for sakura and buff herself"""
        self.sakura2.element = "Ice"
        self.sakura2.HP = 1
        self.sakura1.take_turn(self.sakura2)
        self.assertEqual(self.sakura2.element, self.sakura1.element) # Capture activate
        self.sakura3.HP = 90
        self.sakura1.take_turn(self.sakura3)
        self.sakura1.take_turn(self.sakura3) # Elemental mastery activate
        self.assertEqual(24, self.sakura1.HP)
        self.assertEqual(24, self.sakura1.maxHP)
        self.assertEqual(9, self.sakura1.ATK)

    def test_sister_passive_and_active_skills(self):
        """Sister regenerate 2 HP every turn and gain 10 attack when active skill activate"""
        self.sister1.maxHP = 100
        self.sister1.take_turn(self.sister2)
        self.assertEqual(17, self.sister1.HP) # Regeneration activate
        self.sister1.maxHP = 18
        self.sister1.take_turn(self.sister2)
        self.assertEqual(18, self.sister1.HP) # Excess amount of healing
        self.assertEqual(10, self.sister1.tempATK) # Blessing activate
        self.sister1.take_turn(self.sister2)
        self.assertTrue(self.sister2.isdead())

    def test_paladin_passive_and_active_skills(self):
        """Test paladin holy blade passive and storm shield"""
        self.paladin1.take_turn(self.paladin2)
        self.assertEqual(3, self.paladin1.tempATK) # Holy blade
        self.paladin1.take_turn(self.paladin2)
        self.assertEqual(3, self.paladin1.tempATK)
        self.paladin1.take_turn(self.paladin2)
        self.assertEqual(3, self.paladin1.tempATK)
        self.assertEqual(10, self.paladin1.tempDEF)
        self.paladin3.take_turn(self.paladin1)
        self.assertEqual(12, self.paladin1.HP) # Strom shield
        self.paladin1.take_turn(self.paladin2)
        self.assertEqual(0, self.paladin1.tempATK) # 3 turns passed Holy blade deactivate
        self.assertEqual(0, self.paladin1.tempDEF) # 1 turn passed Strom shield deactivate

if __name__ == '__main__':
    unittest.main(verbosity = 2)