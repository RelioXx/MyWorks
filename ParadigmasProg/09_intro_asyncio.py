import asyncio
import time
async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

async def main():
    await asyncio.gather(count(), count(), count())

t = time.time()
asyncio.run(main())
print(f'Tiempo de ejecución: {time.time() - t} segundos')