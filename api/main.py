from flask import Flask, render_template
from graphs import pie_chart, most_recent_uses, avg_time_on
import os

path_to_directory = os.path.dirname(os.path.abspath(__file__))
filepath = f"{path_to_directory}/data.csv"

app = Flask(__name__)

@app.route('/')
def hello_world():
    pie_chart(filepath)
    last_five = most_recent_uses(filepath)
    avg_durations = avg_time_on(filepath)
    return render_template('home.html', last_five=last_five, avg_durations=avg_durations)


