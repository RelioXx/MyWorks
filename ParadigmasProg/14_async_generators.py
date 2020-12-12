import asyncio

async def cuadrados():
    for i in range(10):
        pass
        yield i ** 2
        await asyncio.sleep(0.1)  # Operación de IO que tarda

async def main():
    r1 = [i async for i in cuadrados()]
    r2 = [i for i in [1,2,3]]
    print(r1)
    print(r2)


if __name__ == '__main__':
    asyncio.run(main())
