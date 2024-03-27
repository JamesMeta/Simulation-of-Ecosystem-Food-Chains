import sys
import random
sys.path.append("src/organism/animal")
from Animal import Animal
from typing import List, Any

class Carnivor(Animal):

    def __init__(self, organism_position: List[float], animal_id: int):
        
        super().__init__(organism_position, animal_id)
        
            # inherited variables
                
            # self.organism_position = organism_position
            # self.animal_id = animal_id
            # self.all_known_resources = []
            # self.all_known_organisms = []
            # self.alive_status = True
            # self.hunger = 0
            # self.thirst = 0
            # self.exhaustion = 0
            # self.warned = False
            # self.needs_sleep = False
            # self.in_danger = False
            # self.ready_to_mate = False
            # self.current_target = None
            # self.progress_left_on_decision = 0
        
        self.stalking = False

    # TODO: Implement this method
    # Brain of the animal, this is where the animal will make decisions on what to do next
    def make_decision(self) -> None:
        pass

    # TODO: Implement this method
    def size_up_opponent(self, opponent: Any) -> bool:
        pass

    # TODO: Implement this method
    def Fight(self, opponent: Any) -> None:
        pass

    def update(self) -> None:
        x = random.randint(-4,4)
        y = random.randint(-4,4)

        self.organism_position[0] += x
        self.organism_position[1] += y

