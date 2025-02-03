import threading
from queue import Queue
from process import Process
from generator import ProcessGenerator , ScoreTracker
from cpu import CPU
from scheduler import Scheduler
import matplotlib.pyplot as plt


import matplotlib.pyplot as plt



# def run_experiment(num_cpus):
#     input_queue = Queue()
#     score_tracker = ScoreTracker()

#     generator = ProcessGenerator(input_queue)
#     scheduler = Scheduler(input_queue, score_tracker)
#     cpus = [CPU(i, scheduler, score_tracker) for i in range(num_cpus)]

#     generator.start()
#     scheduler.start()
#     for cpu in cpus:
#         cpu.start()

#     generator.join()
#     scheduler.stop()
#     scheduler.join()

#     for cpu in cpus:
#         cpu.stop()
#         cpu.join()

#     missed_processes = [p for p in generator.process_list if p.missed_deadline]
#     accepted_processes = [p for p in generator.process_list if not p.missed_deadline]

#     hit_rate = len(accepted_processes) / (len(missed_processes) + len(accepted_processes)) * 100
#     return len(missed_processes), hit_rate

# def main():
#     missed_processes_results = []
#     hit_rate_results = []

#     # Run 20 experiments with different numbers of CPUs (from 1 to 20)
#     for num_cpus in range(21, 51):
#         missed, hit_rate = run_experiment(num_cpus)
#         missed_processes_results.append(missed)
#         hit_rate_results.append(hit_rate)

#     # Plotting the results with matplotlib
#     fig, ax1 = plt.subplots()

#     ax1.set_xlabel('Number of CPUs')
#     ax1.set_ylabel('Missed Processes', color='tab:red')
#     ax1.plot(range(1, 31), missed_processes_results, color='tab:red', label='Missed Processes')
#     ax1.tick_params(axis='y', labelcolor='tab:red')

#     ax2 = ax1.twinx()
#     ax2.set_ylabel('Hit Rate (%)', color='tab:blue')
#     ax2.plot(range(1, 31), hit_rate_results, color='tab:blue', label='Hit Rate')
#     ax2.tick_params(axis='y', labelcolor='tab:blue')

#     fig.tight_layout()
#     plt.title('Performance with Different Number of CPUs')
#     plt.show()

#     with open("logs/experiment_results2.txt", "w") as file:
#         for num_cpus in range(1, 31):
#             file.write(f"CPUs: {num_cpus}, Missed Processes: {missed_processes_results[num_cpus-1]}, Hit Rate: {hit_rate_results[num_cpus-1]}%\n")

#     print("Experiment complete. Results saved and plotted.")

# if __name__ == "__main__":
#     main()


def main():
    input_queue = Queue()
    score_tracker = ScoreTracker()
    
    generator = ProcessGenerator(input_queue)
    scheduler = Scheduler(input_queue, score_tracker)
    cpus = [CPU(i, scheduler, score_tracker) for i in range(3)]
    
    generator.start()
    scheduler.start()
    for cpu in cpus:
        cpu.start()

    generator.join()
    scheduler.stop()
    scheduler.join()
    
    for cpu in cpus:
        cpu.stop()
        cpu.join()

    print("\n=== Final Results ===")
    print(f"Total Score: {score_tracker.total_score}")
    print(f"Missed Processes: {score_tracker.missed_processes}")
    missed_processes = [p for p in generator.process_list if p.missed_deadline]
    accepted_processes = [p for p in generator.process_list if not p.missed_deadline]
    print("Number of Misses:",len(missed_processes))
    print("Number of Accepted:",len(accepted_processes))

    print("HateRate:", "% " + str(int(len(accepted_processes) / (len(missed_processes) + len(accepted_processes)) * 100)))
    print("System shutdown complete")

    with open("logs/missed_processes.txt", "w") as file:
        file.write("Missed Processes:\n")
        for process in missed_processes:
            file.write(f"Process ID: {process.id}, Details: {repr(process)}\n")

    with open("logs/accepted_processes.txt", "w") as file:
        file.write("Accepted Processes:\n")
        for process in accepted_processes:
            file.write(f"Process ID: {process.id}, Details: {repr(process)}\n")


if __name__ == "__main__":
    main()

##### 10 cpu ==> Total Score = 4074 , Missed Processes = 6
#### 8 cpu ==> Total Score = 3166 , Missed Processes = 15
#### 6 cpu ==> Total Score = 3414 , Missed Processes = 17
#### 4 cpu ==> Total Score = 2401 , Missed Processes = 25
#### 2 cpu ==> Total Score = 1099 , Missed Processes = 26
#### 1 cpu ==> Total Score = 589 , Missed Processes = 40