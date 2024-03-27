# Time distribution and handling task

from hal.pycubed import hardware
from tasks.template_task import DebugTask

import time


class Task(DebugTask):

    name = 'TIME'
    ID = 0x01
    

    async def main_task(self):
        print(f'[{self.ID}][{self.name}] Temp.')

