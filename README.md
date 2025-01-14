# MPONC_Streamlined
'Modeling Processes of Neighborhood Change' [Streamlined]

## Introduction
> This streamlined version of the '[24Fa-MPONC]([url](https://github.com/VIP-SMUR/24Fa-MPONC))' research project simulates the impact of the Atlanta Beltline on the surrounding metropolitan area using game theory. The simulation models agent movement across county subdivisions, with agents seeking to move optimally (seeking 'attractive' county subdivisions) based on various factors.
> 
> **GOAL:** The goal of this project is to provide a streamlined, user-friendly parametric simulation tool for Dr. Kastner's research seminar at the Georgia Institute of Technology. Users (students) will be able to experiment, hypothesize, and investigate their own research questions related to urban development patterns, as well as practice using parametric research tools.
<hr>

*The full methodology, game theory, and findings of the full project can be found in the original [24Fa-MPONC]([url](https://github.com/VIP-SMUR/24Fa-MPONC)) repository; it is also pasted below after the *USER GUIDE* section, comprising the entire remainder of this README.*

# User Guide
## Simulating the Atlanta Beltline
- The **Atlanta Beltline** is a public transportation network, providing a higher quality of life and economic opportunities for locals. It's located in Atlanta, Fulton County. In this simulation, we model how individuals, or "agents", move between County Subdivisions depending on various factors including average wealth, distance, proximity to the Atlanta Beltline, population, etc. This simulation will output a GIF, showing a **graph** with **circles** in the center of each region. In each region, the number represents the region's population while the region color represent the average wealth.
- **Beltline score**: Depending on a region's proximity to the Atlanta Beltline (determined by your *HIGH_BLSCORE_METERS* and *LOW_BLSCORE_METERS* parameters, described below), regions will have their centroids shaded **green** depending on their proximity to the Atlanta Beltline (dark green = closer to the beltline -> higher '*beltline*' score). A higher *beltline* score reduces the cost of moving to a region.
> Each region has a 'cost', ranging from 0 to 1. Agents are more likely to move to regions with lower cost.
<hr>

### Atlanta Beltline:
<img src="./Images/Fulton-Atlanta Beltline Visual.png" width="300">

### Example simulation GIF:
- <img src="./Images/StreamlinedSimulationGif.gif" width="300">

## Setup

```bash
cd modeling_processes_of_neighborhood_change_new
conda create -n mponc python=3.12
conda activate mponc
pip install -r requirements.txt
python main.py
```
## Project Settings
> Below are changeable parameters which decide how 'cost' is calculated, changing agent behavior.
<hr>

### To change the below settings, simply open the 'config.py' file and edit the code at the top
- Don't forget to save the file in your IDE before running **main.py** (ctrl+s in some IDE's)

#### RHO_L
- Population capacity
  - It's possible that this capacity be exceeded; however, cost is then maximized.
#### ALPHA_L
- How much agents prioritize **proximity** score (distance) to another centroid VS. **community** score.
  - Note: A region's '_proximity_' score is higher if it's close by; '_community_' score increases if an agent's income is similar to a region's average income.
  - *Fun fact: Agents are assigned a random *income* based on the actual median incomes throughout Fulton and Dekalb counties !*
> **RHO_L** and **ALPHA_L** are both arrays; you can enter multiple values in each to run multiple simulations *simultaneously*.
> 
> Ex. RHO_L = [2, 4]; ALPHA_L = [0.25, 0.75] will run four simulations with rho=2 alpha=0.25, rho=2 alpha=0.75; rho=4 alpha=0.25; and rho=4 alpha=0.75.
<hr>

#### NUM_AGENTS
- Number of agents
- *NOTE: This affects simulation runtime greatly; I recommend NOT exceeding **1000** agents*
#### T_MAX_RANGE
- Duration of the simulation
  - Measured by 'timesteps'
  - 'Timestep' refers to a single instance agent action (relocation); 20,000 timesteps mean the agents relocate a total of 20,000 times during the simulation.*
#### BENCHMARK_INTERVALS
- Interval (# timesteps) to capture the frames of the GIF at
  - This simulation outputs a GIF to visualize results; this parameter decides how many frames should be in GIF (T_MAX_RANGE / BENCHMARK_INTERVALS)
#### HIGH_BLSCORE_METERS & LOW_BLSCORE_METERS
- **HIGH_BLSCORE_METERS**: All regions (their centroids) within this distance will have the highest "Beltline" score (1.0)
- **LOW_BLSCORE_METERS**: All regions (their centroids) outside this distancew ill have the lowest "Beltline" score (0.2)
- All regions in between these values will have a score decreasing linearly from 1.0 to 0.2, depending on their distance away
  - Ex. If HIGH_BLSCORE_METERS = 1000 and LOW_BLSCORE_METERS = 5000, then all region centroids within 1km will have a 1.0 score; a centroid 3km away will have a 0.6 score; centroids 5km or more away will have a 0.2 score.

# TODO: explain agent wealth distributions.

## Reference paper

```bibtex
@misc{mori2024modelingprocessesneighborhoodchange,
      title={Modeling Processes of Neighborhood Change}, 
      author={J. Carlos Martínez Mori and Zhanzhan Zhao},
      year={2024},
      eprint={2401.03307},
      archivePrefix={arXiv},
      primaryClass={cs.MA},
      url={https://arxiv.org/abs/2401.03307}, 
}
```
> The remainder of this README is a copy of the original '24Fa-MPONC' GitHub's README.
# 24Fa-MPONC README:

:   !!! abstract

        This research project simulates the impact of the Atlanta Beltline on neighborhood gentrification using game theory and no-regret dynamics. The simulation models agent movement across census tracts, with agents seeking to minimize costs based on factors like amenity density. The methodology incorporates the four-step model for trip generation and leverages US Census data for population and income distributions. Census tract regions are mapped using TIGER/Line shapefiles, while the Beltline area is defined using OpenStreetMap data. The simulation outputs include dynamic visualizations and CSV data tracking population and income changes across census tracts, providing insights into urban development patterns.



## Intro and Description
This project is based on the reference paper created by Dr. Martinez and Dr. Zhao, which aims to address the following: 
- How does the layout of transportation infrastructure affect the demographics of nearby neighborhoods?
- Does the creation of these infrastructure actually benefit everyone equally; is it fair?
- Can we predict the effects on surrounding communities before these structures are actually built?

These questions are primarily motivated by the issue of gentrification, an issue prevalent in many major cities. This semester, we utilized concepts in game theory, more specifically no-regret dynamics, in order to simulate the effects of the Atlanta Beltline on gentrification. Throughout this semester we followed the main ideas provided by this lecture from Stanford University: "[CS364A: Algorithmic Game Theory Lecture #17: No-Regret Dynamics](https://theory.stanford.edu/~tim/f13/l/l17.pdf)". To summarize our approach with no-regret dynamics:

- People, or 'agents', randomly move from region to region. Depending the region's attributes, a **'cost'** value is assigned to each action.
  - *'Cost' is a function of centroid proximity, number of amenities, average income, mode of transportation, and more.*
- The higher the cost, the less likely an agent is to visit that centroid in the future.
- This process is repeated until the probability distribution of visting centroids converges - an equilibrium is reached, and further actions make no difference. 

### Cost Function
Our current cost function takes into account a region's affordability, site upkeep, access to the Atlanta Beltline, location, community ties, and access to desirable amenities:

> **cost = 1 - (affordability * upkeep * beltline * location_cost * community_cost * accessibility)**

- Affordability [0 or 1]: Affordability score is [0] if 'unaffordable'; a region is 'unaffordable' if its housing capacity has been reached AND all of its inhabitants have a higher income than an Agent.
- Upkeep [0 or 1]: Upkeep score is [1] if the population is not zero.
- Access to Beltline [0 or 1]: Beltline score is [1] if the region contains part of the Atlanta Beltline.
- Location [0.0 to 1.0]: Location score is a function of* region proximity *and an Agent's* mode choice *(car vs. transit).
  - *'Transit' just adds a 1.5x multiplier to the raw distance cost.*
- Community [0.0 to 1.0]: Community score is the similarity between a region's average income and an Agent's average income.
- Accessibility [0.0 to 1.0]: Accessibility score is the normalized amenity density of a region.
  - *Considered amenities are derived from **[24Sp-Mobility-Seg](https://vip-smur.github.io/24sp-mobility-seg/)**, another Georgia Tech research team, in which they investigated which features of a city are most important to residents.*
  - *We excluded certain amenities at our own discretion, such as 'shed', 'guardhouse', 'ferry_terminal', 'garages', and 'bridge' (labels as they appear on OpenStreetMap).*

#### Implemented Amenities (OpenStreetMap labels):

<img src="./Figures/AmenityTags.png" width="500">


### Case study
We decided to apply the above to Atlanta and the Atlanta Beltline, as our case study for this semester. Key changes we have made to accommodate this implementation include: Incorporating the **Four-Step Transportation Model**, to determine mode of transportation for our agents, and an "in Beltline" attribute so our agents can differentiate between regions containing the Atlanta Beltline, and those outside of it. 

## The Four-Step Model
Given that the agents move across various subregions of the Atlanta area in our simulation, one of the critical steps of the simulation is figuring out what subregion the agents go to. To do this in a way that accurately represents real-world distributions, we turned to the four-step model, a common trip generation algorithm: 

<img width="758" alt="Screenshot 2024-12-03 at 2 19 28 PM" src="./Figures/FourStepModel.png">

The model has four components:

1. Trip Generation: This part of the model estimates the number of trips originating from or destined for a specific area. It focuses on understanding how many trips are generated rather than specific travel patterns. This process usually involves some type of data pertaining to the area at hand, such as demographics, income, or land usage.
2. Trip Distribution; This part of the model estimates the number of trips for routes that go from an area to another, as determined in the trip generation step. This process is typically done using the gravity model, which assumes that the number of trips are positively correlated with the attractiveness of an area and inversely correlated to distance.
3. Mode Choice: This part of the model determines the mode of transporation used to make the trips. This is typically done by considering demographic data (such as the percentage of people with cars) in an area.
4. Route Assignment: This part of the model determines the routes travelers take between origins and destinations. This is typically done by considering the route that takes the shorted possible time, and following that. 

Our approach closely follows these four components. We first generate trips by considering the amenity density of areas. We sum up all amenity densities, and divide each area's density by this sum to generate a probability. We then utilize a Poisson Distribution to generate the number of trips by multipling a base number of trips by the probability. We then consider trip distribution through a modified gravity model. The equation for our model is the following, given that we aim to go from area/region i to j:

<img width="686" alt="Screenshot 2024-12-03 at 2 37 56 PM" src="./Figures/GravityModel.png">

We essentially multiply the total number of trips from area i to area j with the net amenity score for the destination j times transportation cost for that specific trip from area i to j, divided by the net amenity score for area j times the transportation cost from area i to j summed up over all destination j's. 

For our modal split, we assume that the car ownership rate is 0.7, and that the transit rate is 0.3. Each region's trips are split based on this. We then assign these routes based on the shortest possible distance.

Through this process, we were able to have a methodical way of distributing the agents across Atlanta based on area factors such as amenity density.

## Census-based approach
Our project utilizes data from the US census wherever possible. Notably, the graphical regions our agents inhabit correspond directly to US census tracts. Consequently, we can compare the economic and population data obtained from our simulation to actual census data for each census tract. Furthermore, since the US Census TIGER/Line Geodatabases contain publicly available shapefiles of all geographic regions it reports on, our simulation can likewise operate utilizing any other census-reported regions, including zip codes, housing districts, school districts, etc. 

Additionally, each 'agent' has a unique wealth attribute as one of the factors influencing decision-making. Instead of assigning these wealths arbitrarily, we create this distribution of wealth using census population and median income data, so that our agents are representative of actual Fulton and Dekalb county resident demographics. Namely, we use the following tables from the Census website: "[S1903 | Median Income In The Past 12 Months (In 2010 Inflation-adjusted Dollars) - ACS 5-Year Estimates Subject Tables](https://data.census.gov/table/ACSST5Y2010.S1903?q=s1903%202010&g=050XX00US13089$1400000,13121$1400000)" and "[B01003 | Total Population - 2010: ACS 5-Year Estimates Detailed Tables](https://data.census.gov/table/ACSDT5Y2022.B01003?q=B01003&g=050XX00US13089$1400000,13121$1400000)". By changing the hyperlinks in our code, our simulation can run with different distributions; for example, those from different years.
* *Note: For the median income and population tables, the hyperlinks in the code won't be 'activated', or functional, until a request is made directly on the Census website - navigate to those links and use the 'Download' button for the appropriate graphs, then run the code; no other action needed. [Fix incoming]*

### TIGER/Line Geodatabases shapefiles:
![Alt text](./Figures/ZIP_URLs.png)

### Income distribution tables:
![Alt text](./Figures/Databases.png)

### [Example] Simulating a different geographic region (close-up of Atlanta):
![Alt text](./Figures/OldZipURL.png)

![Alt text](./Figures/AtlantaBeltlineCloseupGraph.png)


## Project status
### Outputs & configuration
Our code outputs a GIF to visualize agent behavior over time. Each circle represents the centroid of a census tract - green signifying those in the Atlanta Beltline - and the encircled number is the agent population.
Our code also outputs a CSV file containing all the simulated data at every individual timestep.

* *Data contained in CSV's: Census tract name, agent population, raw average income, average income reported by census, normalized average incomes, and amenity density.*
        * *TODO: Include raw amenity counts, census tract geographic area (sqkm).*
* *Note: 'Timestep' refers to a single instance agent action (relocation); 20,000 timesteps mean the agents relocate a total of 20,000 times during the simulation.*

#### GIF
This GIF shows the behavior of 1,000 agents up to 20,000 timesteps, frames being captured every 400 timesteps. Rho=1, alpha=0.25.
![Alt text](./Figures/SimulationGIF.gif)

#### Configuration
In **configuration.py**, the user can specify various settings of the simulation. Changing graph settings is a matter of changing the hyperlinks in **configuration.py**.

**Simulation settings:** 
* Total timesteps run in the simulation
* Timestep interval at which to capture the GIF's frames
* Number of agents
* Variables affect agent behavior
**Graph settings:**
* Regions to simulate
* Economic distribution data
* Regions to mark as 'in the Atlanta Beltline'

Simulation and graph settings:

![Alt text](./Figures/Parameters.png)

![Alt text](./Figures/IDList.png)

### Runtimes
>(1000 agents, 530 census tracts)

Run on a laptop...

Fetching amenities from OpenStreetMap via OSMnx: ~37 minutes
Computing centroid distances: ~18 minutes
Simulation (x8): ~45 minutes
GIF creation (x1), 50 frames: ~19 min
* *Everything except 'Simulation' and 'GIF creation' is cached, making their runtimes negligible in subsequent runs*

## Atlanta Beltline in our Simulation
We automate the process of labelling certain regions as 'in the Atlanta Beltline' by using commuting paths from OpenStreetMap that correspond to the Atlanta Beltline - namely, a bike trail and a railway. To experiment with a different beltline, such as a beltline that spanned across Atlanta horizontally, or simply expanded north by x miles, we would acquire the OpenStreetMap ID's of existing paths (bike trails, walking paths, roads, etc.) corresponding to our desired Beltline, and paste these into **configuration.py**. Alternatively, we can create a such path ourselves in OpenStreetMap.
Then, any region containing segments of these trails would automatically be marked as "In the Atlanta Beltline". 

* *Note: our current code only works if these trails are labelled as "Relations" in OpenStreetMap*
        * *TODO: make this dynamic*

In **configuration.py** - bike trail and railroad OpenStreetMap ID's:

![Alt text](./Figures/RelationIDs.png)

Bike Trail                 |  Railroad
:-------------------------:|:-------------------------:
<img src="./Figures/BeltlineBikeTrail.png" width="300">   |  <img src="./Figures/BeltlineRailroad.png" width="300">

Compare with Atlanta Beltline geography:

<img src="./Figures/AtlantaBeltlineVisual.jpg" width="300">


## Strengths and Weaknesses
### Strengths
Our approach is very modularized. For instance, the four-step model created can be used in any other simulation of any other region. It simply needs lists of agents, a NetworkX graph, and other generalized parameters to operate. Furthermore, Our approach is backed by established human behavior approaches (no-regret dynamics), utilizes a distribution system that is also established (four-step model). We are able to produce dynamic visuals (GIFs).

### Weaknesses
Our approach is only limited to the 2010 Census data for “training purposes.” This may cause our model to overfit and be unable to reliably extrapolate to 2022 Census Data. Additionally, it is very time-consuming to run the simulation, as 37 minutes are currently needed to generate centroids. We aimed to solve this issue with multithreading, but API calls caused this to fail (we kept running into buffering issues). Our simulation also assumes that there is no immigration/emigration in Atlanta, as we have a set, fixed number of agents. We also limit transportation choices to cars and public transportation, even though there are other mediums. 

### Next Steps
This coming Spring semester, we hope to make the GIFs more clearer (currently, there is a lot of regions and it is hard to read which regions the agents are in). We additionally want to add weights to certain amenities, as realistically, some amenities are more valuable than others in driving agent decisions (for example, schools may play a more important than bike stands in driving what regions agents go to). Additionally, this coming semester, we hope to get the necessary parameters from the 2010 data and try to reproduce the 2020 demographics. 



## Presentation


<a href="https://www.youtube.com/watch?v=sXhnPRdE7Hk" target="_blank" rel="noopener noreferrer">
    <img src="https://img.youtube.com/vi/sXhnPRdE7Hk/maxresdefault.jpg" width="480" alt="Final Presentation --- 24Fa --- Modeling Processes of Neighborhood Change (MPONC)" class="off-glb">
</a>



## Team

| Name                  | Seniority | Major                  | Department | GitHub Handle                                                 | 
| --------------------- | --------- | ---------------------- | ---------- | ------------------------------------------------------------- | 
| Matthew Lim           | Sophomore | Computer Science       | COC        | [mlim70](https://github.com/mlim70)                           |                      
| Reyli Olivo           | Junior    | Civil Engineering      | CEE        | [Rolivo05](https://github.com/Rolivo05)                       |                   
| Devam Mondal          | Junior    | Computer Science       | COC        | [Dodesimo](https://github.com/Dodesimo)                       | 
