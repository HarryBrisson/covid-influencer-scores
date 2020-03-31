import math

import pandas as pd

from covid19_stats import *

def get_death_counts():
	df = pd.read_csv('collect_1/data/death_stats.csv')
	df = df.set_index('safeName')
	dates = df[['deaths','pointintime','itemLabel']].to_dict(orient='index')
	return dates

def get_estimated_date(currentdeathcount,event,growthrate):
	death_counts = get_death_counts()
	comparison_death_count = death_counts[event]['deaths']
	number_of_days = math.log(float(comparison_death_count)/float(currentdeathcount),growthrate)
	date_estimate = get_date_from_today(offset=number_of_days-1,fmt='%A %d %B %Y')
	return date_estimate

def get_growth_trajectory(currentdeathcount,event,growthrate):
	death_counts = get_death_counts()
	comparison_death_count = death_counts[event]['deaths']
	number_of_days = math.log(float(comparison_death_count)/float(currentdeathcount),growthrate)
	trajectory = []
	deathcount = currentdeathcount
	for d in range(int(number_of_days)+1):
		deathcount = deathcount*growthrate
		row = {
			'date': get_date_from_today(offset=d,fmt='%A %d %B %Y'),
			'deaths': deathcount
			}
		trajectory.append(row)
	return trajectory

def get_comparisons():
	data = get_death_counts()
	return data.keys()
