# City.py

import numpy as np
import pandas as pd
import osmnx as ox


# ==========
# CITY CLASS
# ==========

class City:

    def __init__(self, centroids, g, amts_dens, centroid_distances, rho, geo_id_to_income):
        """ Constructor """
        self.rho = int(rho)  # house capacity
        self.centroids = centroids  # centroids list
        self.g = g  # OSM graph
        self.n = len(centroids) # num centroids

        # STORE ATTRIBUTES OF ALL CENTROIDS
        self.lon_array = np.array([lon for lon, _, _, _, _ in centroids])  # Longitude
        self.lat_array = np.array([lat for _, lat, _, _, _ in centroids])  # Latitude
        self.name_array = [name for _, _, name, _, _ in centroids]  # Centroid region name
        self.beltline_score_array = np.array([beltline_score for _, _, _, beltline_score, _ in centroids]) # Beltline Score
        self.id_array = self.id_array = [id for _, _, _, _, id in centroids]  # ID

        self.inh_array = [set() for _ in range(self.n)]  # Array of sets - each set contains Agent inhabitants
        self.dow_thr_array = np.zeros(self.n)  # Endowment threshold
        self.upk_array = np.zeros(self.n, dtype=bool)  # Upkeep score
        self.cmt_array = np.zeros(self.n)  # Community score

        self.pop_hist = [[] for _ in range(self.n)]  # Population history - list of lists
        self.cmt_hist = [[] for _ in range(self.n)]  # Community score history - list of lists

        self.node_array = np.array(
            [ox.nearest_nodes(self.g, lon, lat) for lon, lat in zip(self.lon_array, self.lat_array)])

        # Amenity density and centroid distances
        self.amts_dens = amts_dens
        self.centroid_distances = centroid_distances

        # Map GEO_ID to income
        self.geo_id_to_income = geo_id_to_income

    def set_agts(self, agts):
        """ Initialize agents and their endowments """
        self.agts = agts  # list of agents
        self.agt_dows = np.array([a.dow for a in self.agts])  # array of agent endowments

    def update(self):
        """ Update each centroid's: Population, CMT score, UPK score """
        
        for index in range(self.n):  # For each centroid
            inhabitants = self.inh_array[index]  # Centroid inhabitants
            pop = len(inhabitants)

            self.pop_hist[index].append(pop) # Update population history

            if pop > 0:  # Inhabited
                ''' Community Score ''' #(avg inhabitant dows, weighted by distance to other centroids) #TODO: check logic
                inhabitant_dows = np.array([a.dow for a in inhabitants])  # Array of endowments of node's inhabitants
                distances = self.centroid_distances[index, [a.u for a in inhabitants]]
                weights = (1 - distances) ** 2

                cmt = np.average(inhabitant_dows, weights=weights) #Calculate

                ''' Upkeep score '''
                if pop < self.rho:
                    self.dow_thr_array[index] = 0.0
                else:
                    self.dow_thr_array[index] = np.partition(inhabitant_dows, -self.rho)[-self.rho]
                self.upk_array[index] = 1.0
                
            else:  # If uninhabited
                self.dow_thr_array[index] = 0.0
                self.upk_array[index] = 0.0
                cmt = 0.0

            # Update Community history and Community Score (average endowment)
            self.cmt_hist[index].append(cmt)
            self.cmt_array[index] = cmt

    # =====================
    # SAVE DATA TO CSV FILE
    # =====================
    def get_data(self):
        """
        Gather data for each centroid and return as a DataFrame.

        Returns:
        - DataFrame: Data containing Centroid, Population, Avg Endowment, Beltline Score, Amt Density.
        """
        data = []  # Array storing data for each centroid
        
        avg_incomes = np.zeros(self.n)
        for index in range(self.n):
            population = len(self.inh_array[index])
            # Average Endowment
            if population > 0:
                avg_endowment = (np.mean([agent.dow for agent in self.inh_array[index]]))
            else:
                avg_endowment = 0.0
            avg_incomes[index] = avg_endowment

        # Normalize avg_endowments
        min_val = avg_incomes.min()
        max_val = avg_incomes.max()

        # Normalize endowments
        normalized_avg_endowments = (avg_incomes - min_val) / (max_val - min_val)

        for index in range(self.n):
            # ID
            ID = self.id_array[index]

            # Name
            centroid_name = self.name_array[index]

            # Population
            population = len(self.inh_array[index])
            
            avg_income = avg_incomes[index]

            avg_endowment = normalized_avg_endowments[index]

            # Beltline Score
            beltline_score = self.beltline_score_array[index]

            # Amenity Density
            amenity_density = self.amts_dens[index]

            # Expected income (2010 median income data)
            
            if  ID in self.geo_id_to_income:
                expected_income = self.geo_id_to_income[ID]
            else:
                expected_income = "NA"

            data.append({
                'Simulation_ID': ID,
                'Centroid Name': centroid_name,
                'Population': population,
                'Avg Income': avg_income,
                'Expected Income': expected_income,
                'Avg Endowment': avg_endowment,
                'Beltline Score': beltline_score,
                'Amt Density': round(amenity_density, 2)
            })

        df = pd.DataFrame(data)

        return df