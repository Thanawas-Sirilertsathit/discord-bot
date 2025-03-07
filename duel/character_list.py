from duel.dark_characters import Astrologist, Phantom, Star_collector, Clockworker
from duel.earth_characters import Clocktower, Swordman, Estelle_forge, Tailor
from duel.electro_characters import Network_engineer, Nurse, Skateboarder, Mechanic
from duel.fire_characters import Archer, Speedster, Cannon_cart, Socerer
from duel.ice_characters import Actress, Glacier, Ice_worker
from duel.plant_characters import Entomologist, Florist, Huntress, Greenhouse
from duel.water_characters import Arcmage, Barista, Painter, Lawyer
from duel.wind_characters import Sakura, Sister, Paladin, Windmill
from duel.quantum_characters import Gatekeeper, Toykeeper
import random

class CharacterList:
    """Contain all characters"""
    def __init__(self):
        """Initialize data"""
        self.astrologist = Astrologist()
        self.phantom = Phantom()
        self.star_collector = Star_collector()
        self.clocktower = Clocktower()
        self.swordman = Swordman()
        self.estelle_forge = Estelle_forge()
        self.tailor = Tailor()
        self.network_engineer = Network_engineer()
        self.nurse = Nurse()
        self.skateboarder = Skateboarder()
        self.archer = Archer()
        self.cannon_cart = Cannon_cart()
        self.speedster = Speedster()
        self.actress = Actress()
        self.glacier = Glacier()
        self.ice_worker = Ice_worker()
        self.entomologist = Entomologist()
        self.florist = Florist()
        self.huntress = Huntress()
        self.arcmage = Arcmage()
        self.barista = Barista()
        self.painter = Painter()
        self.lawyer = Lawyer()
        self.sakura = Sakura()
        self.sister = Sister()
        self.paladin = Paladin()
        self.gatekeeper = Gatekeeper()
        self.mechanic = Mechanic()
        self.toykeeper = Toykeeper()
        self.clockworker = Clockworker()
        self.socerer = Socerer()
        self.greenhouse = Greenhouse()
        self.windmill = Windmill()
        self.chars_list = []

    def reset(self):
        """Reset all data"""
        self.astrologist = Astrologist()
        self.phantom = Phantom()
        self.star_collector = Star_collector()
        self.clocktower = Clocktower()
        self.swordman = Swordman()
        self.estelle_forge = Estelle_forge()
        self.tailor = Tailor()
        self.network_engineer = Network_engineer()
        self.nurse = Nurse()
        self.skateboarder = Skateboarder()
        self.archer = Archer()
        self.cannon_cart = Cannon_cart()
        self.speedster = Speedster()
        self.actress = Actress()
        self.glacier = Glacier()
        self.ice_worker = Ice_worker()
        self.entomologist = Entomologist()
        self.florist = Florist()
        self.huntress = Huntress()
        self.arcmage = Arcmage()
        self.barista = Barista()
        self.painter = Painter()
        self.lawyer = Lawyer()
        self.sakura = Sakura()
        self.sister = Sister()
        self.paladin = Paladin()
        self.gatekeeper = Gatekeeper()
        self.mechanic = Mechanic()
        self.toykeeper = Toykeeper()
        self.clockworker = Clockworker()
        self.socerer = Socerer()
        self.greenhouse = Greenhouse()
        self.windmill = Windmill()
        self.chars_list = []

    def generate_list(self):
        """Generate a list"""
        self.reset()
        self.chars_list.append(self.astrologist)
        self.chars_list.append(self.phantom)
        self.chars_list.append(self.star_collector)
        self.chars_list.append(self.clocktower)
        self.chars_list.append(self.swordman)
        self.chars_list.append(self.estelle_forge)
        self.chars_list.append(self.tailor)
        self.chars_list.append(self.network_engineer)
        self.chars_list.append(self.nurse)
        self.chars_list.append(self.skateboarder)
        self.chars_list.append(self.speedster)
        self.chars_list.append(self.archer)
        self.chars_list.append(self.cannon_cart)
        self.chars_list.append(self.actress)
        self.chars_list.append(self.glacier)
        self.chars_list.append(self.ice_worker)
        self.chars_list.append(self.entomologist)
        self.chars_list.append(self.florist)
        self.chars_list.append(self.huntress)
        self.chars_list.append(self.arcmage)
        self.chars_list.append(self.barista)
        self.chars_list.append(self.painter)
        self.chars_list.append(self.lawyer)
        self.chars_list.append(self.sakura)
        self.chars_list.append(self.sister)
        self.chars_list.append(self.paladin)
        self.chars_list.append(self.gatekeeper)
        self.chars_list.append(self.mechanic)
        self.chars_list.append(self.toykeeper)
        self.chars_list.append(self.clockworker)
        self.chars_list.append(self.socerer)
        self.chars_list.append(self.greenhouse)
        self.chars_list.append(self.windmill)

    def get_list(self):
        """Return a list contains all characters"""
        return self.chars_list
    
    def find(self, name):
        """Method for finding a wanted character"""
        for i in self.chars_list:
            if i.name == name:
                return i
        return None

    def get_random_enemy(self, floor):
        """Generate a list of enemies based on the floor level"""
        enemies = random.sample(self.chars_list, 3)
        for enemy in enemies:
            enemy.maxHP += floor * 3
            enemy.HP += floor * 3
            enemy.ATK += floor
            for i in range(floor//10):
                enemy.level_up()
        return enemies