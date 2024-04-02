from typing import List, Any
import random
import sys
sys.path.append("src/organism/animal/herbivor")
from Herbivor import Herbivor

class Rabbit(Herbivor):

    def __init__(self, organism_position: List[float], animal_id: int, all_known_static_resources: Any, all_known_dynamic_resources: Any, all_known_organisms: Any):
                super().__init__(organism_position, animal_id, all_known_static_resources, all_known_dynamic_resources, all_known_organisms)

                # inherited variables

                # self.organism_position = organism_position
                # self.animal_id = animal_id

                # self.all_known_static_resources = {}
                # self.all_known_dynamic_resources = {}
                # self.all_known_organisms = {}
                # self.alive_status = True

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
                # self.hidden = False

                self.name = "Rabbit"
                self.species_id = 7
                self.procreate_cool_down = 500      # ticks
                self.max_hunger = 8640                # ticks
                self.max_thirst = 8640                # ticks
                self.max_exhaustion = 4320            # ticks
                self.min_hunger = 1440                # ticks
                self.min_thirst = 1440                # ticks
                self.max_speed = 4                        # pixels per tick
                self.min_speed = 2                        # pixels per tick
                self.mass = 1
                self.sight_range = 200                # pixels
                self.feeding_range = 5                # pixels (not provided in the stats, so keeping it the same as before)
                self.sleep_duration = 720             # ticks (sleep_lengths converted to ticks)
                self.detection_multiplier = 1         # constant
                self.consumable_resources = [1]       # species_id
                self.potential_predators = [1,5]        # species_id
                self.decision_duration = 50          # ticks
                
                if self.debug_mode:
                        self.color = "white"
                        self.radius = 10

                if self.random_start:
                    self.hunger = random.randint(0, self.max_hunger)
                    self.thirst = random.randint(0, self.max_thirst)
                    self.exhaustion = random.randint(0, self.max_exhaustion)
                    self.procreate_cool_down = random.randint(0, self.procreate_cool_down)


                def procreate(self) -> Any:

                    def get_unique_animal_id() -> int:
                        for i in range(1, len(self.all_known_organisms) + 2):
                            if i not in self.all_known_organisms:
                                return i

                    if not self.current_target.female:
                        self.female = True
                        rabbit_id = get_unique_animal_id()
                        new_rabbit = Rabbit(self.organism_position, rabbit_id, self.all_known_static_resources, self.all_known_dynamic_resources, self.all_known_organisms)
                        
                        self.all_known_organisms[rabbit_id] = new_rabbit

                    else:
                        self.current_target.female = False
                        self.current_target.procreate_cool_down = 66528
                        self.current_target.current_target = None
                        self.current_target.ready_to_mate = False
                        self.procreate_cool_down = 66528
                        self.current_target = None
                        self.ready_to_mate = False

                            
                            
        

                