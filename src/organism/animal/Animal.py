import sys
sys.path.append("src")
from organism.Organism import Organism
from typing import List, Any

class Animal(Organism):

    def __init__(self, organism_position: List[float], animal_id: int):

        super().__init__(organism_position, animal_id)

        # inherited variables

        # self.organism_position = organism_position
        # self.animal_id = animal_id
        # self.all_known_resources = []
        # self.all_known_organisms = []
        # self.alive_status = True

        self.hunger = 0
        self.thirst = 0
        self.exhaustion = 0
        self.warned = False
        self.in_danger = False
        self.needs_sleep = False
        self.ready_to_mate = False
        self.current_target = None
        self.progress_left_on_decision = 0

    def drink_water(self, amount: float) -> None:
        self.thirst += amount
    
    def eat_food(self, amount: float) -> None:
        self.hunger += amount
    
    # TODO: Implement this method, This needs to be defined once the simulations update method is defined so we can understand how long a tick is
    def sleep(self) -> None:
        pass

    # TODO: Implement this method, This needs to have creature interaction implemented first
    def procreate(self) -> Any:
        pass

    # TODO: Implement this method, This needs to have creature movement implemented first
    def wander(self) -> None:
        pass

    # TODO: Implement this method, This needs to have some thought put into how creatures will interact with each other
    def run(self, target: Any) -> None:
        pass

    # TODO: Implement this method
    # function detects food within the detection range of the animal
    def Detect_Food(self) -> List[Any]:
        pass

    # TODO: Implement this method
    def Detect_Threats(self) -> List[Any]:
        pass

    # TODO: Implement this method
    def Detect_Mates(self) -> List[Any]:
        pass

    # TODO: Implement this method
    def move_towards_resource(self, resource: Any) -> None:
        pass

    # TODO: Implement this method
    def kill_organism(self, organism: Any) -> None:
        pass