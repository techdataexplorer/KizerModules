
import math
from haversine import haversine, Unit
import pandas as pd

class FindTheCity(object):

    def __init__(self):
        self.FolderPath = ""
        self.Lat = 0
        self.Long = 0

    def setFolderPath(self, folderPath):
        self.FolderPath = str(folderPath)

    def setLatitude(self, latitude):
        self.Lat = float(latitude)

    def setLongitude(self, longitude):
        self.Long = float(longitude)

    # def setMilesKm(self, milesKm):
    #     self.MilesKm = milesKm
    #     self.MilesKm = self.MilesKm.upper()

    # def distance_between_a_and_b(self, MilesKm, LATITUDEA, LATITUDEB, LONGITUDEA, LONGITUDEB):
    #     # 'CALCULATE DISTANCE BETWEEN SITE A and SITE B
    #     # 'INPUT: LATITUDEA#, LATITUDEB#, LONGITUDEA#, LONGITUDEB#
    #     # 'OUTPUT: Z# (DISTANCE IN MILES)

    #     # 'HIGH ACCURACY FORMULA
    #     Z = (math.sin((math.radians(LATITUDEA - LATITUDEB)) / 2)) ** 2
    #     Z += math.cos(math.radians(LATITUDEA)) * math.cos(math.radians(LATITUDEB)) * (math.sin((math.radians(LONGITUDEA - LONGITUDEB)) / 2)) ** 2
    #     Z = math.sqrt(Z)
    #     # X = Z
    #     ZSHORT = 2 * (180 / math.pi) * math.asin(Z)

    #     if MilesKm == "M":
    #         return round(69.06 * ZSHORT)  # DISTANCE IN MILES
    #     # elif MilesKm == "K":
    #     return round(111.1 * ZSHORT)  # DISTANCE IN KILOMETERS

    def execute(self):

        CitiesFilePath = self.FolderPath + "/All Cities.csv"
        #xlsCitiesFilePath = self.FolderPath + "/Other/All Cities.xls"
        cities_df = pd.read_csv(CitiesFilePath) 
        #print(cities_df)
        smallestDistance = float('inf')
        smallestIndex = 0

        #finds the distance with each city
        userCity = (self.Lat, self.Long)
        for index, row in cities_df.iterrows():
            
            #normalizedDistance = self.distance_between_a_and_b(self.MilesKm, self.Lat, row['Latitude'], self.Long, row['Longitude'])
            dfCity = (row['Latitude'], row['Longitude'])
            normalizedDistance = haversine(userCity, dfCity)

            #keep track of smallest distance
            if normalizedDistance < smallestDistance:
                smallestDistance = normalizedDistance
                smallestIndex = index

        answer_df = cities_df.iloc[smallestIndex]
        print("City Found")
        print("The city is " + answer_df['Site'] + ", " + answer_df['State / Province'])
        print("The city number is " + str(answer_df['Index']))
        print("\nProgram Completed")


test = FindTheCity()
test.setFolderPath(r"C:\Users\Public\QGIS TESTING\QGIS Input Files\Step 1")




#mention how the lat needs to be within -90 and 90
test.setLatitude(46)
test.setLongitude(-84)

#if the user wants to go again, do not ask for the file path, just ask for lat, long, and miles
test.execute()