# log_monitoring

A simple Python script to monitor task durations from a log file and log warnings or errors if thresholds are exceeded.

## Installation

1. Clone the repository or download the script.
2. Install dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

1. Make sure your log file is named logs.log and is formatted like:

    ```csv
    11:35:23,scheduled task 032, START,37980
    11:35:56,scheduled task 032, END,37980
    ```

2. Run the script:

    ```bash
    python log_monitoring.py
    ```

3. Check the generated files:

    ```text
    warnings.log — for tasks exceeding 5 minutes
    errors.log — for tasks exceeding 10 minutes
    ```
