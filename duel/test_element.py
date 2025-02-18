import unittest
from element import ElementReaction

class ElementReactionTest(unittest.TestCase):
    
    def setUp(self):
        self.elementreaction = ElementReaction()

    def test_element_reaction_normal1(self):
        """Test for legal elemental reactions part 1"""
        overload = self.elementreaction.reaction("Electro", "Fire")
        self.assertEqual(2, overload)
        noreact1 = self.elementreaction.reaction("Fire", "Electro")
        self.assertEqual(1, noreact1)

    def test_element_reaction_normal2(self):
        """Test for legal elemental reactions part 2"""
        earthquake = self.elementreaction.reaction("Earth", "Earth")
        self.assertEqual(2, earthquake)
        noreact1 = self.elementreaction.reaction("Earth", "Water")
        self.assertEqual(1, noreact1)

    def test_element_reaction_normal3(self):
        """Test for legal elemental reactions part 3"""
        frozen = self.elementreaction.reaction("Ice", "Water")
        self.assertEqual(2, frozen)
        swirl = self.elementreaction.reaction("Wind", "Fire")
        self.assertEqual(2, swirl)

    def test_element_reaction_for_wrong_attacker_input(self):
        """Test for wrong attacker input : should raise ValueError"""
        with self.assertRaises(ValueError):
            broken = self.elementreaction.reaction("E", "Fire")

    def test_element_reaction_for_wrong_receiver_input(self):
        """Test for wrong receiver input : should raise ValueError"""
        with self.assertRaises(ValueError):
            broken = self.elementreaction.reaction("Electro", "F")


if __name__ == '__main__':
    unittest.main(verbosity = 2)