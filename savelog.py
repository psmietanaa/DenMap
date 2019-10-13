from datetime import *
import os


# This function stores logs
def write_log(data):
    # Creating a directory to store the logs
    foldername = "logs"
    # This ignores the error of an already created dir
    os.makedirs(foldername, exist_ok=True)
    # Give normal user permission to read logs
    os.chmod(foldername, 0o777)
    # Get current time
    time = datetime.now().strftime("%Y-%m-%d %H:%M")
    # Set file name
    filename = "log_" + time + '.txt'
    output = os.path.join(foldername, filename)
    # Write data to log
    with open(output, "a") as file:
        # Give normal user permission to read logs
        os.chmod(output, 0o777)
        file.write(data + "\n\n")
