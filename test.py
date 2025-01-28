import threading
import time
import random
from queue import Queue
from typing import Optional
from dataclasses import dataclass

@dataclass
class Process:
    id: int
    arrival_time: int
    execution_time: int
    starting_deadline: int
    ending_deadline: int
    value: int

    def get_remaining_time(self, current_time: int) -> int:
        return self.ending_deadline - current_time

    def is_expired(self, current_time: int) -> bool:
        return current_time > self.starting_deadline or current_time > self.ending_deadline

    def __str__(self) -> str:
        return (f"Process(id={self.id}, arrival_time={self.arrival_time}, "
                f"execution_time={self.execution_time}, starting_deadline={self.starting_deadline}, "
                f"ending_deadline={self.ending_deadline}, value={self.value})")

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

class ProcessGenerator:
    def __init__(self, max_count: Optional[int] = None):
        self.process_count = 0
        self.max_count = max_count if max_count is not None else 100
        self.random = random.Random()
        self.processes_queue = Queue()  # Thread-safe queue

    def generate_process(self) -> Process:
        arrival_time = int(time.time())  # Use current timestamp for real-time arrival
        execution_time = self.random.randint(1, 10)
        starting_deadline = arrival_time + self.random.randint(1, 5)
        ending_deadline = starting_deadline + execution_time + self.random.randint(1, 5)
        value = self.random.randint(1, 100)

        process = Process(
            id=self.process_count,
            arrival_time=arrival_time,
            execution_time=execution_time,
            starting_deadline=starting_deadline,
            ending_deadline=ending_deadline,
            value=value
        )

        self.process_count += 1
        return process

    def run(self):
        while self.process_count < self.max_count:
            process = self.generate_process()
            self.processes_queue.put(process)  # Add process to the thread-safe queue
            print(f"Generated: {process}")
            time.sleep(self.random.uniform(0.5, 2.0))  # Random delay between process generation

# Example usage
def main():
    ready_queue = Queue()
    cpu = CPU(ready_queue)

    # Start the CPU thread
    cpu_thread = threading.Thread(target=cpu.run, daemon=True)
    cpu_thread.start()

    # Start the process generator
    generator = ProcessGenerator(max_count=10)
    generator_thread = threading.Thread(target=generator.run,daemon=True)
    generator_thread.start()

    # Wait for the process generator to finish
    generator_thread.join()

    # Add a sentinel value to signal the CPU to shut down
    ready_queue.put(None)

    # Wait for the CPU thread to finish
    cpu_thread.join()

if __name__ == "__main__":
    main()
