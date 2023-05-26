#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script to watch the log output of execution for each process.
# This script starts tmux with 6 window instances to let the user have an overview
# of the logs representing the current system behavior.
# To look at them in your editor, open the file at /tmp/logfiles/.
# Terminating tmux works with `Ctrl-b + :kill-session` in the command prompt.
# You may want to use `tmux list-sessions` and `tmux attach-session -t NR`,
# if you accidentally detached with `Ctrl-b d`, but you could also use `killall tmux`
# or `tmux list-sessions` and tmux kill-sessions -t SESSNAME`.
# You may want to also use `netstat -tupl` to see what program uses what ip+ports.
# Best tmux guide https://gist.github.com/sdondley/b01cc5bb1169c8c83401e438a652b84e

from typing import Any
import os
import shutil
import subprocess
import sys
import time # sleep

# Workaround slow network connection with checking the output and continuously retrying on failure
# tmux might still mess up the layout, but we have a much better chance than "simply trying"
def subproc_rununtil_returncode(goal_returncode: int, command: Any):
    current_returncode = 0
    if goal_returncode == 0:
        current_returncode = 1
    elif goal_returncode == 1:
        current_returncode = 0        # run at least once

    while current_returncode != goal_returncode:
        runres = subprocess.run(command)
        current_returncode = runres.returncode
        time.sleep(0.05)


if (shutil.which("tmux") is None):
  print("Please install tmux to have functional monitoring, exiting..")
  sys.exit(1)
if (shutil.which("netcat") is None):
  print("Please install netcat to have functional input writing, exiting..")
  sys.exit(1)

args = sys.argv
len_args = len(args)
lognr: int = 0
if len_args != 2:
  print('./iorepl.py must have exactly 1 argument: the number of the log files, exiting..')
  sys.exit(1)
if args[1] == "-h" or args[1] == "--help":
  # printUsage()
  sys.exit(0)
try:
  lognr = int(args[1])
except ValueError:
  print('argument is no valid integer, exiting..')
  sys.exit(1)

log_dir = "/tmp/logfiles/"
proc_name1 = "example1"
proc_name2 = "example2"
proc_name3 = "example3"
port_proc_name1 = 123
port_proc_name2 = 124

# get log file paths
proc_name1_logfile: str = os.path.join(log_dir, proc_name1+str(lognr)+".log")
proc_name2_logfile: str = os.path.join(log_dir, proc_name2+str(lognr)+".log")
proc_name3_logfile: str = os.path.join(log_dir, proc_name3+str(lognr)+".log")

# ensure that all log files are existing
if (os.path.isdir(log_dir) is False):
  print('The directory for the logfiles does not exist, exiting..')
  sys.exit(1)
if (os.path.isfile(proc_name1_logfile) is False):
  print('logfiles for proc_name1_logfile does not exist, exiting..')
  sys.exit(1)
if (os.path.isfile(proc_name2_logfile) is False):
  print('logfiles for proc_name2_logfile does not exist, exiting..')
  sys.exit(1)
if (os.path.isfile(proc_name3_logfile) is False):
  print('logfiles for proc_name3_logfile does not exist, exiting..')
  sys.exit(1)

# tmux kill-session -t iorepl_tmux
subprocess.run(["tmux", "kill-session", "-t", "iorepl_tmux"]) # returns 0, if session exists and 1, if not
time.sleep(0.05)
# This might also log "cant't find session: iorepl_tmux"

## prepare windowing layout
# tmux new -d -siorepl_tmux
subprocess.run(["tmux", "new", "-d", "-s", "iorepl_tmux"]) # returns 1
time.sleep(0.05)

