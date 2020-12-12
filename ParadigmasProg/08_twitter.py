# Autenticación con Twitter y seguimiento con Twitter Streaming API
from rx import create, operators
from tweepy import OAuthHandler, Stream, StreamListener

from printer import Printer
from secret import consumer_key, access_token, consumer_secret, access_token_secret
import json

def mi_observable(keywords):
    def observe_tweets(o, s):
        class TweetListener (StreamListener):
            def on_data(self, data):
                o.on_next(data)

            def on_error(self, status):
                o.on_error(status)

        listener = TweetListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, listener)
        stream.filter(track=keywords)

    return create(observe_tweets)


keywords = ['toque de queda']

mi_observable(keywords).pipe(
    operators.map(lambda txt: json.loads(txt)),
    operators.map(lambda d: f'{d["user"]["name"]}: {d["text"]}')
).subscribe(Printer())

