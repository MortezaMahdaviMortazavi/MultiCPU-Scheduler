import threading
from queue import Queue
from process import Process, ProcessGenerator
from cpu import CPU

def main():
    ready_queue = Queue()
    cpu = CPU(id=1, ready_queue=ready_queue)

    generator = ProcessGenerator(max_count=5)
    generator_thread = threading.Thread(target=generator.run, daemon=True)

    generator_thread.start()
    generator_thread.join()
    cpu.ready_queue = generator.processes_queue
    cpu_thread = threading.Thread(target=cpu.run, daemon=True)
    cpu_thread.start()

    
    ready_queue.put(None)  # Signal CPU to stop

    cpu_thread.join()

if __name__ == "__main__":
    main()