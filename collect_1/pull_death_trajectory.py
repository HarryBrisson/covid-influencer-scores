import requests

def get_historical_data():
	r = requests.get('https://corona.lmao.ninja/v2/historical/')
	return r.json()

def get_death_daily_increase_rate(country=None):
	# eventually will have a calculation that pulls from historical data
	return .3