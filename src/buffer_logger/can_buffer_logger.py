import can
import asyncio
import zlib as zl
from multiprocessing import shared_memory
from buffer_logger.buffer_logger import BufferLogger
from numpy import array2string, empty, set_printoptions
from datetime import datetime


class CanBufferLogger(BufferLogger):
    ''' This class is being used to log all 'raw' can messages asychronously.
    '''

    def __init__(self, config, config_type):
        super().__init__(config, config_type)
        self.can_logging = self.config[
            self.config_type]['raw_can_data_logging']
        if(self.can_logging['enabled']):
            self.shared_list = None
            self.can_logging_buffer = self.can_logging['buffer']
            self.buffered_data = empty([self.can_logging_buffer],
                                       dtype=can.Message)
            set_printoptions(threshold=self.can_logging_buffer)

    def connect_to_network(self):
        ''' Listens to the configured channel, bustype and bitrate.

            Returns void.
        '''
        self.network = can.Bus(
            self.config[self.config_type]['channel'],
            bustype=self.config[self.config_type]['bustype'],
            bitrate=self.config[self.config_type]['bitrate'],
            receive_own_messages=True)

    async def listen_to_network(self):
        ''' Firstly, connects to network and creates async listener variables.
            Then initializes variables needed for to listen to the can
            messages. And later when while loop is cancelled then stop
            the listener.

            Returns void.
        '''
        self.connect_to_network()
        self._starting_async_listener()
        # Uses circular buffer implementation which overwrites
        # oldest index with new data once the buffer is full.
        index = 0
        buffer_full = False
        try:
            while True:
                can_msg = await self.reader.get_message()
                # Sleeps 0.1 seconds so doesn't try to read all messages
                # at once.
                await asyncio.sleep(0.1)
                self.buffered_data[index] = {
                    'timestamp': can_msg.timestamp,
                    'arbitration_id': can_msg.arbitration_id,
                    'data': (can_msg.data).hex(' '),
                    'channel': can_msg.channel}

                index = (index + 1) % self.can_logging_buffer
                if(index == 0):
                    # Buffer is now completely full with can messages.
                    buffer_full = True
                # At every n-th index update shared memory for HTTP server
                if (index % self.can_logging[
                            'shm_update_interval_threshold'] == 0):
                    # First close open shared memory
                    if(self.shared_list is not None):
                        self.shared_list.shm.close()
                        self.shared_list.shm.unlink()
                    # Skips None data
                    if(not buffer_full):
                        # Compresses buffered data
                        temp_buff_data = zl.compress(
                            str(self.buffered_data[:index].tolist(
                            )).encode('UTF-8'), 2)
                    else:
                        # Compresses buffered data
                        temp_buff_data = zl.compress(
                            str(self.buffered_data.tolist(
                            )).encode('UTF-8'), 2)
                    try:
                        # Try to share buffered data
                        self.shared_list = shared_memory.ShareableList(
                            [temp_buff_data], name='shm_buff_data')
                    except FileExistsError:
                        # Logs where still saved so needs to close first
                        temp_shm = shared_memory.ShareableList(
                            name='shm_buff_data')
                        temp_shm.shm.close()
                        temp_shm.shm.unlink()
                        self.shared_list = shared_memory.ShareableList(
                            [temp_buff_data], name='shm_buff_data')

        except KeyboardInterrupt:
            self._closing_async_listener()

    def release_memorized_messages(self):
        ''' Exports raw can data at once. When this triggered the raw can data
            with the size of the buffer is exported. This can be used when an
            error/malfunction is occuring.

            Returns void.
        '''

        self._log_data(array2string(self.buffered_data))

    def _log_data(self, message):
        log_file_name = datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + '.log'
        log_file_location = self.directory + log_file_name
        with open(log_file_location, 'w') as file:
            file.write(message)
        file.close()

    def _starting_async_listener(self):
        self.reader = can.AsyncBufferedReader()
        listeners = [self.reader]
        loop = asyncio.get_event_loop()
        self.notifier = can.Notifier(self.network, listeners,
                                     loop=loop)

    def _closing_async_listener(self):
        self.notifier.stop()
        self.network.shutdown()
