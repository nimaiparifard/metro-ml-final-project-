import numpy as np
from station import Station
import datetime
import matplotlib.pyplot as plt
import networkx as nx

class Metro:
    def __init__(self) -> None:
        self.stations_list = []
        # Defining stations from the end of each line towards the beginning
        # Exit Stations
        kahrizak = Station('Kahrizak', input_rate_range=(0, 0), output_rate_range=None, children=[], is_last_station=True)
        basij = Station('Basij', input_rate_range=(0, 0), output_rate_range=None, children=[], is_last_station=True)
        ghaem = Station('Ghaem', input_rate_range=(0, 0), output_rate_range=None, children=[], is_last_station=True)
        buali = Station('BuAli', input_rate_range=(0, 0), output_rate_range=None, children=[], is_last_station=True)
        
        # Common and Normal Stations (defined in reverse order to correctly assign children)
        # Line 1
        mohammadiye = Station('Mohammadiye', input_rate_range=(10, 14), output_rate_range=(15, 20), children=[kahrizak])
        dowlat = Station('Dowlat', input_rate_range=(10, 14), output_rate_range=(15, 20), children=[mohammadiye])
        beheshti = Station('Beheshti', input_rate_range=(10, 14), output_rate_range=(15, 20), children=[dowlat])  # Shared with Line 3
        shariati = Station('Shariati', input_rate_range=(10, 14), output_rate_range=(8, 12), children=[beheshti])
        tajrish = Station('Tajrish', input_rate_range=(30, 40), output_rate_range=(0, 0), children=[shariati], is_first_station=True)
        
        # Line 2
        molavi = Station('Molavi', input_rate_range=(10, 14), output_rate_range=(8, 12), children=[basij])
        # Mohammadiye already defined, add Molavi as a child
        mohammadiye.children.append(molavi)
        teatr = Station('Teatr', input_rate_range=(10, 14), output_rate_range=(15, 20), children=[mohammadiye])  # Shared with Line 4
        valiasr = Station('Valiasr', input_rate_range=(10, 14), output_rate_range=(15, 20), children=[teatr])  # Shared with Line 3
        sanat = Station('Sanat', input_rate_range=(30, 40), output_rate_range=(0, 0), children=[valiasr], is_first_station=True)
        
        # Line 3
        heravi = Station('Heravi', input_rate_range=(10, 14), output_rate_range=(8, 12), children=[ghaem])
        # Beheshti already defined, add Heravi as a child
        beheshti.children.append(heravi)
        jihad = Station('Jihad', input_rate_range=(10, 14), output_rate_range=(8, 12), children=[beheshti])
        # Valiasr already defined, add Jihad as a child
        valiasr.children.append(jihad)
        sattari = Station('Sattari', input_rate_range=(30, 40), output_rate_range=(0, 0), children=[valiasr], is_first_station=True)
        
        # Line 4
        shemiran = Station('Shemiran', input_rate_range=(10, 14), output_rate_range=(8, 12), children=[buali])
        ferdowsi = Station('Ferdowsi', input_rate_range=(10, 14), output_rate_range=(8, 12), children=[shemiran])
        # Teatr already defined, add Ferdowsi as a child
        teatr.children.append(ferdowsi)
        azadi = Station('Azadi', input_rate_range=(30, 40), output_rate_range=(0, 0), children=[teatr], is_first_station=True)
        
    
        # Store all stations in a list or dictionary for further processing if needed
        self.stations = {
            'Kahrizak': kahrizak, 'Basij': basij, 'Ghaem': ghaem, 'BuAli': buali,
            'Mohammadiye': mohammadiye, 'Dowlat': dowlat, 'Beheshti': beheshti,
            'Shariati': shariati, 'Tajrish': tajrish, 'Molavi': molavi, 'Teatr': teatr,
            'Valiasr': valiasr, 'Sanat': sanat, 'Heravi': heravi, 'Jihad': jihad,
            'Sattari': sattari, 'Shemiran': shemiran, 'Ferdowsi': ferdowsi, 'Azadi': azadi
        }

        for station_name, station_object in self.stations.items():
            self.stations_list.append(station_object)

        self.lines = {
            'Line 1': ['Tajrish', 'Shariati', 'Beheshti', 'Dowlat', 'Mohammadiye', 'Kahrizak'],
            'Line 2': ['Sanat', 'Valiasr', 'Teatr', 'Mohammadiye', 'Molavi', 'Basij'],
            'Line 3': ['Sattari', 'Valiasr', 'Jihad', 'Beheshti', 'Heravi', 'Ghaem'],
            'Line 4': ['Azadi', 'Teatr', 'Ferdowsi', 'Dowlat', 'Shemiran', 'BuAli'],
        }

    def create_metro_graph(self):
        metro_structure = {
            'Kahrizak': [],
            'Basij': [],
            'Ghaem': [],
            'BuAli': [],
            'Mohammadiye': ['Kahrizak', 'Molavi'],
            'Dowlat': ['Mohammadiye'],
            'Beheshti': ['Dowlat', 'Heravi'],
            'Shariati': ['Beheshti'],
            'Tajrish': ['Shariati'],
            'Molavi': ['Basij'],
            'Teatr': ['Mohammadiye', 'Ferdowsi'],
            'Valiasr': ['Teatr', 'Jihad'],
            'Sanat': ['Valiasr'],
            'Heravi': ['Ghaem'],
            'Jihad': ['Beheshti'],
            'Sattari': ['Valiasr'],
            'Shemiran': ['BuAli'],
            'Ferdowsi': ['Shemiran'],
            'Azadi': ['Teatr'],
        }
        # Create a directed graph from the metro structure
        G = nx.DiGraph(metro_structure)
        pos = nx.kamada_kawai_layout(G)

        plt.figure(figsize=(18, 10))
        nx.draw(G, pos, with_labels=True, node_size=2500, node_color='skyblue', font_size=10, font_weight='bold', arrowstyle='-|>', arrowsize=12)
        plt.title('Metro Station Structure (Improved Layout)')
        plt.axis('off')  # Turn off the axis for a cleaner look
        plt.show()



    def metro_simulation_one_day(self):
        # Start time: 6 AM on 1st Jan 2024
        start_time = datetime.datetime(2024, 1, 1, 6, 0)
        # End time: 10 PM on the same day
        end_time = datetime.datetime(2024, 1, 1, 22, 0)
        
        # Current simulation time
        timestamp = start_time
        
        while timestamp <= end_time:
            print(f"Simulating for time: {timestamp}")  # Placeholder for simulation steps
            
            # Loop through each line in sequence
            for line_name, stations in self.lines.items():  # Assuming self.lines is defined in __init__
                print(f"Processing {line_name}")  # Placeholder for line processing
                
                for station_name in stations:
                    station = self.stations[station_name]
                    # Simulate passenger flow at this station
                    station.passengers_flow(timestamp)
                    print(f"Simulated passengers flow at {station.name}")  # Placeholder for actual simulation
                    
            # Increment timestamp by 6 minutes
            timestamp += datetime.timedelta(minutes=6)
            
        print("Simulation complete.")


cursed_metro = Metro()
cursed_metro.create_metro_graph()
cursed_metro.metro_simulation_one_day()