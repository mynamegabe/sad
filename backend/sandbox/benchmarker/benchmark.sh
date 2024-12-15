#!/bin/sh

# get initial processes running using ps
ps -aux > /tmp/initial_processes

# run command time /sandbox/run.sh in background and store the result in /tmp/time
time /app/run.sh > /tmp/time &

# get final processes running using ps
ps -aux > /tmp/final_processes

# get the difference between the initial and final processes
process_diff=$(diff /tmp/initial_processes /tmp/final_processes)

# store the results in /tmp/results
echo "PROCESS DIFFERENCE" >> /tmp/results
echo "$process_diff" >> /tmp/results
echo "PROCESS DIFFERENCE END" >> /tmp/results
echo "EXEUCTION TIME" >> /tmp/results
echo $(cat /tmp/time) >> /tmp/results
echo "EXECUTION TIME END" >> /tmp/results

# remove run.sh 
rm /app/run.sh

python entropy_scan.py --filename /tmp/0Hr6xm8QV5
python yara-scanner/yara_main.py --update
python yara-scanner/yara_main.py --scan-dir /tmp/0Hr6xm8QV5 --gen-report --recursive