from typing import List, Any

class Organism:
    
    def __init__(self, organism_position: List[float], animal_id: int):
        
        self.organism_position = organism_position
        self.animal_id = animal_id

        self.all_known_resources = []
        self.all_known_organisms = []
        self.alive_status = True
    
    def die(self) -> int:
        self.alive_status = False
        return self.animal_id
    









if __name__ == "__main__":
    pass