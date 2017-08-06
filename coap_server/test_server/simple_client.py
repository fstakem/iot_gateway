import logging
import asyncio

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
    protocol = await Context.create_client_context()

    request_1 = Message(code=GET, uri='coap://localhost/time')
    request_2 = Message(code=GET, uri='coap://localhost/other/separate')

    try:
        response_1 = await protocol.request(request_1).response
        response_2 = await protocol.request(request_2).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response_1.code, response_1.payload))
        print('Result: %s\n%r'%(response_2.code, response_2.payload))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())