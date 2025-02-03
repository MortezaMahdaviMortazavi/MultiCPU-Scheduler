from queue import Queue
import time
import random
from dataclasses import dataclass
from typing import Optional
import heapq
import threading

from process import Process



class Scheduler(threading.Thread):
    def __init__(self, input_queue, score_tracker, max_ready_size=5):
        super().__init__()
        self.input_queue = input_queue
        self.ready_queue = []
        self.lock = threading.Lock()
        self.max_ready_size = max_ready_size
        self._stop_event = threading.Event()
        self.score_tracker = score_tracker

    def _add_to_ready(self, process: Process):
        current_time = time.time()
        
        # Immediate deadline check
        if process.is_expired(current_time):
            self.score_tracker.add_missed()
            print("Process with Id",process.id,"Has Expired Oh Damn you Bitch")
            process.missed_deadline = True
            return False
            
        if not process.can_finish(current_time):
            self.score_tracker.add_missed()
            process.missed_deadline = True
            print("Process with Id",process.id,"Has Expired Oh Damn you Bitch")
            return False

        with self.lock:
            if len(self.ready_queue) < self.max_ready_size:
                heapq.heappush(self.ready_queue, process)
                return True
            else:
                # Replace strategy using composite priority
                if process > self.ready_queue[0]:
                    removed = heapq.heappop(self.ready_queue)
                    heapq.heappush(self.ready_queue, process)
                    if not removed.missed_deadline:
                        self.score_tracker.add_missed()
                    return True
        return False

    def get_next_process(self) -> Optional[Process]:
        with self.lock:
            if self.ready_queue:
                return heapq.heappop(self.ready_queue)
        return None

    def run(self):
        while not self._stop_event.is_set():
            process = self.input_queue.get()
            if process is None:
                self._stop_event.set()
                break
            self._add_to_ready(process)
            self._cleanup_expired()

    def _cleanup_expired(self):
        current_time = time.time()
        with self.lock:
            new_queue = []
            for p in self.ready_queue:
                if p.is_expired(current_time) or not p.can_finish(current_time):
                    self.score_tracker.add_missed()
                    p.missed_deadline = True
                else:
                    new_queue.append(p)
            self.ready_queue = new_queue
            heapq.heapify(self.ready_queue)

    def stop(self):
        self._stop_event.set()