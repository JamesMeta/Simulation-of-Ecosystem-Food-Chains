from typing import List, Any

class Organism:
    
    def __init__(self, organism_position: List[float], animal_id: int):

        self.organism_position = organism_position
        self.animal_id = animal_id

        self.all_known_static_resources = {}
        self.all_known_dynamic_resources = {}
        self.all_known_organisms = {}
        self.gender = None
        self.alive_status = True
    
    def die(self) -> None:

        if self.alive_status == False:
            return 

        self.alive_status = False
        print(f"Organism {self.animal_id} has died.")
        del self.all_known_organisms[self.animal_id]
    









if __name__ == "__main__":
    pass