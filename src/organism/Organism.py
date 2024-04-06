from typing import List, Any

# Great Grandparent class
# This class is the base class for all organisms in the simulation
# It contains the basic attributes that all organisms have
# It also contains the die function which is used to remove the organism from the simulation
class Organism:
    
    def __init__(self, organism_position: List[float], animal_id: int):

        self.organism_position = organism_position
        self.animal_id = animal_id

        self.all_known_static_resources = {}
        self.all_known_organisms = {}
        self.gender = None
        self.alive_status = True
        self.name = None

        # carnivore = 0, herbivore = 1
        self.dietary_classification = None
    
    def die(self, cause_of_death) -> None:

        if self.alive_status == False:
            return 

        self.alive_status = False

        # Use the utility class to count the cause of death
        self.all_known_organisms["utility"].count_deaths[cause_of_death] += 1
        del self.all_known_organisms[self.animal_id]
    









if __name__ == "__main__":
    pass