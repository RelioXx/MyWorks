import requests
import rx
from rx import from_, operators


class Printer(rx.core.Observer):
    def on_next(self, v):
        print(v)
    def on_completed(self):
        print('Terminado')
    def on_error(self,e):
        print(e)


params = {
    'apikey': '4d5b0373',
    's': input('Película a buscar')
}

content = requests.get(f'http://www.omdbapi.com/', params=params)

data = content.json()
from_(data['Search']).pipe(
    operators.filter(lambda t: t['Type'] == 'movie'),
    operators.map(lambda t: f'({t["imdbID"][2:]}) - {t["Title"]}: {t["Poster"]} ({t["Year"]})')
).subscribe(Printer())
