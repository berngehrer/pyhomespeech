import subprocess

def runCommand(command, printError = False):
    status = -1
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = process.communicate() 
    status = process.wait()
    if status == 0:
        return status, output
    elif err:
        raise 
    return status, None