# tmux send-keys -t iorepl_tmux.0 'tmux split-window -p 50 -c "$PWD"' ENTER
cmd = ["tmux", "send-keys", "-t", "iorepl_tmux.0", "tmux split-window -p 50 -c \"$PWD\"", "ENTER"]
subproc_rununtil_returncode(0, cmd)
# 0
# 1<-
# tmux send-keys -t iorepl_tmux 'tmux select-pane -t 0' ENTER
cmd = ["tmux", "send-keys", "-t", "iorepl_tmux", "tmux select-pane -t 0", "ENTER"]
subproc_rununtil_returncode(0, cmd)
# subprocess.run(["tmux", "send-keys", "-t", "iorepl_tmux", "tmux select-pane -t 0", "ENTER"], check=True)
# time.sleep(0.05)
# tmux send-keys -t iorepl_tmux.0 'tmux split-window -h -p 66 -c "$PWD"' ENTER
cmd = ["tmux", "send-keys", "-t", "iorepl_tmux.0", "tmux split-window -h -p 66 -c \"$PWD\"", "ENTER"]
subproc_rununtil_returncode(0, cmd)
# 0 |  1<-|
#    2
# tmux send-keys -t iorepl_tmux.1 'tmux split-window -h -p 50 -c "$PWD"' ENTER
cmd = ["tmux", "send-keys", "-t", "iorepl_tmux.1", "tmux split-window -h -p 50 -c \"$PWD\"", "ENTER"]
subproc_rununtil_returncode(0, cmd)
# tmux send-keys -t iorepl_tmux 'tmux select-pane -t 3' ENTER
cmd = ["tmux", "send-keys", "-t", "iorepl_tmux", "tmux select-pane -t 3", "ENTER"]
subproc_rununtil_returncode(0, cmd)
# 0 | 1 | 2
#     3<-
# tmux send-keys -t iorepl_tmux.3 'tmux split-window -h -p 66 -c "$PWD"' ENTER
cmd = ["tmux", "send-keys", "-t", "iorepl_tmux.3", "tmux split-window -h -p 66 -c \"$PWD\"", "ENTER"]
subproc_rununtil_returncode(0, cmd)
# # #tmux send-keys -t iorepl_tmux.4 'tmux split-window -h -p 50 -c "$PWD"' ENTER
cmd = ["tmux", "send-keys", "-t", "iorepl_tmux.4", "tmux split-window -h -p 50 -c \"$PWD\"", "ENTER"]
subproc_rununtil_returncode(0, cmd)
# 0 | 1 | 2
# 3 | 4 | 5<-
# tmux send-keys -t iorepl_tmux 'tmux set-option mouse on' ENTER
cmd = ["tmux", "send-keys", "-t", "iorepl_tmux", "tmux set-option mouse on", "ENTER"]
subproc_rununtil_returncode(0, cmd)
time.sleep(0.2)

### visualize output
# tmux send-keys -t iorepl_tmux.0 'tail -f proc_name1_logfile' ENTER
# tmux send-keys -t iorepl_tmux.1 'tail -f proc_name2_logfile' ENTER
# tmux send-keys -t iorepl_tmux.2 'tail -f proc_name3_logfile' ENTER
# tmux send-keys -t iorepl_tmux.3 'netcat localhost port_proc_name1' ENTER
# tmux send-keys -t iorepl_tmux.4 'netcat localhost port_proc_name2' ENTER
# tmux attach-session -twatch_repl_tmux
subprocess.run(["tmux", "send-keys", "-t", "iorepl_tmux.0", "tail -f "+proc_name1_logfile, "ENTER"], check=True)
time.sleep(0.05)
subprocess.run(["tmux", "send-keys", "-t", "iorepl_tmux.1", "tail -f "+proc_name2_logfile, "ENTER"], check=True)
time.sleep(0.05)
subprocess.run(["tmux", "send-keys", "-t", "iorepl_tmux.2", "tail -f "+proc_name3_logfile, "ENTER"], check=True)
time.sleep(0.05)
subprocess.run(["tmux", "send-keys", "-t", "iorepl_tmux.3", "tmux kill-session -t iorepl_tmux"], check=True)
time.sleep(0.05)
## start netcat for input writing
subprocess.run(["tmux", "send-keys", "-t", "iorepl_tmux.4", "netcat localhost "+str(port_proc_name1), "ENTER"], check=True)
time.sleep(0.05)
subprocess.run(["tmux", "send-keys", "-t", "iorepl_tmux.5", "netcat localhost "+str(port_proc_name2), "ENTER"], check=True)
time.sleep(0.05)
subprocess.run(["tmux", "attach-session", "-t", "iorepl_tmux"])

#tmux send-keys -t iorepl_tmux.0 'tmux split-window -c "$PWD"' ENTER
# split-window options:
# -h for horizontal instead of vertical
# -l 20 to control size of lines
# -hl 20 to control size of horizontal lines
# -p for percentage
# -b option as "before option"
# -hb to make new pane show up to the left of current one
# -f for full width (ignoring other panes)
# -t 1 splits pane 1
# debugging views with C-b q

#kill all sessions except current session:
#subprocess.run(["tmux", "kill-session", "-a"], check=True)
#tmux attach-session -t iorepl_tmux
#target a specific window in a specific session: separate them with a colon
#tmux send-keys -t foosession:foo.0 ls ENTER
