import asyncio
import time


pro_time = 0.05
rival_time = 0.55
max_moves = 30
num_rivals = 24

async def move_pro(player_q: asyncio.Queue, qs: [asyncio.Queue]):
    while 1:
        game_info = await player_q.get()
        board = game_info['board']
        turn = game_info['turn'] + 1

        print(f'Partida {board}, el jugador está pensando el turno {turn}')
        await asyncio.sleep(pro_time)
        print(f'Partida {board}, el jugador ha ejecutado el turno {turn}')
        await qs[board - 1].put({'turn': turn, 'board': board})
        player_q.task_done()

async def move_rival(q: asyncio.Queue, player_q: asyncio.Queue):
    while 1:
        board_info = await q.get()
        board = board_info['board']
        turn = board_info['turn']
        print(f'Partida: {board}, rival pensando el turno {turn}')
        await asyncio.sleep(rival_time)
        print(f'Partida: {board}, rival ha ejecutado el movimiento {turn}')
        q.task_done()
        if turn < max_moves:
            await player_q.put(board_info)
        else:
            return
        #print(q.qsize())

async def main():
    qs = [asyncio.Queue() for _ in range(num_rivals)]
    player_q = asyncio.Queue()

    for i in range(num_rivals):
        await player_q.put({'board': i + 1, 'turn': 0})

    pro = asyncio.create_task(move_pro(player_q, qs))
    rivals = [asyncio.create_task(move_rival(q, player_q)) for q in qs]

    await asyncio.gather(*rivals)

    await player_q.join()
    for q in qs:
        await q.join()
        
    '''for r in rivals:
        r.cancel()

    pro.cancel()'''




if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(f'All orders dispatched in {time.time() - start:0.4f} seconds')