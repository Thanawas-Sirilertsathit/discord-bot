import unittest
from ice_characters import Actress, Glacier, Ice_worker

class IceCharacterTest(unittest.TestCase):
    """Test cases for ice characters"""
    def setUp(self):
        self.actress1 = Actress()
        self.actress2 = Actress()
        self.actress3 = Actress()
        self.glacier1 = Glacier()
        self.glacier2 = Glacier()
        self.glacier3 = Glacier()
        self.ice_worker1 = Ice_worker()
        self.ice_worker2 = Ice_worker()
        self.ice_worker3 = Ice_worker()

    def test_glacier_passive_and_glacier_active_skill(self):
        """Glacier passive deal more damage against water enemy and glacier active deal 7 damage to enemy"""
        self.glacier2.element = "Water"
        self.glacier1.take_turn(self.glacier2)
        self.assertEqual(-1, self.glacier2.HP) # Frozen river activate
        self.glacier1.take_turn(self.glacier3)
        self.glacier1.take_turn(self.glacier3)
        self.assertEqual(2, self.glacier3.HP) # Ice shards activate

    def test_actress_passive_and_actress_active_skill(self):
        """Actress passive copy enemy attack and active that heal self"""
        self.actress2.ATK = 100
        self.actress1.take_turn(self.actress2)
        self.assertEqual(100, self.actress1.ATK) # Mirror world activate
        self.actress1.HP = 15
        self.actress1.take_turn(self.actress3)
        self.assertEqual(100, self.actress1.ATK)
        self.assertEqual(20, self.actress1.HP) # Curtain fall activate

    def test_ice_worker_passive_and_ice_worker_active_skill(self):
        """Ice worker passive increase max HP and ice worker active skill increase ATK to Earth enemy"""
        self.ice_worker1.take_turn(self.ice_worker2)
        self.assertEqual(8, self.ice_worker1.maxHP) # Cold career activate
        self.assertEqual(8, self.ice_worker1.HP)
        self.ice_worker1.take_turn(self.ice_worker2)
        self.ice_worker3.element = "Earth"
        self.ice_worker1.take_turn(self.ice_worker3)
        self.assertEqual(5, self.ice_worker3.HP) # Gigantic ice activate
        self.ice_worker1.take_turn(self.ice_worker3)
        self.assertEqual(-2, self.ice_worker3.HP)

if __name__ == '__main__':
    unittest.main(verbosity = 2)