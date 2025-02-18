class ElementReaction:
    """This contains elements and then delegates work to subclasses of each element"""
    def __init__(self):
        self.earth = "Earth"
        self.water = "Water"
        self.electro = "Electro"
        self.fire = "Fire"
        self.plant = "Plant"
        self.dark = "Dark"
        self.wind = "Wind"
        self.ice = "Ice"
        self.EARTH = Earth()
        self.WATER = Water()
        self.ELECTRO = Electro()
        self.FIRE = Fire()
        self.PLANT = Plant()
        self.DARK = Dark()
        self.WIND = Wind()
        self.ICE = Ice()
    
    def reaction(self, attacker, receiver):
        """ Reaction damage multiplier calculator
        :param attacker: element of attacker
        :param receiver: element of damage receiver
        :returns: damage multiplier for the reaction
        """
        if attacker == self.earth:
            return self.EARTH.reaction(receiver)
        elif attacker == self.fire:
            return self.FIRE.reaction(receiver)
        elif attacker == self.water:
            return self.WATER.reaction(receiver)
        elif attacker == self.plant:
            return self.PLANT.reaction(receiver)
        elif attacker == self.ice:
            return self.ICE.reaction(receiver)
        elif attacker == self.electro:
            return self.ELECTRO.reaction(receiver)
        elif attacker == self.dark:
            return self.DARK.reaction(receiver)
        elif attacker == self.wind:
            return self.WIND.reaction(receiver)
        else:
            raise ValueError(f"There is no element {attacker}")
        
class Element:
    """Abstract class"""
    def __init__(self):
        self.earth = "Earth"
        self.water = "Water"
        self.electro = "Electro"
        self.fire = "Fire"
        self.plant = "Plant"
        self.dark = "Dark"
        self.wind = "Wind"
        self.ice = "Ice"
        self.element_list = ["Earth", "Water", "Electro", "Fire", "Plant", "Dark", "Wind", "Ice"]
    def reaction(self):
        pass

class Earth(Element):
    """Contain earth elemental reactions"""
    def __init__(self):
        super().__init__()
    
    def reaction(self, receiver):
        """Output the damage multiplier of the reaction"""
        if receiver == self.earth: # Earthquake reaction (Earth -> Earth)
            return 2
        elif receiver == self.electro: # Insult reaction (Earth -> Electro)
            return 2
        elif receiver in self.element_list:
            return 1
        else:
            raise ValueError(f"There is no element {receiver}")

class Water(Element):
    """Contain water elemental reactions"""
    def __init__(self):
        super().__init__()
    
    def reaction(self, receiver):
        """Output the damage multiplier of the reaction"""
        if receiver == self.fire: # Extinguish reaction (Water -> Fire)
            return 2
        elif receiver == self.earth: # Dissolve reaction (Water -> Earth)
            return 2
        elif receiver in self.element_list:
            return 1
        else:
            raise ValueError(f"There is no element {receiver}")

class Electro(Element):
    """Contain electro elemental reactions"""
    def __init__(self):
        super().__init__()
    
    def reaction(self, receiver):
        """Output the damage multiplier of the reaction"""
        if receiver == self.fire: # Overload reaction (Electro -> Fire)
            return 2
        elif receiver == self.ice: # Superconduct reaction (Electro -> Ice)
            return 2
        elif receiver in self.element_list:
            return 1
        else:
            raise ValueError(f"There is no element {receiver}")

class Fire(Element):
    """Contain fire elemental reactions"""
    def __init__(self):
        super().__init__()
    
    def reaction(self, receiver):
        """Output the damage multiplier of the reaction"""
        if receiver == self.earth: # Earth shackle reaction (Fire -> Earth)
            return 2
        elif receiver == self.ice: # Melt reaction (Fire -> Ice)
            return 2
        elif receiver == self.plant: # Burn reaction (Fire -> Plant)
            return 2
        elif receiver == self.dark: # Light up reaction (Fire -> Dark)
            return 2
        elif receiver in self.element_list:
            return 1
        else:
            raise ValueError(f"There is no element {receiver}")

class Plant(Element):
    """Contain plant elemental reactions"""
    def __init__(self):
        super().__init__()
    
    def reaction(self, receiver):
        """Output the damage multiplier of the reaction"""
        if receiver == self.electro: # Aggravate reaction (Plant -> Electro)
            return 2
        elif receiver == self.water: # Bloom reaction (Plant -> Water)
            return 2
        elif receiver in self.element_list:
            return 1
        else:
            raise ValueError(f"There is no element {receiver}")

class Dark(Element):
    """Contain dark elemental reactions"""
    def __init__(self):
        super().__init__()
    
    def reaction(self, receiver):
        """Output the damage multiplier of the reaction"""
        if receiver == self.plant: # Wither reaction (Dark -> Plant)
            return 2
        elif receiver == self.wind: # Dark wave reaction (Dark -> Wind)
            return 2
        elif receiver in self.element_list:
            return 1
        else:
            raise ValueError(f"There is no element {receiver}")

class Wind(Element):
    """Contain wind elemental reactions"""
    def __init__(self):
        super().__init__()
    
    def reaction(self, receiver):
        """Output the damage multiplier of the reaction"""
        if receiver == self.plant: # Gust reaction (Wind -> Plant)
            return 2
        elif receiver == self.fire: # Swirl reaction (Wind -> Fire)
            return 2
        elif receiver in self.element_list:
            return 1
        else:
            raise ValueError(f"There is no element {receiver}")

class Ice(Element):
    """Contain ice elemental reactions"""
    def __init__(self):
        super().__init__()
    
    def reaction(self, receiver):
        """Output the damage multiplier of the reaction"""
        if receiver == self.water: # Frozen reaction (Ice -> Water)
            return 2
        elif receiver == self.dark: # Aurora reaction (Ice -> Dark)
            return 2
        elif receiver in self.element_list:
            return 1
        else:
            raise ValueError(f"There is no element {receiver}")
