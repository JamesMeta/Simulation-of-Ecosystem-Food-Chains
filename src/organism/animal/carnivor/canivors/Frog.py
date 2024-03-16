from typing import List, Any
import Carnivor

class Frog(Carnivor.Carnivor):
    
        def __init__(self, species_id: int, alive_status: bool, 
                    procreate_cool_down: float, organism_position: List[float],
                    animal_id: int, hunger: float, max_hunger: float,
                    thirst: float, max_thirst: float, speed: float, mass: float, exhaustion: float, max_exhaustion: float, 
                    visibility_range: float, detection_range: float, feeding_range: float, sleep_duration: int, 
                    detection_multiplier: float, warned: bool, in_danger: bool, ready_to_mate: bool,
                    consumable_organisms: List[int], consumable_resources: List[int], all_known_resources: List[Any],
                    decision_duration: int
                    ):
            
            super().__init__(species_id, alive_status, procreate_cool_down, organism_position, animal_id, hunger, max_hunger, thirst, max_thirst, speed, mass, exhaustion, max_exhaustion, visibility_range, detection_range, feeding_range, sleep_duration, detection_multiplier, warned, in_danger, ready_to_mate, consumable_organisms, consumable_resources, all_known_resources, decision_duration)

            self.name = "Frog"