import unittest
from water_characters import Arcmage, Barista, Painter, Lawyer

class WaterCharacterTest(unittest.TestCase):
    """Test cases for water characters"""
    def setUp(self):
        self.arcmage1 = Arcmage()
        self.arcmage2 = Arcmage()
        self.arcmage3 = Arcmage()
        self.barista1 = Barista()
        self.barista2 = Barista()
        self.barista3 = Barista()
        self.painter1 = Painter()
        self.painter2 = Painter()
        self.painter3 = Painter()
        self.lawyer1 = Lawyer()
        self.lawyer2 = Lawyer()
        self.lawyer3 = Lawyer()

    def test_arcmage_passive_and_arcmage_active_skill(self):
        """Arcmage passive increase damage up to 3 times and active add more 5 max HP"""
        self.arcmage1.take_turn(self.arcmage2)
        self.assertEqual(3, self.arcmage1.ATK) # Absorbtion activate
        self.arcmage1.take_turn(self.arcmage2)
        self.assertEqual(4, self.arcmage1.ATK)
        self.arcmage1.take_turn(self.arcmage2)
        self.assertEqual(5, self.arcmage1.ATK)
        self.assertEqual(14, self.arcmage1.maxHP) # Bubble shield activate
        self.assertEqual(14, self.arcmage1.HP)
        self.arcmage1.take_turn(self.arcmage2)
        self.assertEqual(5, self.arcmage1.ATK) # Absorbtion should not go further than this

    def test_barista_passive_and_barista_active_skill(self):
        """Barista passive increase damage against ice enemy and active heal 5 HP"""
        self.barista2.element = "Ice"
        self.barista1.take_turn(self.barista2)
        self.assertEqual(5, self.barista2.HP) # Hot coffee activate
        self.barista1.take_turn(self.barista2)
        self.barista1.HP = 1
        self.barista1.take_turn(self.barista2)
        self.assertEqual(6, self.barista1.HP) # Secret recipe activate

    def test_painter_passive_and_painter_active_skill(self):
        """Painter passive decrease enemy ATK by 2 and active copy enemy HP to herself"""
        self.painter2.ATK = 5
        self.painter1.take_turn(self.painter2)
        self.assertEqual(3, self.painter2.ATK) # Color soak activate
        self.painter1.ATK = 2
        self.painter2.take_turn(self.painter1)
        self.assertEqual(1, self.painter1.ATK) # Edge case for color soak
        self.painter1.take_turn(self.painter2)
        self.assertEqual(3, self.painter2.ATK)
        self.painter1.take_turn(self.painter2)
        self.assertEqual(3, self.painter2.ATK)
        self.painter1.take_turn(self.painter2)
        self.assertEqual(3, self.painter2.ATK)
        self.painter2.HP = 100
        self.painter1.take_turn(self.painter2)
        self.assertEqual(3, self.painter2.ATK)
        self.assertEqual(100, self.painter1.HP) # Portrait drawing activate

    def test_lawyer_passive_and_lawyer_active_skill(self):
        """Lawyer passive and active transfer enemy ATK to her ATK or HP"""
        self.lawyer2.ATK = 100
        self.lawyer1.take_turn(self.lawyer2)
        self.assertEqual(4, self.lawyer1.ATK) # Peace representative activate
        self.assertEqual(99, self.lawyer2.ATK)
        self.lawyer1.take_turn(self.lawyer2)
        self.assertEqual(5, self.lawyer1.ATK) # Peace representative activate
        self.assertEqual(98, self.lawyer2.ATK)
        self.lawyer1.take_turn(self.lawyer2)
        self.assertEqual(6, self.lawyer1.ATK) # Peace representative activate
        self.assertEqual(97, self.lawyer2.ATK)
        self.lawyer1.take_turn(self.lawyer2)
        self.assertEqual(7, self.lawyer1.ATK) # Peace representative activate
        self.assertEqual(1, self.lawyer2.ATK)
        self.assertEqual(111, self.lawyer1.HP) # Emergency law activate

if __name__ == '__main__':
    unittest.main(verbosity = 2)