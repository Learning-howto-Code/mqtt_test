import csv
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import datetime
from datetime import datetime
matplotlib.use('Agg') #doesn't create pop-p for flask

path_to_directory = "/Users/jakehopkins/Downloads/mqtt_test"
filepath = f"{path_to_directory}/data.csv"

def pie_chart(filepath):
    room_counts = Counter()

    with open(filepath, 'r', newline='') as file: #iterates through csv, gets str from column, increases counter for that counter
        reader = csv.DictReader(file)
        for row in reader:
            room = row['room'].strip()
            if room:
                room_counts[room] += 1

    labels = list(room_counts.keys())
    sizes = list(room_counts.values())

    print("Room counts:")
    for label, size in zip(labels, sizes):
        print(f"{label}: {size}")

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Room Usage Frequency')
    plt.savefig('static/pie_chart.png')
    plt.close
def most_recent_uses(filepath):
    data = pd.read_csv(filepath) #pandas reads csv file

    last_five = data.tail(5) # only keeps last five rows
    last_five = last_five.to_dict(orient='records')  # Convert to list of dicts
    
    for entry in last_five: # iterates throug list, removes dates and changes to 12 hour time
        entry['time_on'] = datetime.strptime(entry['time_on'], "%Y-%m-%d %H:%M:%S").strftime("%I:%M:%S %p")
        entry['time_off'] = datetime.strptime(entry['time_off'], "%Y-%m-%d %H:%M:%S").strftime("%I:%M:%S %p")
    print(last_five)#prints the last five 
    return last_five
def avg_time_on(filepath):

    df = pd.read_csv('data.csv', parse_dates=['time_on', 'time_off']) #creates pandas data frame with time on and off axis's
    df['duration'] = (df['time_off'] - df['time_on']).dt.total_seconds() #calculates how long each entry is on for
    avg_durations = df.groupby('room')['duration'].mean().reset_index() #averges data fram using mean funtion
    avg_durations['duration'] = avg_durations['duration'].apply(lambda x: round(x, 1)) #rounds averages to one digit after decimal

    print(avg_durations)
    return avg_durations.to_dict(orient='records') # chagnes data shape from pandas df to dictionary



