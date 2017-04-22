#usr/bin/env python3
# -*- coding: utf-8 -*-

# Task Killer For Windows

# Imports
import subprocess
import json
import sys
import os

# TODO
class TaskKill:

    def __init__(self):
        pass

    def fetch_data(self):
        """
        Fetches the config data from a json file.
        """
        with open("config.json", "r+", encoding="utf-8") as config:
            data = json.load(config)
            # Add logic
            config.seek(0)
            json.dump(data, config)
            config.truncate(0)

    def check_process(self):
        """
        Checks which processes are running and wether to end those processes or not.
        """
<<<<<<< HEAD
        data = [x.decode("windows-1252").split(",") for x in subprocess.check_output("TASKLIST /FO csv").splitlines()][3:]
        proc = {x[0][1:-1]: int(x[1][1:-1]) for x in data}

=======
        proc = [line.split() for line in subprocess.check_output("TASKLIST").splitlines()] # Look up /fo parameter for Tasklist
        # Use list comprehension for subprocess.check_output()
        # Clean the list for newlines
        # Add processes and process ids to an dictionary
        # Return processes and call kill_process with this dictionary
    
>>>>>>> 51380a7ae75dde342160a22b70f90aa1a57b6b28
    def kill_process(self):
        """
        Calls the TASKKILL command to Windows CMD.
        """
        pass

    def log_information(self, status):
        """
        Logs information to a log file.
        """
        separator = "=" * 30 + "\n"
        with open("taskkill_logs.txt", "a", encoding="utf-8") as logs:
            try:
                logs.write("{} Kill Status: {}\n".format(separator, status))
            except Exception as e:
                print("Unexpected Error Occured: {}".format(e))
                exit(1)
