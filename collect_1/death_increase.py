from argparse import ArgumentParser
from datetime import datetime, timedelta
import os
import pandas as pd
import requests
import sys

from collect_1.constants import COUNTRIES, DATA_DIR


def get_and_clean_data():
    """ Gets country deaths by day from API, filters to last week, cleans up country naming """
    historical = requests.get('https://corona.lmao.ninja/V2/historical')

    df = pd.json_normalize(historical.json(), sep='_')

    deaths = [c for c in df.columns if 'deaths' in c]
    df = pd.melt(df, 'country', deaths, 'date', 'deaths')
    df['date'] = pd.to_datetime(df['date'].str.replace('timeline_deaths_', ''))

    week_ago = pd.Timestamp((datetime.today() - timedelta(days=8)).date())  # adding 8 because today's data obviously not in yet
    df = df[df['date'] >= week_ago]

    country_map = {c.lower(): c for c in COUNTRIES}
    addtl_countries = {'kosovo': 'Serbia', 'cote d\'ivoire': 'Cote d\'Ivoire',
                       'burma': 'Myanmar', 'holy see': 'Vatican City'}

    df['country'] = df['country'].str.replace('\*| \(.+', '', regex=True) \
                                 .map({**country_map, **addtl_countries})

    return df


def get_last_seven_days_avg_increase(country=None):
    """Calculates the average rate of daily increase.  Can optionally filter by country.

    Args:
        country (str): Name of country.  Defaults to None

    Returns:
        DataFrame: Rate of daily increase in past 7 days by country

    Raises:
        ValueError: if country cannot be found
    """

    if country and country not in COUNTRIES:
        raise ValueError('f{country} is not a valid option--perhaps it is misspelled?')

    deaths = get_and_clean_data()

    if country:
        deaths = deaths[deaths['country'] == country]

    deaths = deaths.groupby(['country', 'date'], as_index=False)['deaths'].sum()
    deaths['increase'] = (deaths['deaths'] - deaths['deaths'].shift()) / deaths['deaths']
    deaths = deaths.groupby('country')['increase'].mean().reset_index()

    return deaths


def parse_args(args):
    parser = ArgumentParser()
    parser.add_argument('--country', required=False,
                        help='Name of country to analyze.'
                             'Defaults to None, meaning '
                             'analysis will include all countries')

    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    deaths = get_last_seven_days_avg_increase(args.country)

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    deaths.to_csv(os.path.join(DATA_DIR, 'avg_deaths.csv'), index=False)
