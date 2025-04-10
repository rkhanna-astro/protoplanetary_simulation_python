# EARLY STAGES OF PROTOSTELLAR DISK EVOLUTION: A LINK TO INITIAL CLOUD CORE

## Background:
This is a Python code for running and solving different cases to study early Protostellar Disk Evolution analytically.

## How to Run:
The code is still under maintainence and improvement. However, you can run the few cases as follows:
-   Make sure you take the latest git pull of the Codebase.
-   Ensure that these files have the Python packages installed - `process.py`, `process_nw.py`, `makedata_c.py`, `fun_bvps_c.py`, `funsys_c.py` and `plot_me.py`.
-   After this you can run one of these files to run different initial conditions to study the first 3000 years of cloud core:
    - `time_evol_eta1.py`
    - `time_evol_eta2_a4_a5.py`
    - `time_evol_eta2.py`
    - `time_evol_eta3.py`
    - `time_evolnw.py`

## Results:
As of now the results will be simple CSV files with all the essential properties that we aim to study to understand the disk evolution. The code will generate something like `output_alpha_{alpha}_eta_{eta}_time_{time_year}.csv`. Here, time_year will range from 1000 to 3000 years incremented by 50 years.

## Further Updates:
Soon, with the team, I aim to fix the complete codebase. For regular updates, do visit this github repository or take git pulls.

## Contact:
For any doubts or concerns contact me Rahul (rkhann43@uwo.ca) or Majd (mnoel25@uwo.ca).

Thank you

