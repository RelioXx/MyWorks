import rx

rx.of('Hola', 'Adiós').subscribe(
    on_next=lambda v: print(f'Recibido: {v}'),
    on_completed=lambda: print('Done!')
)
