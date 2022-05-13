import os, re, pathlib, sys

# Gets user input with message showing current directory
def get_input():
    curr_dir = str(pathlib.Path(__file__).parent.resolve()) # Get the current directory
    return input(curr_dir + " % ") # Display current directory and % when getting user input


# Determines if command is cd and executes it if so
def cd_command(command):
    if command[0] == 'cd':
        if len(command) > 1: # If we have a directory to change to
            try: os.chdir(command[1]); return True
            except: os.write(1, ("Directory does not exist\n").encode())
        else: print("Missing arguments, please enter the directory you want to change to")
    return False # This boolean is used to indicate that we need to process further since the command wasn't a cd


# Used to run 'simple' commands that don't involve pipes or redirects
def run_simple_command(command):
    process = os.fork()
    if process < 0: os.write(1, ("Error starting process\n").encode()) # Error forking
    elif process == 0:
        for dir in re.split(":", os.environ['PATH']): # Look for command in path
            try: os.execve(dir + "/" + command[0], command, os.environ)
            except: pass # Just pass so we can try out different directories
        os.write(1, ("Error running command: " + command[0] + " command not found\n").encode()); exit() 
    else: os.wait() # Wait for child to finish and clean up

# Used to run commands that involve a redirect
def run_redirect_command(command):
    process = os.fork()
    if process < 0: os.write(1, ("Error starting process\n").encode()) # Error forking
    elif process == 0:
        os.close(1) # Redirect child's stdout
        os.open(command[2], os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1, True)
        for dir in re.split(":", os.environ['PATH']): # Look for command in path
            try: os.execve(dir + "/" + command[0], [command[0]], os.environ)
            except: pass # Just pass so we can try out different directories
        os.write(2, ("Error running command: " + command + " command not found\n").encode()); sys.exit()
    else: os.wait() # Wait for child to finish and clean up

# Used to run commands that involve a pipe TODO: Add actual pipe command in this bitch TODO:
def run_pipe_command(command):
    process = os.fork()
    if process < 0: os.write(1, ("Error starting process\n").encode()) # Error forking
    elif process == 0:
        os.close(1) # Redirect child's stdout
        os.open('pipe.txt', os.O_CREAT | os.O_WRONLY) # I will use pipe.txt as a buffer
        os.set_inheritable(1, True)
        for dir in re.split(":", os.environ['PATH']): # Look for command in path
            try: os.execve(dir + "/" + command[0], [command[0]], os.environ)
            except: pass # Just pass so we can try out different directories
        os.write(2, ("Error running command: " + command + " command not found\n").encode()); sys.exit()
    else: 
        os.wait() # Wait for child to finish and clean up
        run_simple_command([command[2], 'pipe.txt']) # 


# Logic to determine what type of command is recieved and how to process it 
def process_command(command):
    if command.strip() == 'exit': exit() # Look for exit command, even if floating between whitespace
    command = command.split() # Transform command into string list
    if not cd_command(command):
            if len(command) == 3 and command[1] == ">": run_redirect_command(command)
            elif len(command) == 3 and command[1] == "|": run_pipe_command(command)
            else: run_simple_command(command)


# Basic loop of getting and executing commands
def main():
    print('')
    while(1):
        command = get_input()
        process_command(command)

main()