import asyncio
import time


async def prepare_meat(meat_type: str) -> str:
    print(f'\tCooking {meat_type}...')
    await asyncio.sleep(3)
    print(f'\tDone cooking {meat_type}!')
    return meat_type

async def add_extra(extra: str, base: str) -> str:
    print(f'\tAdding extra {extra} to {base}...')
    await asyncio.sleep(1)
    print(f'\tDone preparing extra {extra}!')
    return f'{base} with {extra}'


async def chef_lifecycle(id: int, q: asyncio.Queue) -> None:
    while 1:
        order = await q.get()
        meal_start = time.time()
        print(f'Preparing meal with {order[0]} meat and {order[1]} extra')
        base = await prepare_meat(order[0])
        completed = await add_extra(order[1], base)
        print(f'Done menu: {completed} in {time.time() - meal_start:0.2f} seconds')
        q.task_done()


async def generate_order(id: int, q: asyncio.Queue) -> None:
    dishes = [
        ['burger', 'cheese'],
        ['chicken burger', 'pickles'],
        ['veggie burger', 'cheese'],
    ]

    for dish in dishes:
        await q.put(dish)
        print(f'Order with id {id} added {dish} to queue')


async def main():

    num_producers = 1
    num_consumers = 1

    q = asyncio.Queue()

    producers = [asyncio.create_task(generate_order(n, q)) for n in range(num_producers)]
    consumers = [asyncio.create_task(chef_lifecycle(n, q)) for n in range(num_consumers)]

    await asyncio.gather(*producers)
    print('Waiting for q...')
    await q.join()
    print('Q finished')

    for c in consumers:
        c.cancel()


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(f'El torneo ha terminado en {time.time() - start:0.2f} segundos')
