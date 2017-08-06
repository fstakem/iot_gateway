# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    8.5.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
import logging
import asyncio

from aiocoap import *


logging.basicConfig(level=logging.INFO)


async def push_data(protocol):
    payload = b'10'
    request = Message(code=PUT, uri='coap://localhost/device/1/sensor/1', payload=payload)

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Push data result: %s' % (response.code))

async def get_tx_rate(protocol):
    request = Message(code=GET, uri='coap://localhost/device/1/sensor/1')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Get tx rate result: %s' % (response.code))
        print('\t%r' % (response.payload))


async def main():
    protocol = await Context.create_client_context()

    for i in range(10):
        await push_data(protocol)

    await get_tx_rate(protocol)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())