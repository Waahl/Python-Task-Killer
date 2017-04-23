#usr/bin/env python3
# -*- coding: utf-8 -*-

# Task Killer For Windows

# Imports
import subprocess
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

        if len(data["whitelist"]) < 1:
            print("Warning no processes has been whitelisted in the config.json")
        else:
            for proc in process:
                if proc not in data["whitelist"]:
                    kill_process(proc)
                else:
                    print("Skipping process {}".format(proc))

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
    status = []
    try:
        proc_status = subprocess.check_output("TASKKILL /F /T /IM {}".format(process)).decode("utf-8")
        status.append(proc_status)
    except subprocess.CalledProcessError:
        print("Failed to find task, skipping.")
        status.append("ERROR")
        pass
    log_information(status)

def log_information(status):
    """
    Logs information to a log file.
    """
    separator = "=" * 30 + "\n"
    with open("taskkill_logs.txt", "a", encoding="utf-8") as logs:
        try:
            for i in status:
                logs.write(i)
            logs.write("\n" + separator + "\n")
        except Exception as e:
            print("Unexpected Error Occured: {}".format(e))
            exit(1)
    exit(0)

if __name__ == "__main__":
    if sys.platform == "win32":
        check_process()
    else:
        print("This os is not based on win32.")
        exit(1)
