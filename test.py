import sys
import csv
from datetime import datetime
import pandas as pd
from graphs import avg_time_on

path_to_directory = "/Users/jakehopkins/Downloads/mqtt_test"
filepath = f"{path_to_directory}/data.csv"

# def most_recent_uses(filepath):
#     data = pd.read_csv(filepath) #pandas reads csv file
#     last_five = data.tail(5) # only keeps last five rows
#     print(last_five)#prints the last five
#     return last_five
# most_recent_uses(filepath)
avg_time_on(filepath)
