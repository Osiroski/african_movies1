import tweepy
import logging
import credentials
from os impro environ

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def create_api():
   
    auth = tweepy.OAuthHandler(environ['CONSUMER_KEY'], environ['CONSUMER_SECRET'])
    auth.set_access_token(environ['ACCESS_TOKEN'], environ['ACCESS_SECRET'])
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
