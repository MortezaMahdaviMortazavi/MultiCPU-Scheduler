import threading
import time
from cpu import CPU
from process import Process , ProcessGenerator
from queue import Queue
from typing import Optional

class CPU:
    def __init__(self, ready_queue: Queue):
        self.id = id(self)  # Unique identifier for the CPU instance
        self.current_process: Optional[Process] = None
        self.is_busy = False
        self.mutex = threading.Lock()
        self.ready_queue = ready_queue

    def execute_process(self, process: Process):
        """
        Executes the given process, ensuring it adheres to execution time and deadlines.
        """
        with self.mutex:
            self.is_busy = True
            self.current_process = process

        print(f"CPU {self.id}: Starting execution of {process}")

        start_time = time.time()
        time.sleep(min(process.execution_time, process.get_remaining_time(int(start_time))))  # Simulate execution
        end_time = time.time()

        if end_time - start_time >= process.execution_time:
            print(f"CPU {self.id}: Process {process.id} executed successfully.")
        else:
            print(f"CPU {self.id}: Process {process.id} could not complete before the deadline.")

        with self.mutex:
            self.is_busy = False
            self.current_process = None

    def run(self):
        """
        Continuously fetch and execute processes from the ready queue.
        """
        while True:
            process = self.ready_queue.get()  # Fetch process from the queue (blocking operation)

            if process is None:  # Sentinel value to stop the CPU thread
                print(f"CPU {self.id}: Shutting down.")
                break

            current_time = int(time.time())
            if process.is_expired(current_time):
                print(f"CPU {self.id}: Skipping expired process {process.id}.")
                continue

            self.execute_process(process)