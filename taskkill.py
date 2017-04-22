#usr/bin/env python3
# -*- coding: utf-8 -*-

# Task Killer For Windows

# Imports
import subprocess
import json
import sys
import os

# TODO

def fetch_data(process):
    """
    Fetches the config data from a json file.
    """
    with open("config.json", "r+", encoding="utf-8") as config:
        data = json.load(config)
        if process in data["processes"]:
            kill_process(process)

def check_process():
    """
    Checks which processes are running and wether to end those processes or not.
    """
    data = [x.decode("windows-1252").split(",") for x in \
    subprocess.check_output("TASKLIST /FO csv").splitlines()][3:]

    proc = [x[0][1:-1] for x in data]

    for process in proc:
        fetch_data(process)

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

if __name__ == "__main__":
    check_process()
