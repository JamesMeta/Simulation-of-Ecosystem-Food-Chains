import sys
sys.path.append("src/organism/animal/herbivor")
from Herbivor import Herbivor
from typing import List, Any

class GrassHopper(Herbivor):

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
                # self.hidden = False

                self.name = "Grasshopper"
                self.species_id = 8
                self.procreate_cool_down = 45360      # ticks
                self.max_hunger = 25920               # ticks
                self.max_thirst = 8640                # ticks
                self.max_exhaustion = 8640            # ticks
                self.min_hunger = 4320                # ticks
                self.min_thirst = 1440                # ticks
                self.speed = 1                        # pixels per tick
                self.mass = 0.0001
                self.sight_range = 60                 # pixels
                self.feeding_range = 5                # pixels (not provided in the stats, so keeping it the same as before)
                self.sleep_duration = 2160            # ticks (sleep_lengths converted to ticks)
                self.detection_multiplier = 1         # constant
                self.consumable_resources = {1}       # species_id
                self.decision_duration = 100          # ticks


                self.debug_mode = True
                
                if self.debug_mode:
                        self.color = "yellow"
                        self.radius = 1
                        


if __name__ == "__main__":
    pass