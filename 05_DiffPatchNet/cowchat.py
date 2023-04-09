import asyncio
import cowsay
import shlex

clients = {}
cowsToPeers = {}
peersToCows = {}

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], 
return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                match shlex.split(q.result().decode()):
                    case ["who"]:
                        if me not in cowsToPeers.values():
                            await clients[me].put(f"You are not able to write until 
registration!")
                        else:
                            peersCowsString = ",".join(list(cowsToPeers.keys()))
                            await clients[me].put(f"{peersCowsString}")
                    case ["cows"]:
                        if me not in cowsToPeers.values():
                            await clients[me].put(f"You are not able to write until 
registration!")
                        else:
                            await clients[me].put(f"{[cow for cow in cowsay.list_cows() if 
cow not in cowsToPeers]}")
                    case ["login", cow]:
                        if cow in cowsay.list_cows():
                            if cow in cowsToPeers:
                                await clients[me].put("This name is already taken :(")
                            else:
                                cowsToPeers[cow] = me
                                peersToCows[me] = cow
                        else:
                            await clients[me].put("Bad cow name :(")
                    case ["say", cow, *text]:
                        if me not in cowsToPeers.values():
                            await clients[me].put(f"You are not able to write until 
registration!")
                        else:
                            if cow in cowsToPeers:
                                await 
clients[cowsToPeers[cow]].put(cowsay.cowsay("".join(text), cow=peersToCows[me]))
                            else:
                                await clients[me].put("There's no cow with this name")
                    case ["yield", *text]:
                        if me not in cowsToPeers.values():
                            await clients[me].put(f"You are not able to write until 
registration!")
                        else:
                            for cow in cowsToPeers:
                                if cowsToPeers[cow] != me:
                                    await 
clients[cowsToPeers[cow]].put(cowsay.cowsay("".join(text), cow=peersToCows[me]))
                    case ["quit"]:
                        cow = peersToCows[me]
                        peersToCows.pop(me)
                        cowsToPeers.pop(cow)
                        send.cancel()
                        receive.cancel()
                        del clients[me]
                        writer.close()
                        await writer.wait_closed()
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1234)
    async with server:
        await server.serve_forever()

asyncio.run(main())
