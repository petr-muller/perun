import subprocess

__author__ = 'Tomas Fiedor'


def run_external_command(cmd_args):
    """
    Arguments:
        cmd_args(list): list of external command and its arguments to be run

    Returns:
        bool: return value of the external command that was run
    """
    print("Running the following process: {}".format(cmd_args))
    process = subprocess.Popen(" ".join(cmd_args), shell=True)
    process.wait()
    return process.returncode
