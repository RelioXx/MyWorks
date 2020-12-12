import rx

l = ['Hola', 'Adiós']
rx.from_(l).subscribe(
    on_next=lambda v: print(f'Recibido: {v}'),
    on_completed=lambda: print('Done!')
)
