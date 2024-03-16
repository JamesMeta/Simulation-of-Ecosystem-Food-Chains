from typing import List, Any

class Organism:
    
    def __init__(self, species_id: int, alive_status: bool, procreate_cool_down: float, organism_position: List[float]):
        self.species_id = species_id
        self.alive_status = alive_status
        self.procreate_cool_down = procreate_cool_down
        self.organism_position = organism_position
    
    def die(self) -> int:
        self.alive_status = False
        return self.species_id
    









if __name__ == "__main__":
    pass