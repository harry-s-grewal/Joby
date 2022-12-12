import os

def ping_cmd(hostname, timeout):
    """Sends a ping command through the
       terminal in an OS-agnostic way
       without needing to run as admin.
    """
    cmd_identifier = "-c"

    os_name = os.name
    if os_name == "nt":
        cmd_identifier = "-n"

    packet_size = "1"
    cmd = " ".join(["ping", hostname, "-t", str(timeout)])
    print("This is the command:",cmd)
    response = os.system(cmd)
    if response == 0:
        return True
    else:
        return False