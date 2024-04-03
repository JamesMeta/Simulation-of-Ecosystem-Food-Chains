import sys
import random
sys.path.append("src/organism/animal")
from Animal import Animal
from typing import List, Any

class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BLACK = '\033[30m'
    

# Colorizing function
def colorize(text, color):
    return f"{color}{text}{colors.RESET}"

class Carnivor(Animal):

    def __init__(self, organism_position: List[float], animal_id: int, all_known_static_resources: Any,  all_known_organisms: Any):
        
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
        # self.current_task = False

        self.stalking = False

        #override these variables in the child class
        self.species_id = None
        self.procreate_cool_down = None
        self.max_hunger = None
        self.max_thirst = None
        self.max_exhaustion = None
        self.min_hunger = None
        self.min_thirst = None
        self.max_speed = None
        self.min_speed = None
        self.mass = None
        self.sight_range = None
        self.feeding_range = None
        self.sleep_duration = None
        self.detection_multiplier = None
        self.consumable_organisms = None
        self.decision_duration = None
        self.potential_predators = None

    # TODO: Implement this method
    # Brain of the animal, this is where the animal will make decisions on what to do next
    def make_decision(self) -> None:
        pass

    def Detect_Food(self) -> List[Any]:
        pass

    def update(self) -> None:
        x = random.randint(-4,4)
        y = random.randint(-4,4)

        self.organism_position[0] += x
        self.organism_position[1] += y

