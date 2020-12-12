import asyncio
import time


pro_time = 0.01
rival_time = 0.9
max_moves = 60
num_rivals = 24

async def move_pro(qs: [asyncio.Queue]):
    for turn in range(1, 31):
        for i, q in enumerate(qs):
            print(f'Partida: {i} pro pensando su turno {turn}')
            await asyncio.sleep(pro_time)
            await q.put({'turn': turn, 'board': i})

async def move_rival(q: asyncio.Queue):
    while 1:
        board_info = await q.get()
        board = board_info['board']
        turn = board_info['turn']
        print(f'Partida: {board}, rival pensando el turno {turn}')
        await asyncio.sleep(rival_time)
        q.task_done()
        #print(q.qsize())

async def main():
    qs = [asyncio.Queue() for _ in range(num_rivals)]

    pro = asyncio.create_task(move_pro(qs))
    rivals = [asyncio.create_task(move_rival(q)) for q in qs]

    await asyncio.gather(pro)
    for q in qs:
        await q.join()

    for r in rivals:
        r.cancel()




if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(f'All orders dispatched in {time.time() - start:0.2f} seconds')