import asyncio
import can

def print_message(msg):
    """Regular callback function. Can also be a coroutine."""
    print(msg)

async def main():
    can0 = can.Bus('vcan0', bustype='socketcan', receive_own_messages=True)
    reader = can.AsyncBufferedReader()

    listeners = [
        print_message,  # Callback function
        reader         # AsyncBufferedReader() listener
    ]

    # Create Notifier with an explicit loop to use for scheduling of callbacks
    loop = asyncio.get_event_loop()
    notifier = can.Notifier(can0, listeners, loop=loop)

    print('Bouncing 10 messages...')
    while True:
        # Wait for next message from AsyncBufferedReader
        msg = await reader.get_message()
        # Delay response
        await asyncio.sleep(0.5)
    # Wait for last message to arrive
    await reader.get_message()
    print('Done!')

    # Clean-up
    notifier.stop()
    can0.shutdown()

# Get the default event loop
loop = asyncio.get_event_loop()
# Run until main coroutine finishes
loop.run_until_complete(main())
loop.close()
