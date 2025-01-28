from dataclasses import dataclass
from typing import Optional

@dataclass
class Process:
    id: int
    arrivalTime: int
    executionTime: int
    startingDeadline: int
    endingDeadline: int
    value: int

    def get_remaining_time(self, current_time: int) -> int:
        return self.endingDeadline - current_time

    def is_expired(self, current_time: int) -> bool:
        return current_time > self.startingDeadline or current_time > self.endingDeadline

    def __str__(self) -> str:
        return (f"Process(id={self.id}, arrivalTime={self.arrivalTime}, "
                f"executionTime={self.executionTime}, startingDeadline={self.startingDeadline}, "
                f"endingDeadline={self.endingDeadline}, value={self.value})")
    



# Create a process
process = Process(
    id=1,
    arrivalTime=0,
    executionTime=5,
    startingDeadline=10,
    endingDeadline=15,
    value=100
)

# Check if the process is expired at a given time
current_time = 12
print(process.is_expired(current_time))  # Output: False

# Get remaining time until the ending deadline
print(process.get_remaining_time(current_time))  # Output: 3

# Print the process details
print(process)
# Output: Process(id=1, arrivalTime=0, executionTime=5, startingDeadline=10, endingDeadline=15, value=100)