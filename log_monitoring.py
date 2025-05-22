import pandas as pd

# This function loads and ensures the correct data type of the logs
def load_and_clean_log(filepath):
    logs = pd.read_csv(filepath, names=['time', 'description', 'status', 'id'], dtype=str)
    # Ensure the time is the correct data type
    logs['time'] = pd.to_datetime(logs['time'], format='%H:%M:%S')
    # Ensure the id is int and no whitespaces are present
    logs['id'] = logs['id'].str.strip().astype(int)
    # Ensure no whithespaces are present
    logs['status'] = logs['status'].str.strip()
    logs['description'] = logs['description'].str.strip()
    return logs

# This function creates a new dataframe that meres the logs with the same id and 
# computes the time it took the job to finish
def calculate_duration(logs):
    # Split the Start and end logs
    starts = logs[logs['status'] == 'START'].copy()
    ends = logs[logs['status'] == 'END'].copy()
    # Create a new df merged between the two 
    merged = pd.merge(starts, ends, on='id', suffixes=('_start', '_end'))
    # Add the duration to the df
    merged['duration'] = merged['time_end'] - merged['time_start']
    return merged[['id', 'description', 'time_start', 'time_end', 'duration']]

if __name__ == "__main__":
    logs = load_and_clean_log('logs.log')
    duration_df = calculate_duration(logs)