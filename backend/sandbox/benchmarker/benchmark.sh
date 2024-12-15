#!/bin/sh

# get initial processes running using ps
initial_processes=$(ps -aux)

# get initial time
initial_time=$(date)

# run command
sh run.sh &

# get final processes running using ps
final_processes=$(ps -aux)

# get the difference between the initial and final processes
process_diff=$(diff <(echo "$initial_processes") <(echo "$final_processes"))

# get final time
final_time=$(date)

# get the difference between the initial and final time
time_diff=$(diff <(echo "$initial_time") <(echo "$final_time"))

# store the results in /tmp/results
echo "$process_diff" > /tmp/results
echo "$time_diff" >> /tmp/results

python entropy_scan.py
python yara-scanner/yara_main.py --update
python yara-scanner/yara_main.py --scan-dir /app/testdir --gen-report --recursive