#usr/bin/env python3
# -*- coding: utf-8 -*-

# Task Killer For Windows

# Imports
import subprocess
import datetime
import json
import sys

def fetch_data(process):
    """
    Fetches the config data from a json file.
    """

    with open("config.json", "r+", encoding="utf-8") as config:
        try:
            data = json.load(config)
        except Exception as e:
            print("Unexpected Error Occured: {}".format(e))

        # Dictionary with int as a key for the profile
        profiles = {x + 1: i for x, i in enumerate(data["profiles"])}

        print("PROFILES: {}".format(profiles))
        profile = input("ENTER ID: ")

        # Sets the current profile to whatever int you chose
        profile = profiles[int(profile)]

        # Set of processes to kill
        kill_list = set()

        # Checks if there are processes in the config.json file
        if len(data["profiles"][profile]) < 1:
            print("Warning no processes has been set to kill in the config.json")
            exit(1)
        else:
            for proc in process:
                if proc in data["profiles"][profile]:
                    kill_list.add(proc)
                else:
                    continue

        # To avoid duplicates of a process a set is used
        # This will only affect the amount of errors output and reduce the
        # runtime of the script a bit.
        kill_process(kill_list)

def check_process():
    """
    Checks which processes are running and wether to end those processes or not.
    """

    # Calls the windows command TASKLIST in csv format
    # Formats it using line splitting and decodes the strings
    # Splits the commas
    # Slices it to exclude the first items that define PID, name etc...
    data = [x.decode("windows-1252").split(",") for x in \
    subprocess.check_output("TASKLIST /FO csv").splitlines()][3:]

    # Fetches the name of each process and excludes the single quotations mark
    # around the string otherwise it would look like '"this.exe"' which is != "this.exe"
    proc = [x[0][1:-1] for x in data]

    fetch_data(proc)

def kill_process(process):
    """
    Calls the TASKKILL command to Windows CMD.
    """
    # Stores the output from output of TASKKILL like errors and successes
    status = []

    for proc in process:
        try:
            # Calls the TASKKILL using the force, terminate all child processes
            # and the imagename parameter, decodes into utf-8 and appends the output
            # to the status list.
            proc_status = subprocess.check_output("TASKKILL /F /T /IM {}".format(proc)).decode("utf-8")
            status.append(proc_status)

        except subprocess.CalledProcessError as e:
            print("Error Occured: ", e)
            status.append("ERROR")
            pass

    log_information(status)

def log_information(status):
    """
    Logs information to a log file.
    """

    # Decorative for the text file storing the logs
    separator = "=" * 30 + "\n"
    
    with open("taskkill_logs.txt", "a", encoding="utf-8") as logs:
        try:
            for log in status:
                logs.write(log + " : " + str(datetime.datetime.now()))

            # Writing the logs with decoration to the log file
            logs.write("\n" + separator + "\n")
        except Exception as e:
            print("Unexpected Error Occured: {}".format(e))
            exit(1)

    exit(0)

if __name__ == "__main__":
    if sys.platform.startswith("win32"):
        check_process()
    else:
        print("This os is not based on win32.")
        exit(1)
