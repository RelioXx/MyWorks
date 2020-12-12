import asyncio
import time


pro_time = 0.05
rival_time = 0.55
max_moves = 60

async def move_pro(q_pro: asyncio.Queue, q_rivals: asyncio.Queue):
    while 1:
        board, move = await q_rivals.get()
        await asyncio.sleep(pro_time)
        move += 1
        print(f'Movimiento de pro: {move} hecho en partida {board}')
        await q_pro.put((board, move))
        q_rivals.task_done()

async def move_rival(q_pro: asyncio.Queue, q_rivals: asyncio.Queue, rival_id: int):
    while 1:
        board, move = await q_pro.get()
        if move >= max_moves:
            q_pro.task_done()
            return
        await asyncio.sleep(rival_time)
        move += 1
        print(f'Movimiento de rival: {move} hecho en partida {board}')
        await q_rivals.put((board, move))
        q_pro.task_done()



async def main():
    num_rivals = 24
    q_pro = asyncio.Queue()
    q_rivals = asyncio.Queue()

    for i in range(1, num_rivals + 1):
        await q_pro.put((i, 1))
    pro = asyncio.create_task(move_pro(q_pro, q_rivals))
    rivals = [asyncio.create_task(move_rival(q_pro, q_rivals, n)) for n in range(num_rivals)]

    await asyncio.gather(pro)
    print('Waiting for q...')
    await q_pro.join()
    await q_rivals.join()
    print('Q finished')


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(f'All orders dispatched in {time.time() - start:0.2f} seconds')