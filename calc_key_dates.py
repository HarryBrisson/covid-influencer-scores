import math

import pandas as pd

from covid19_stats import *

def get_death_counts():
	files = [f'collect_1/data/wikidata_{t}.csv' for t in ['conflicts','disasters','massacres']]
	df = pd.DataFrame()
	for f in files:
		df = df.append(pd.read_csv(f),ignore_index=True)
	df = df[pd.to_numeric(df['deaths'],errors='coerce')>100]
	df = df.drop_duplicates('itemLabel')
	df['safeName'] = df['itemLabel'].str.replace(' ','')
	df = df.set_index('safeName')
	dates = df[['deaths','pointintime','itemLabel']].to_dict(orient='index')
	return dates

def get_estimated_date(currentdeathcount,event,growthrate):
	death_counts = get_death_counts()
	comparison_death_count = death_counts[event]['deaths']
	number_of_days = math.log(float(comparison_death_count)/float(currentdeathcount),growthrate)
	date_estimate = get_date_from_today(offset=number_of_days-1,fmt='%A %d %B %Y')
	return date_estimate

def get_comparisons():
	data = get_death_counts()
	return data.keys()
