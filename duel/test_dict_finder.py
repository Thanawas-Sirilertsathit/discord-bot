import unittest
from dict_finder import dict_finder

class DictFinderTest(unittest.TestCase):

    def test_dict_finder(self):
        """Test for dictionary finder function in game_data.csv"""
        archer = dict_finder("Archer")
        self.assertEqual(7, int(archer["HP"]))
        self.assertEqual(2, int(archer["Cost"]))
        phantom = dict_finder("Phantom")
        self.assertEqual(5, int(phantom["ATK"]))
        self.assertEqual("Dark", phantom["Element"])
        clocktower = dict_finder("599-Clocktower")
        self.assertEqual("Building", clocktower["Trait"])
        self.assertEqual(2, int(clocktower["Skill cooldown"]))


if __name__ == '__main__':
    unittest.main(verbosity = 2)