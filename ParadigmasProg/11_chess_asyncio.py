import asyncio
import time
import random

async def play_chess(id):
    for turn in range(30):
        print(f'Partida {id}, el profesional va a jugar el turno {turn}')
        await asyncio.sleep(0.005)
        print(f'Partida {id}, turno {turn} para el amateur')
        await asyncio.sleep(0.055)
    print(f'Ha terminado la partida {id}')
    return

async def main():
    nums = await asyncio.gather(*(play_chess(n) for n in range(24)))
    return [str(n) for n in nums]


t = time.time()
asyncio.run(main())
print(f'Tiempo de ejecución: {time.time() - t} segundos')