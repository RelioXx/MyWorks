import rx

def generador (o, s):
    o.on_next('Hola')
    o.on_next('Adiós')
    o.on_complete()

rx.create(generador).subscribe(lambda v: print(f'Recibido: {v}'))


#######
