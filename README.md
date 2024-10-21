# Job Shop Scheduling Problem Solver using Genetic Algorithm

Welcome to my genetic algorithm implementation for solving the Job Shop Scheduling Problem (JSSP). This project aims to provide an efficient solution to JSSP, which is a complex combinatorial optimization problem.

## Getting Started

### Prerequisites

Ensure you have the following software installed:
- Python 3
- Git

**Clone the Repository**

   Clone the `main` branch of the repository:

   ```bash
   git clone https://github.com/tarungattu/JobShopGA_withAMR.git
   ```
### Running the Algorithm

The scheduler is built as a class, having various method including the main genetic algorithm method. In order to run it you must import it in you python file

```bash
from JobShopScheduler import JobShopScheduler
```

The various parameters must be set before creating a scheduler

```bash
m - number of Machines
n - number of Jobs
num_amrs - number of AMRs
N - Population size for Genetic Algorithm
pc - Crossover Probability
pm - Mutation Probability
T - Maximum number of generations
machine_data - job data for machine sequence. Can be used from the benchmarks file
ptime_data - processing time data for each job on each machine. Can be used from the benchmarks file.
```

Each benchmark is a dictionary containing two keys: machine_data and ptime_data


