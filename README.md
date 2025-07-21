# EARLY STAGES OF PROTOSTELLAR DISK EVOLUTION: A LINK TO INITIAL CLOUD CORE

## Background:
This is a Python code for running and solving different cases to study early Protostellar Disk Evolution analytically.

## How to Run (fiducial case):
The code is still under maintainence and improvement. However, you can run some important cases as follows:
-   Make sure you take the latest git pull of the Codebase.
-   Ensure that these Python packages are installed - `numpy`, `scipy`, `scipy.integrate`, `scipy.optimize`, `matplotlib`.
-   The essential files for solving the analytical solution are: `process.py`, `process_nw.py`, `makedata_c.py`, `fun_bvps_c.py`, `funsys_c.py`,  `plot_me.py` and `plot_me_3times.py`.

-   After this you can run the following file to study the first 3000 years of cloud core for the fiducial case (alpha = 0.5, gamma = 1.1, eta = 0.01 and lambda = 0.1):
    - `time_fiducial_case.py`

- If you want to play with the code and the set of parameters, you can manually change any of the paremeter (alpha, gamma, eta and lambda) in the `results` dictionary object in `time_fiducial_case.py` file. For example for different alpha, we can do as follows:

```
results = {
    'fiducial': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    'alpha1': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.3, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    'alpha2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.8, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'}
}
```

- The years are stored as integers from `pf1 - pf41`, where 1 points to values for 1000 yr and 41 points to values for 3000 yr, for the `general` case. (as the increment is of 50 years for 1 iteration)

- To fetch the results for your case you have to get it as follows as done in the fiducial case:

```
results_1000_yr = dict['fiducial']['pf1']
results_1500_yr = dict['fiducial']['pf11']
results_2000_yr = dict['fiducial']['pf21']
results_3000_yr = dict['fiducial']['pf41']
```

- For running multiple cases, you can also add new keys and the values will be different for different set of parameters in the `results` dictionary.

## Creating Figures:
To run and generate any of the figures that we have finalized, you can run any of the file starting with `figure`, example:
- `figure1_time_evolution.py` generates the figure 1 for time evolution (t = 1, 2 and 3 kyrs)
    - `figure5_gamma_evolution.py` generates the figure 5 which depicts the influence of different gamma over the disk evolution.

After running any of these file, a `pdf` or a `jpg` will be created file that will show the figure for the desired parameter or plot.

## Results:
As of now the results will be stored in CSV files with all the essential properties that we aim to study to understand the disk evolution. 

All the codes will generate many files like `output_alpha_{alpha0}_eta_{etaprime}_lambda_{lamda0}_time_{time_year}.csv`. Here, by default time_year will range from 1000 to 3000 years, incremented by 50 years.

## Further Updates:
Soon, with the team, I aim to fix the complete codebase. For regular updates, do visit this github repository or take git pulls.

## Contact:
For any doubts or concerns contact me Rahul (rkhann43@uwo.ca) or Majd (mnoel25@uwo.ca).

Thank you for your curiosity!
