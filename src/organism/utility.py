from typing import List, Any

class Utility:
    
    def __init__(self, all_known_organisms):

        self.all_known_organisms = all_known_organisms
        self.species_id = 10
        self.organism_position = [-1000, -1000]
        self.hidden = True

        self.count_deaths = {
            "starvation": 0,
            "predation": 0,
            "dehydration": 0,
        }
    

    def count_deaths(self, reason):
        self.count_deaths[reason] += 1


        
    
    


if __name__ == "__main__":
    pass