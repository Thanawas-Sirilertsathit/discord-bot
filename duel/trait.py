class Trait:
    """This contains trait reaction"""
    def __init__(self):
        self.none = "None"
        self.building = "Building"
        self.siege = "Siege"
        self.list_trait = [self.none, self.building, self.siege]
    
    def reaction(self, attacker, receiver):
        """ Reaction damage multiplier calculator
        :param attacker: trait of attacker
        :param receiver: trait of damage receiver
        :returns: damage multiplier for the reaction
        """
        if attacker == self.siege and receiver == self.building:
            return 2 # Destruction reaction (Siege -> Building)
        elif attacker in self.list_trait and receiver in self.list_trait:
            return 1 # No reaction
        else:
            raise ValueError("Invalid trait")