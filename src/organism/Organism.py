from typing import List, Any

class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

# Colorizing function
def colorize(text, color):
    return f"{color}{text}{colors.RESET}"

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
        print(colorize(f"Organism {self.name} #{self.animal_id} has died due to {cause_of_death}", colors.RED))
        del self.all_known_organisms[self.animal_id]
    









if __name__ == "__main__":
    pass