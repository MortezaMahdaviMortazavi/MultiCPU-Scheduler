import threading
import time
from queue import Queue
from typing import Optional
from process import Process


class CPU(threading.Thread):
    def __init__(self, cpu_id: int, scheduler, score_tracker):
        super().__init__()
        self.cpu_id = cpu_id
        self.scheduler = scheduler
        self.score_tracker = score_tracker
        self.current_process: Optional[Process] = None
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            process = self.scheduler.get_next_process()
            if process:
                self._execute_process(process)
            else:
                time.sleep(0.2)

    def _execute_process(self, process: Process):
        current_time = time.time()
        if process.missed_deadline or process.is_expired(current_time) or not process.can_finish(current_time):
            self.score_tracker.add_missed()
            print("Process with Id",process.id,"Has Expired Oh Damn you Bitch")
            return

        try:
            print(f"CPU-{self.cpu_id} ▶ Started process {process.id} "
                  f"(Value:{process.value} Deadline:{process.starting_deadline-current_time:.1f}s)")
            time.sleep(process.execution_time)
            
            if time.time() > process.ending_deadline:
                print("Missed ending deadline",end="------------")
                raise RuntimeError("Missed ending deadline")
                
            self.score_tracker.add_score(process.value)
            print(f"CPU-{self.cpu_id} ✔ Completed process {process.id} (+{process.value}pts)")
            
        except Exception as e:
            print(f"CPU-{self.cpu_id} ❌ Failed process {process.id} ({str(e)})")
            self.score_tracker.add_missed()

    def stop(self):
        self._stop_event.set()