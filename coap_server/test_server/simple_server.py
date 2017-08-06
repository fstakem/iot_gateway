import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap


class BlockResource(resource.Resource):
    """
    Example resource which supports GET and PUT methods. It sends large
    responses, which trigger blockwise transfer.
    """

    def __init__(self):
        super(BlockResource, self).__init__()
        self.content = ("This is the resource's default content. It is padded "\
                "with numbers to be large enough to trigger blockwise "\
                "transfer.\n" + "0123456789\n" * 100).encode("ascii")

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.content = request.payload
        payload = ("I've accepted the new payload. You may inspect it here in "\
                "Python's repr format:\n\n%r"%self.content).encode('utf8')
        return aiocoap.Message(payload=payload)


class SeparateLargeResource(resource.Resource):
    """
    Example resource which supports GET method. It uses asyncio.sleep to
    simulate a long-running operation, and thus forces the protocol to send
    empty ACK first.
    """

    def __init__(self):
        super(SeparateLargeResource, self).__init__()

    async def render_get(self, request):
        await asyncio.sleep(3)

        payload = "Three rings for the elven kings under the sky, seven rings"\
                "for dwarven lords in their halls of stone, nine rings for"\
                "mortal men doomed to die, one ring for the dark lord on his"\
                "dark throne.".encode('ascii')
        return aiocoap.Message(payload=payload)

class TimeResource(resource.ObservableResource):
    """
    Example resource that can be observed. The `notify` method keeps scheduling
    itself, and calles `update_state` to trigger sending notifications.
    """
    def __init__(self):
        super(TimeResource, self).__init__()

        self.notify()

    def notify(self):
        self.updated_state()
        asyncio.get_event_loop().call_later(6, self.notify)

    def update_observation_count(self, count):
        if count:
            print("Keeping the clock nearby to trigger observations")
        else:
            print("Stowing away the clock until someone asks again")

    async def render_get(self, request):
        payload = datetime.datetime.now().strftime("%Y-%m-%d %H:%M").encode('ascii')
        return aiocoap.Message(payload=payload)

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    root = resource.Site()
    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('time',), TimeResource())
    root.add_resource(('other', 'block'), BlockResource())
    root.add_resource(('other', 'separate'), SeparateLargeResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()