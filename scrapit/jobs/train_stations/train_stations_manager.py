import pandas as pd
class TrainStationManager:
    def train_station_mange(self):
        train_stations = pd.read_csv(filepath_or_buffer='https://raw.githubusercontent.com/trainline-eu/stations/master/stations.csv',sep=';')