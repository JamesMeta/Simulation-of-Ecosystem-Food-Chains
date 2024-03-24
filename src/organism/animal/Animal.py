import sys
sys.path.append("src")
from organism.Organism import Organism
from typing import List, Any

class Animal(Organism):

    def __init__(self, species_id: int, alive_status: bool, 
                procreate_cool_down: float, organism_position: List[float],
                animal_id: int, hunger: float, max_hunger: float,
                thirst: float, max_thirst: float, speed: float, mass: float, exhaustion: float, max_exhaustion: float, 
                visibility_range: float, detection_range: float, feeding_range: float, sleep_duration: int, 
                detection_multiplier: float, warned: bool, in_danger: bool, ready_to_mate: bool,
                consumable_organisms: List[int], consumable_resources: List[int], all_known_resources: List[Any],
                decision_duration: int
                ):
        
        super().__init__(species_id, alive_status, procreate_cool_down, organism_position)
        self.animal_id = animal_id
        self.hunger = hunger
        self.max_hunger = max_hunger
        self.thirst = thirst
        self.max_thirst = max_thirst
        self.speed = speed
        self.mass = mass
        self.exhaustion = exhaustion
        self.max_exhaustion = max_exhaustion
        self.visibility_range = visibility_range
        self.detection_range = detection_range
        self.feeding_range = feeding_range
        self.sleep_duration = sleep_duration
        self.detection_multiplier = detection_multiplier
        self.warned = warned
        self.in_danger = in_danger
        self.ready_to_mate = ready_to_mate
        self.consumable_organisms = consumable_organisms
        self.consumable_resources = consumable_resources
        self.all_known_resources = all_known_resources
        self.current_target = None
        self.decision_duration = decision_duration
        self.all_known_organisms = []
        self.progress_left_of_decision = 0

    def drink_water(self, amount: float) -> None:
        self.thirst += amount
        if self.thirst > self.max_thirst:
            self.thirst = self.max_thirst
    
    def eat_food(self, amount: float) -> None:
        self.hunger += amount
        if self.hunger > self.max_hunger:
            self.hunger = self.max_hunger
    
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