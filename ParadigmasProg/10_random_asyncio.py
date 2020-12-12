import asyncio
import time
import random

async def generate_random(id):
    threshold = 8
    num = random.randint(1,10)
    while num < threshold:
        print(f'La tarea {id} ha fallado al obtener el número {num}')
        await asyncio.sleep(1)
        num = random.randint(1,10)
    print(f'La tarea {id} ha terminado con el resultado {num}')
    return num

async def main():
    nums = await asyncio.gather(*(generate_random(n) for n in range(100)))
    return [str(n) for n in nums]


t = time.time()
resultados = asyncio.run(main())


print(f'Resultados: {", ".join(resultados)}')
print(f'Tiempo de ejecución: {time.time() - t} segundos')