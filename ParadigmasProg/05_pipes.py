'''

from printer import Printer
from secret import consumer_key, access_token, consumer_secret, access_token_secret
import json

class receiver(rx.core.Observer):
    def on_next(self, v):
        print(v)##recibir imagen
    def on_completed(self):
        print('Terminado')
    def on_error(self,e):
        print(e)

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
'''

####

class receiver(rx.core.Observer):
    def on_next(self, v):
        print(v)##recibir imagen
    def on_completed(self):
        print('Terminado')
    def on_error(self,e):
        print(e)

def f1(txt):
    print(txt)
    list1 = ["Dead", "Die" , "Jotaro", "joline"]

    def retrievedata():
        class TweetListener(StreamListener):
            def on_data(self, data):
                o.on_next(data)

            def on_error(self, status):
                o.on_error(status)

    return create(retrievedata)


def f2():
    return "f2"

from rx import of, operators
f1("Ey que tal gente").pipe(
    operators.map(lambda s: s.upper()),
    operators.map(lambda s: f'En mayúscula: {s}')
).subscribe(lambda v: print(f'Recibido: {v}'))

####
'''

from rx import of, operators
of('Hola', 'Adiós').pipe(
    operators.map(lambda s: s.upper()),
    operators.map(lambda s: f'En mayúscula: {s}')
).subscribe(lambda v: print(f'Recibido: {v}'))

'''