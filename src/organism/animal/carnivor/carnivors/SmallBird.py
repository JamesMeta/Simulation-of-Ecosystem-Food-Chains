from typing import List, Any
import sys
import random
sys.path.append("src/organism/animal/carnivor")
from Carnivor import Carnivor

class SmallBird(Carnivor):
    
        def __init__(self, organism_position: List[float], animal_id: int, all_known_static_resources: Any, all_known_organisms: Any):
                super().__init__(organism_position, animal_id, all_known_static_resources, all_known_organisms)

                # inherited variables

                # self.organism_position = organism_position
                # self.animal_id = animal_id

                # self.all_known_static_resources = {}
                # self.all_known_dynamic_resources = {}
                # self.all_known_organisms = {}
                # self.alive_status = True
                # self.visited_static_resources = []
                # self.gender = None

                # self.hunger = 0
                # self.thirst = 0
                # self.exhaustion = 0
                # self.ready_to_mate = False
                # self.current_target = None
                # self.current_threat = None
                # self.progress_left_on_decision = 0
                # self.current_direction = [0, 0]
                # self.safe_place = None

                # self.random_start = True
                # self.debug_mode = True

                # #Binary variables for AI
                # self.needs_sleep = False
                # self.in_danger = False
                # self.needs_food = False
                # self.needs_water = False
                # self.needs_mate = False
                # self.female = False
                # self.needs_for_speed = False
                # self.stalking = False
                # self.current_task = False

                self.name = "Bird"
                self.species_id = 6
                self.max_procreation_cool_down = 20960
                self.procreate_cool_down = 20960    # ticks
                self.max_hunger = 6640               # ticks
                self.max_thirst = 8640               # ticks
                self.max_exhaustion = 8640           # ticks
                self.min_hunger = 3440               # ticks
                self.min_thirst = 1440               # ticks
                self.max_speed = 4                        # pixels per tick
                self.min_speed = 2                        # pixels per tick
                self.mass = 0.03
                self.sight_range = 240               # pixels
                self.feeding_range = 5               # pixels (not provided in the stats, so keeping it the same as before)
                self.sleep_duration = 2880           # ticks (sleep_lengths converted to ticks)
                self.detection_multiplier = 1        # constant
                self.consumable_organisms = [8]   # species_id
                self.potential_predators = [4]        # species_id
                self.decision_duration = 100         # ticks
                self.metabolism_constant = 0.15
                self.litter_size = [1,2,3,4,5,6,7,8]
                
                if self.debug_mode:
                        self.color = "black"
                        self.radius = 2
                
                all_grass_lands = [resource for resource in all_known_static_resources.values() if resource.resource_type_id == 1]
                self.safe_place = random.choice(all_grass_lands)
                

        def procreate(self) -> Any:

                def get_unique_animal_id() -> int:
                        for i in range(1, len(self.all_known_organisms) + 2):
                                if i not in self.all_known_organisms:
                                        return i

                        if self.gender == 0:
                                return
                
                for i in range(random.choice(self.litter_size)):
                        animal_id = get_unique_animal_id()
                        x = self.organism_position[0] 
                        y = self.organism_position[1] 
                        position = [x, y]
                        new_animal = SmallBird(position, animal_id, self.all_known_static_resources, self.all_known_organisms)
                        self.all_known_organisms[animal_id] = new_animal
                        new_animal.procreate_cool_down = self.max_procreation_cool_down

                self.procreate_cool_down = self.max_procreation_cool_down
                self.ready_to_mate = False
                self.current_task = False

                

                self.current_target.current_target = None
                self.current_target.current_task = False
                self.current_target.ready_to_mate = False
                self.current_target.procreate_cool_down = self.max_procreation_cool_down
        
                self.current_target = None

