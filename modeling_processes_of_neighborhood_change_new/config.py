# config.py

""" Simulation Parameters """
RHO_L = [8] # Rho: Region housing capacity
ALPHA_L = [0.25] # Alpha: Agent preference (distance [0.0] vs. community [1.0])
T_MAX_RANGE = 10000 # Total timesteps
NUM_AGENTS = 500 # Number of agents
HIGH_BLSCORE_METERS = 5000 # Radius for high Beltline score (greatly impacted areas)
LOW_BLSCORE_METERS = 17500 # Radius for low Beltline score (too far to experience benefits)
BENCHMARK_INTERVALS = 500 # Intervals (# timesteps) to capture frames of GIF

EPSILON = 1e-3 # Rate of learning

"-----------------------------------------------------------------------------------------------------------------------"
""" Misc. Settings """

""" Flags """
RUN_EXPERIMENTS = True  # RUN SIMULATION?
RUN_CALIBRATION = False # RUN CALIBRATION?
PLOT_CITIES = True      # PLOT SIMULATION?
PLOT_FOLIUM = False        # Create Folium graph of t_max?
viewData = False        # View GDF info + more?
viewAmenityData = False # View amenity counts?

""" Visualization Settings """
COLORBAR_NUM_INTERVALS = 20 # Number of distinct colors to show in visualization
DPI = 9600 # DPI resolution of MatPlotLib graphs

""" GIF Settings """
GIF_FRAME_DURATION = 100 # Millseconds
GIF_NUM_PAUSE_FRAMES = 15 # Number of repeat frames to show upon GIF completion

""" Multiprocessing Settings (number of CPU's) """
N_JOBS = -1

""" Geographic key (name) """
CTY_KEY = 'Georgia'


"-----------------------------------------------------------------------------------------------------------------------"


""" Layer handling """

# CENSUS SHAPEFILES (https://www.census.gov/cgi-bin/geo/shapefiles/index.php)
ZIP_URLS = [
    "https://www2.census.gov/geo/tiger/TIGER2024/COUSUB/tl_2024_13_cousub.zip" # County sub (GEOID, NAME)
    #"https://www2.census.gov/geo/tiger/TIGER2010/TRACT/2010/tl_2010_13_tract10.zip" # Census Tracts (GEOID, NAMELSAD10)
    ,"https://www2.census.gov/geo/tiger/TIGER2024/CBSA/tl_2024_us_cbsa.zip" # CBSA (GEOID, NAME)
    #,"https://www2.census.gov/geo/tiger/TIGER2020/COUNTY/tl_2020_us_county.zip" # Counties (GEOID, NAMELSAD)
]
#Census tracts [2010]: https://www2.census.gov/geo/tiger/TIGER2010/TRACT/2010/tl_2010_13_tract10.zip
#PUMA: https://www2.census.gov/geo/tiger/TIGER2024/PUMA20/tl_2024_01_puma20.zip (GEOID20, NAMELSAD) [COULDN'T GET TO WORK]
#County subdivisions: https://www2.census.gov/geo/tiger/TIGER2024/COUSUB/tl_2024_13_cousub.zip (GEOID, NAME)
#Counties: https://www2.census.gov/geo/tiger/TIGER2020/COUNTY/tl_2020_us_county.zip
#Urban Areas: https://www2.census.gov/geo/tiger/TIGER2024/UAC20/tl_2024_us_uac20.zip
#CBSA [metro statistical area]: https://www2.census.gov/geo/tiger/TIGER2024/CBSA/tl_2024_us_cbsa.zip (CBSAFP, NAME)
#States: https://www2.census.gov/geo/tiger/TIGER2024/STATE/tl_2024_us_state.zip (NAME, STUSPS)

# Columns of region identifiers; to be renamed to 'Simulation_ID'
IDENTIFIER_COLUMNS = {
    1: 'GEOID',
    2: 'GEOID',
}

# Column of region names; to be renamed to 'Simulation_Name'
NAME_COLUMNS = {
    1: 'NAME',
    2: 'NAME'
}


""" Income Initialization """
# Database: https://data.census.gov/table?g=040XX00US13

# MEDIAN INCOME IN THE PAST 12 MONTHS (IN 2010 INFLATION-ADJUSTED DOLLARS) (https://data.census.gov/table/ACSST5Y2010.S1903?q=s1903%202010&g=050XX00US13089$1400000,13121$1400000)
# [349 regions]
ECONOMIC_URL = "https://data.census.gov/api/access/table/download?download_id=6fad78b0ac510efbe0f426059c1394dfc06eb60dc6feabc66622be2b05a0048c"
ECONOMIC_DATA_SKIP_ROWS = [1]
ECONOMIC_DATA_COL = "S1903_C02_001E" # Name of 'Income' data column
# "-" label indicates either:
# 1) no sample observations or too few sample observations were available to compute an estimate
# 2) a ratio of medians cannot be calculated because one or both of the median estimates falls in the lowest or upper interval of an open-ended distribution

# TOTAL POPULATION (https://data.census.gov/table/ACSDT5Y2022.B01003?q=B01003&g=050XX00US13089$1400000,13121$1400000)
# [349 regions]
POPULATION_URL = "https://data.census.gov/api/access/table/download?download_id=4633c4c26713411721d6ab3ea6301d2048efb597bbd910dfc5783a9be347b400" 
POPULATION_DATA_SKIP_ROWS = [1, 2]
POPULATION_DATA_COL = "B01003_001E" # Name of 'Population' data column


""" List of regions to simulate """
# County FIPS codes: https://www.census.gov/library/reference/code-lists/ansi/2010.html
# Urban Area names: https://en.wikipedia.org/wiki/List_of_United_States_urban_areas
ID_LIST = [
    ('12060', True), # Atlanta region(s) for CSBA 
    ('13121', True), # Fulton County
    ('13089', True) # Dekalb County
]

""" Beltline 'relation' IDs from Open Street Map """
RELATION_IDS = [8408433, 13048389]


""" Amenity filters """
AMENITY_TAGS = {
    'public_transport': ['platform', 'stop_position', 'station'],
    'highway': 'bus_stop',
    'railway': ['station', 'tram_stop', 'halt', 'subway_entrance'],
    'amenity': [
        'bus_station', 'train_station', 'airport',
        'government', 'university', 'place_of_worship', 'school',
        'civic_center', 'hospital'
    ],
    'shop': 'supermarket',
    'tourism': ['museum', 'hotel'],
    'building': ['apartments', 'house', 'service'],
    'landuse': ['residential', 'industrial']
}