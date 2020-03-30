
import json

from flask import Flask, request, render_template

from covid19_stats import *
from calc_key_dates import *


app = Flask(__name__)

@app.route('/')
def main():

	country = request.args.get('country')
	event = request.args.get('event')

	if country == None:
		country='all'
	if event == "None":
		event = None

	increase_rate = get_death_daily_increase_rate(country=country)
	current_deathcount = get_yesterdays_deathcount(country=country)
	events = get_death_counts()

	print(event)

	if event:
		date = get_estimated_date(current_deathcount,event,increase_rate)
	else:
		date = None

	print(date)

	html = render_template('main.html',events=events, event=event, increase_rate=increase_rate, date=date, country=country)
	return(html)



if __name__ == '__main__':
	app.run(debug=True)