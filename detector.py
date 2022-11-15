import os
import shutil
import subprocess
from os.path import exists

import psutil
import getopt
import sys

time = 1
black_list = []
white_list = []

while True:
    if time == 1:
        print("\nScanning in progress...")
    proc = subprocess.Popen('netstat -ano -p tcp | findStr "993 587 465 2525"', shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    out, err = proc.communicate()

    output = out.decode()

    my_list = output.split(" ")
    # PID will be the last number once split
    pid = my_list[-1]
    # obtain output from checking the application name of PID
    cmd_output = subprocess.getoutput(f'tasklist /fi "pid eq {pid}"')
    # to make finding process name easier, split cmd_output
    process_name = cmd_output.split()

    time += 1
    if "ESTABLISHED" in output:
        # delete empty array elements
        my_list = list(filter(None, my_list))
        # get the full IP address with port number from the last element from output
        port_num = my_list[-3]
        # split at the ':' to get port number at last index of array
        get_port = port_num.split(":")
        port = get_port[-1]

       # 13th element in process_name will always be application name
        process_name = process_name[13]
        p = psutil.Process(int(pid))

        if process_name not in white_list:
            print("KEYLOGGER DETECTED!")

            # terminate process if it exists in blacklist
            if process_name in black_list:
                p.kill()
                print("Blacklist application found running.\nProcess automatically terminated.")
                time = 1
            # if process is not in whitelist, check if it should be
            elif process_name not in white_list:
                print("Pausing application...\n")
                p.suspend()
                print("Information on application identified in your system to be potential threat...")
                print(f'Application name: {process_name}\n'
                        f'Process ID (PID): {pid}'
                        f'Trying to communicate on port {port}\n')
                selected = False
                while not selected:
                    is_safe = input("Would you like to whitelist this application? (Y/N): ").lower()
                    if is_safe == 'n':
                        print("Terminating process...")
                        p.kill()
                        print("Adding to blacklist...")
                        black_list.append(process_name)
                        selected = True
                        time = 1
                    elif is_safe == 'y':
                        print("Resuming process...")
                        p.resume()
                        print("Adding to whitelist...")
                        white_list.append(process_name)
                        selected = True
                        time = 1

                    print("whitelist:", white_list)
                    print("blacklist:", black_list)
