# Autenticación con Twitter y seguimiento con Twitter Streaming API
from rx import create, operators
from tweepy import OAuthHandler, Stream, StreamListener

from textblob import TextBlob
from secret import consumer_key, access_token, consumer_secret, access_token_secret
from tkinter import *
import json

#'character U+1f1f9 is above the range (U+0000-U+FFFF) allowed by tcl'
def parse_tweet(t):
    username = t["user"]["name"] if 'user' in t else 'Anónimo'
    text = t["text"] if 'text' in t else ''

    # Para los que tengan un error del estilo:
    # character U+1f1f9 is above the range (U+0000-U+FFFF) allowed by tcl
    #username = ''.join([c for c in username if ord(c) < 65536])
    #text = ''.join([c for c in text if ord(c) < 65536])

    return {
        'text': f'{username}: {text}',
        'sentiment': TextBlob(text).sentiment.polarity
    }

def embed_tweet(tweet, text):
    if tweet['sentiment'] < -0.05:
        mood = 'negativo'
    elif tweet['sentiment'] > 0.05:
        mood = 'positivo'
    else:
        mood = 'neutral'
    text.insert(END, f'{tweet["text"]}\n', mood)

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
        stream.filter(track=keywords, is_async=True, languages=['en'])

    return create(observe_tweets)


class App:
    def __init__(self):
        self.__contador = 0
        self.window = Tk()
        self.window.title = 'Seguimiento de Twitter!'
        self.window.geometry('650x450')
        self.window.resizable(False, False)

        Label(text='Término de búsqueda').grid(column=0, row=0)

        Button(text='Buscar', width=35, command=self.searchButton).grid(column=0, row=1, columnspan=2)

        self.entry = Entry()
        # Forma alternativa con StringVar bindeando vista y modelo
        #self.val = StringVar()
        #self.entry = Entry(textvariable=self.val)
        self.entry.grid(column=1, row=0)

        self.txt = Text(bg='#ddd')
        self.txt.grid(row=2, column=0, columnspan=2)
        self.txt.tag_config('negativo', background='white', foreground='red')
        self.txt.tag_config('neutral', background='white', foreground='black')
        self.txt.tag_config('positivo', background='white', foreground='green')

        '''self.txt.insert(END, 'Primera línea\n', 'negativo')
        self.txt.insert(END, 'Segunda línea\n', 'neutral')
        self.txt.insert(END, 'Tercera línea\n', 'positivo')'''

        self.window.mainloop()

    def searchButton(self):
        mi_observable([self.entry.get()]).pipe(
            operators.map(lambda txt: json.loads(txt)),
            operators.map(lambda d: parse_tweet(d))
        ).subscribe(on_next=lambda t:embed_tweet(t, self.txt), on_error=lambda e: print(e))

if __name__ == '__main__':
    App()
