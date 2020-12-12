import rx

class Printer(rx.core.Observer):
    def on_next(self, v):
        print(f'Recibido: {v}')

    def on_completed(self):
        print('Terminado')

def observer_teclado(o, s):
    while 1:
        msg = input('Introduce algo:')
        if msg:
            o.on_next(msg)
        else:
            o.on_completed()
            return

rx.create(observer_teclado).subscribe(Printer())
