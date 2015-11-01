import tweepy
import json
from json import dumps
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from flask import Flask, make_response
import config

#app = Flask(__name__)

class StdOutListener(StreamListener):
    
    def on_data(self, data):
        print data
        return True
        
    def on_error(self, status):
        print status

if __name__ == '__main__':
    #app.run()
    
    l = StdOutListener()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    stream = Stream(auth, l)
    
    stream.filter(track=['Merkelmussweg'])
    """
api = tweepy.API(auth)

###@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
###
tweets=[]
for status in tweepy.Cursor(api.home_timeline).items(10):
        process_or_store(status.json)
        tweets.append(status.text)

@app.route('/')
def hello_world():
    a=[1,2,3]
    return make_response(dumps(tweets))
#    return a
#hello_world(a)

"""