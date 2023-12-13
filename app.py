from flask import Flask, render_template, url_for, request, redirect
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from scraper import scrape_comments
import re
from model import predict
import matplotlib.pyplot as plt
import os
import base64
from io import BytesIO
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)

def url_validation(url):
    regexp = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$"
    if re.match(regexp, url):
        return True
    else:
        return False

def create_plot(predictions):
    counts = [(predictions == "negative").sum(), (predictions == "positive").sum()]
    labels = ['negative', 'positive']
    colors = ['#2B474B','#9AC8F7']

    fig = go.Figure(data=[go.Pie(labels=labels, values=counts, marker_colors=colors)])
    fig.update_traces(textinfo='percent+label', hole=.3, hoverinfo="label+percent+name")

    plot_url = pio.to_html(fig, full_html=False, default_height='500px', default_width='500px')

    return plot_url

@app.route("/", methods=["GET", "POST"])

def index():
    if request.method == "POST":
        youtube_url = request.form.get("url_input")
        if url_validation(youtube_url):
            scraped_comments = scrape_comments(youtube_url)
            predictions = predict(list(scraped_comments['Comment']))
            print(predictions)
            plot_url = create_plot(predictions)

            return render_template('subpage.html', comments=scraped_comments, predictions=predictions, plot_url=plot_url, url=youtube_url)
        else:
            return render_template('index.html', error_message='Please provide a valid YouTube URL.')
    return render_template('index.html')

@app.route("/subpage", methods=["GET", "POST"])
def subpage():
    return render_template('subpage.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
