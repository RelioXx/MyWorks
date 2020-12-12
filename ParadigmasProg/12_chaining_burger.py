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


async def prepare_meal(order: [str]) -> None:
    meal_start = time.time()
    print(f'Preparing meal with {order[0]} meat and {order[1]} extra')
    base = await prepare_meat(order[0])
    completed = await add_extra(order[1], base)
    print(f'Done menu: {completed} in {time.time() - meal_start:0.2f} seconds')

async def main():
    orders = [
        ['burger', 'cheese'],
        ['chicken burger', 'pickles'],
        ['veggie burger', 'cheese'],
    ]

    await asyncio.gather(*(prepare_meal(order) for order in orders))

if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(f'All orders dispatched in {time.time() - start:0.2f} seconds')