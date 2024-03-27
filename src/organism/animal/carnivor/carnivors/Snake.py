import sys
sys.path.append("src/organism/animal/carnivor")
from Carnivor import Carnivor
from typing import List, Any

class Snake(Carnivor):
    
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
                # self.in_danger = False
                # self.needs_sleep = False
                # self.ready_to_mate = False
                # self.current_target = None
                # self.progress_left_on_decision = 0
                # self.stalking = False

                self.name = "Snake"
                self.species_id = 4
                self.procreate_cool_down = 181440     # ticks
                self.max_hunger = 120960               # ticks
                self.max_thirst = 8640                 # ticks
                self.max_exhaustion = 8640             # ticks
                self.min_hunger = 20160                # ticks
                self.min_thirst = 1440                 # ticks
                self.speed = 1                         # pixels per tick
                self.mass = 0.25
                self.sight_range = 120                 # pixels
                self.feeding_range = 5                 # pixels (not provided in the stats, so keeping it the same as before)
                self.sleep_duration = 1440             # ticks (sleep_lengths converted to ticks)
                self.detection_multiplier = 1          # constant
                self.consumable_organisms = {3, 6}     # species_id
                self.decision_duration = 100           # ticks

                
                self.debug_mode = True

                if self.debug_mode:
                        self.color = "red"
                        self.radius = 5

                
                


