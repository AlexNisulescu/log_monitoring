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
    return merged[['id', 'description_start', 'time_start', 'time_end', 'duration']]

# This function evaluates if the log should be a warning or an error
def evaluate_duration(duration, threshold_warning=5, threshold_error=10):
    minutes = duration.total_seconds() / 60
    if minutes > threshold_error:
        return 'ERROR'
    elif minutes > threshold_warning:
        return 'WARNING'
    else:
        return None

# This function is used to generate the report
def generate_report(merged_df):
    report = []
    for _, row in merged_df.iterrows():
        log_level = evaluate_duration(row['duration'])

        # Format duration as HH:MM:SS
        total_seconds = int(row['duration'].total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        formatted_duration = f"{hours:02}:{minutes:02}:{seconds:02}"
        # Report message
        msg = f"Job {row['id']} ({row['description_start']}): Duration = {formatted_duration}"
        # Append the warning/error message
        if log_level:
            msg += f" [{log_level}: Duration exceeds {5 if log_level == 'WARNING' else 10} minutes!]"
        report.append(msg)
    return report

if __name__ == "__main__":
    logs = load_and_clean_log('logs.log')
    duration_df = calculate_duration(logs)
    report = generate_report(duration_df)

    # Write the warnings and errors to warnings.log and errors.log files
    with open('warnings.log', 'w') as warning_file, open('errors.log', 'w') as error_file:
        for line in report:
            if '[WARNING:' in line:
                warning_file.write(line + '\n')
            elif '[ERROR:' in line:
                error_file.write(line + '\n')