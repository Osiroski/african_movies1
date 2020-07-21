import tweepy
import os
import time
import logging
from config import create_api
import time
import requests
from scraper import get_title
import pandas as pd
import random


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def message(url):
    titles=get_title(url)
    title_url='http://www.omdbapi.com/?i=tt3896198&apikey=75015db4&t='+random.choice(titles)
    page = requests.get(title_url).json()
    return page

def tweet_image(url, post):
    api = create_api()
  
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status=post)
        os.remove(filename)
    else:
        print("Unable to download image")

def main():
    interval=60 * 60 * 4
    
    while True:
        countries=pd.read_csv('countries.csv')
        countries=countries['2-Letter'].to_list()
        country=random.choice(countries)
        country_url='https://www.imdb.com/search/title/?countries='+country+'&count=250'
        page=message(country_url)
        if 'Error' in page.keys():
            logger.info("Title not available. Restarting....")
            message(country_url)
        elif page['Poster']=='N/A':
            logger.info("Poster not available. Restarting....")
            main()
        else: 
            logger.info(f" Message {page['Poster']}")
            post = 'Movie Review 🍱🌟\n'+page['Title']+'\n'+page['Plot']
            tweet_image(page['Poster'], post)
            time.sleep(interval)

if __name__ == "__main__":
    main()
