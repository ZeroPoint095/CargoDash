import can
import logging
import asyncio
from buffer_logger.buffer_logger import BufferLogger
from numpy import array2string, empty, set_printoptions
from datetime import datetime


class CanOpenBufferLogger(BufferLogger):

    def __init__(self, config, config_type):
        super().__init__(config, config_type)
        can_logging = self.config[self.config_type]['raw_can_data_logging']
        if(can_logging['enabled']):
            # Creates new network connection because CANopen library has
            # difficulties with multithreading on a single network connection.
            self.can_logging_buffer = can_logging['buffer']
            self.buffered_data = empty([self.can_logging_buffer],
                                       dtype=can.Message)
            set_printoptions(threshold=self.can_logging_buffer)
    
    async def listen_to_network(self):
        can0 = can.Bus(
            self.config[self.config_type]['channel'],
            bustype=self.config[self.config_type]['bustype'],
            receive_own_messages=True) 
        self.reader = can.AsyncBufferedReader()
        listeners = [self.reader]
        loop = asyncio.get_event_loop()
        notifier = can.Notifier(can0, listeners, loop=loop)
        # Uses circular buffer implementation which overwrites
        # oldest index with new data once the buffer is full.
        index = 0
        while True:
            can_msg = await self.reader.get_message()
            await asyncio.sleep(0.5)
            index = (index + 1) % self.can_logging_buffer
            self.buffered_data[index] = can_msg
            print(index)
        await self.reader.get_message()
        notifier.stop()
        can0.shutdown()

    def release_memorized_messages(self):
        ''' Exports raw can data at once. When this triggered the raw can data
            with the size of the buffer is exported. This can be used when an
            error/malfunction is occuring.

            Returns void.
        '''

        self._log_data(array2string(self.buffered_data))

    def _log_data(self, message):
        log_file_name = datetime.now().strftime('%d-%m-%Y-%H:%M:%S') + '.log'
        log_file_location = self.directory + log_file_name
        with open(log_file_location, 'w') as file:
            file.write(message)
        file.close()
