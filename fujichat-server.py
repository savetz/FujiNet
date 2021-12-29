#Chat server for fujichat
#Based on Echo TCP Server from
#https://www.mendrugory.com/post/python3-7-asyncio-chat/
#Creative Commons Attribution-NonCommercial 4.0 International License

import asyncio

writers = []

def forward(writer, addr, message):
    for w in writers:
        #if w != writer:
        #w.write(f"{addr}: {message}\n".encode())
        w.write(f"{message}\n".encode())

async def handle(reader, writer):
    writers.append(writer)
    addr = writer.get_extra_info('peername')
    message = f"{addr} connected"
    print(message)
    forward(writer, addr, message)
    while True:
        data = await reader.read(100)
        message = data.decode().strip()
        forward(writer, addr, message)
        await writer.drain()
        if message == "exit":
            message = f"{addr} wants to close the connection."
            print(message)
            forward(writer, "Server", message)
            break
    writers.remove(writer)
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle, '0.0.0.0', 8888)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()

asyncio.run(main())