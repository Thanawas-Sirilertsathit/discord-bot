import unittest
from trait import Trait

class TraitReactionTest(unittest.TestCase):
    
    def setUp(self):
        self.trait = Trait()

    def test_element_reaction_normal1(self):
        """Test for legal trait reactions part 1"""
        destruct = self.trait.reaction("Siege", "Building")
        self.assertEqual(2, destruct)
        noreact1 = self.trait.reaction("None", "Siege")
        self.assertEqual(1, noreact1)
        noreact2 = self.trait.reaction("Building", "Siege")
        self.assertEqual(1, noreact2)

    def test_trait_reaction_for_wrong_attacker_input(self):
        """Test for wrong attacker input : should raise ValueError"""
        with self.assertRaises(ValueError):
            broken = self.trait.reaction("P", "None")

    def test_trait_reaction_for_wrong_receiver_input(self):
        """Test for wrong receiver input : should raise ValueError"""
        with self.assertRaises(ValueError):
            broken = self.trait.reaction("None", "F")


if __name__ == '__main__':
    unittest.main(verbosity = 2)