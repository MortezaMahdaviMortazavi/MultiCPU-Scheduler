# MultiCPU-Scheduler

![Scheduler Banner](https://via.placeholder.com/1200x300?text=Multi-CPU+Scheduler)

A simulation of a multi-CPU scheduling system that dynamically generates processes and schedules them on multiple CPUs while managing deadlines, execution times, and scoring. This project demonstrates concurrent programming in Python using threads, mutex locks, and priority queues.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Modules & Files](#modules--files)
- [How It Works](#how-it-works)
- [Usage](#usage)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## Overview

This project implements a multi-CPU scheduling system where processes are generated randomly and concurrently during runtime. Each process is assigned attributes such as arrival time, execution time, starting deadline, ending deadline, and a randomly generated score (value). The goal of the scheduler is to maximize the total score of the completed processes while ensuring that process deadlines are respected.

The system features:
- **Random Process Generation:** A dedicated thread (Process Generator) creates processes at varied intervals.
- **Dynamic Scheduling:** Processes are first placed in an input queue, then moved to a ready queue based on priority and deadline constraints.
- **Multi-CPU Execution:** Multiple CPU threads concurrently execute processes fetched from the ready queue.
- **Deadline & Scoring:** Processes that miss their deadlines are penalized, and scores are aggregated from successfully executed processes.

---

## Features

- **Randomized Process Attributes:**  
  - **Arrival Time:** Time when the process enters the system.
  - **Execution Time:** CPU time required by the process.
  - **Starting Deadline:** Maximum delay allowed for starting execution.
  - **Ending Deadline:** Latest allowable time to complete process execution.
  - **Value (Score):** Random integer between 1 and 100 representing the process's reward.

- **Concurrent Process Generation:**  
  Uses a dedicated thread to generate processes at random intervals and push them into an input queue.

- **Priority-based Scheduling:**  
  The scheduler uses a composite priority (combining process value, deadlines, and execution time) to maintain a bounded ready queue. When the queue is full, lower-priority processes can be replaced by higher-priority ones.

- **Multi-Threaded CPU Simulation:**  
  Multiple CPU threads fetch processes concurrently from the ready queue, ensuring thread-safety with locks to avoid race conditions.

- **Deadline Management:**  
  Processes that expire (due to missed starting deadlines or insufficient time to complete) are dropped and penalized by incrementing the missed process count.

- **Score Tracking:**  
  A shared score tracker aggregates the total score for completed processes and counts missed processes.

---

## Architecture

The system is organized into three main components:

1. **Process Generator:**  
   Responsible for generating random processes and feeding them into the input queue.

2. **Scheduler:**  
   Manages two queues:
   - **Input Queue:** Where processes are initially enqueued.
   - **Ready Queue:** A bounded, priority-based queue from which CPU threads fetch processes.  
   The scheduler also cleans up expired processes and handles queue management.

3. **CPU Threads:**  
   Multiple CPU threads act as consumers. They continuously fetch processes from the scheduler’s ready queue and simulate their execution. They enforce deadline constraints and update the score tracker based on process success or failure.

![System Architecture Diagram](https://via.placeholder.com/800x400?text=System+Architecture)

---

## Modules & Files

- **`main.py`**  
  Entry point of the application. Initializes the process generator, scheduler, CPUs, and the score tracker.

- **`process.py`**  
  Contains the `Process` and `ProcessHybrid` classes with process attributes, deadline checks, and custom ordering based on composite priority.

- **`generator.py`**  
  Implements the `ProcessGenerator` class that produces processes with random attributes and pushes them to the input queue.

- **`scheduler.py`**  
  Implements the `Scheduler` class. It manages the input and ready queues, performs process prioritization, and cleans up expired processes.

- **`cpu.py`**  
  Contains the `CPU` class that simulates CPU threads, executing processes fetched from the scheduler, and updating the score tracker.

---

## How It Works

1. **Process Generation:**  
   The `ProcessGenerator` thread continuously generates new processes with random attributes and enqueues them in the input queue until a specified maximum number of processes is reached.

2. **Scheduling:**  
   The `Scheduler` thread monitors the input queue, transfers valid processes to the ready queue, and maintains the ready queue as a min-heap (using Python's `heapq`) based on composite priority. Processes that are close to missing their deadlines are dropped, and the scheduler replaces lower-priority processes if the ready queue is full.

3. **Execution:**  
   Multiple CPU threads run concurrently. Each CPU thread calls `get_next_process()` on the scheduler to obtain the next process to execute. If a process is expired or cannot finish before its ending deadline, it is marked as missed. Otherwise, the CPU thread simulates the execution by sleeping for the process's execution time and updates the score tracker.

4. **Score Tracking:**  
   The `ScoreTracker` class safely aggregates scores and counts missed processes across multiple threads using mutex locks.

---

## Usage

1. **Prerequisites:**  
   - Python 3.x  
   - Standard libraries (`threading`, `queue`, `time`, `random`, etc.)

2. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/multi-cpu-scheduler.git
   cd multi-cpu-scheduler
