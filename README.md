#### Robust tmux panes

1. Do you have network issues?
2. Do you need to monitor multiple program outputs?
3. Do you have a use case for tmux panes?

Then consider ~~stealing~~ using this code to workaround 1, use for 2 or adjust for 3.
This is a working example, for which process names and ports are altered.

Functionality and explanation from ./iorepl.py:
```py
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
```

Without network issues, you can use
```py
runres = subprocess.run(command)
assert(runres == 0)
```
and remove all `time.sleep(0.2)` and `time.sleep(0.05)`.
