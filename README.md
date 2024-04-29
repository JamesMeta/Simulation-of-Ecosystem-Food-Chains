---
runme:
  id: 01HWM4W0B0HHJ2MYQPEG4JFAB9
  version: v3
---

# Ontario Tech University Faculty of Science, Computer Science

**Date:** April 6, 2024

---

## Simulation and Modelling Course Project:

**Food Web Simulation**

![Screenshot](/images/Picture0.png)

**Authors:**
James Mata, Clayton Cotter-Wasmund

---

### Abstract

This report is a summary of the full report you can view with the included pdf file. This project simulates an ecosystem centered around food web interactions, capturing biological relationships in a local environment.

### Repository

[Food Web Simulation Repository](https://github.com/JamesMeta/Simulation-of-Ecosystem-Food-Chains)

### How To Run

Simply run the Simulation.exe executable located in the root folder for the repository. A blank Pygame screen will open before all options are selected so be sure to return to the terminal after the window opens to complete your choices.

### Demonstration

[Food Web Simulation Demonstration](https://youtu.be/1EuounfYO8k)

---

# 1. Introduction

The goal of the project was to simulate an ecosystem with multiple intertwined food webs, and see if said ecosystem was able to reach sustainable levels that mimic natural ecological processes. Among the considered outcomes was:

![Screenshot](/images/Picture1.png)

**Figure 1:** Population graphs of carnivores and herbivores relating to predation, primarily the result- ing wave forms and how they compare to observed phase syn- chronizations.

![Screenshot](/images/Picture2.png)

**Figure 2:** Reproductive survival numbers that are regulated by the carrying capacity of the environment.

![Screenshot](/images/Picture3.png)

**Figure 3:** Population analysis of food chains / trophic levels. In the terms of environmental science this would be biomass distributions.

---

# 2. Inspirations and Related Work

The inspiration for this project came from our appreciation for nature and interactive ecosystem simulations like Equilinox. We also used BYJU’s explanation of food webs to structure our interactions. No single academic paper served as the primary reference for this project, as we focused on widely accepted ecological observations.

### A. Equilinox

![Screenshot](/images/Picture4.png)

**Figure 4:** Equilinox is a relaxing nature simulation game where players create and nurture ecosystems.

### B. BYJU Food Web

![Screenshot](/images/Picture5.png)

**Figure 5:** This food web includes all four trophic levels, with one producer (grass), and multiple primary (rabbit, mouse, grasshopper), secondary (small bird, frog, snake), and tertiary (hawk, fox, owl) consumers.

---

# 3. Methodology

The simulation's implementation revolves around decision trees for ecosystem interactions. Animals are categorized as carnivores or herbivores, with their behaviors outlined in the repository's design folder.

Key logic points include resource prioritization based on threshold levels, with critical decisions like sleep, water, food, and reproduction governed by these thresholds. The simulation also relies on ordinary differential equations for time progression and Lotka-Volterra predator-prey models for population dynamics.

---

# 4. Results

Our project aimed to validate the ecosystem simulation through various tests and observations.

![Screenshot](/images/Picture6.png)  
![Screenshot](/images/Picture7.png)

**Figures 6-7:** Predation relationship between rabbits and foxes, showing proportionality between population fluctuations.

Carrying capacity tests were conducted to understand how the ecosystem adjusted to resource availability, reflecting natural behavior patterns.

![Screenshot](/images/Picture8.png)  
![Screenshot](/images/Picture9.png)

**Figures 8-9:** Demonstration of the carrying capacity phenomenon in a simulation with only rabbits and grass.

The interaction between trophic levels was also tested, examining the flow of energy and biomass distribution within the ecosystem.

![Screenshot](/images/Picture10.png)  
![Screenshot](/images/Picture11.png)  
**Figures 10-11:** Biomass distribution across different trophic levels, demonstrating realistic energy flow.

---

# 5. Scope and Limitations

The primary assumption in our simulation is that all animals know where resource areas are located, limiting the scope to smaller environments. Issues like infinite resource respawning and inability to simulate ecosystem extinction were among the limitations we encountered.

---

# 6. Conclusion

Despite the limitations, we are confident in our achievements regarding interactions between animals in a diverse ecosystem. The systematic approach to building and testing the simulation allowed us to create realistic food chains and trophic levels.

---

# 7. References

1. AspidistraK. "Lotka–Volterra Equations Linearized Solution Graph." Wikipedia, March 28, 2024. [Link](https://en.wikipedia.org/wiki/Lotka)
2. Quittem, Brandon. "Bitcoin Is a Pioneer Species." Medium, January 5, 2023. [Link](https://medium.com/the-bitcoin-times/bitcoin-is-a-pioneer-species-38f42ecdbb88)
3. ThinMatrix. "Equilinox PressKit." Equilinox, 2019. [Link](https://equilinox.com/presskit/sheet.php?p=equilinox)
4. "Logistic Population Growth." Encyclopædia Britannica, 2012. [Link](https://www.britannica.com/science/population-ecology/Logistic-population-growth)
5. "Food Chain: Definition, Types, Examples, FAQs." BYJUS, October 4, 2023. [Link](https://byjus.com/biology/overview-of-food-chain/)
