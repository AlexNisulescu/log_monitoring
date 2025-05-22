import pandas as pd

def load_and_clean_log(filepath):
    logs = pd.read_csv(filepath, names=['time', 'description', 'status', 'id'], dtype=str)
    # Ensure the time is the correct data type
    logs['time'] = pd.to_datetime(logs['time'], format='%H:%M:%S')
    # Ensure the id is int
    logs['id'] = logs['id'].astype(int)
    return logs

if __name__ == "__main__":
    logs = load_and_clean_log('logs.log')