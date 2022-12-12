"""Ping module utilizing system ping binary in an OS agnostic way."""
import os
from subprocess import Popen, PIPE

def ping_cmd(hostname, timeout):
    """Sends a ping command through the
       terminal in an OS-agnostic way
       without needing to run as admin.
    """
    os_modifier = "-c"

    os_name = os.name
    if os_name == "nt": # AKA Windows
        os_modifier = "-n"
    packet_size = "1"
    cmd = ["ping", os_modifier, packet_size, hostname, "-t", str(timeout)]

    response = Popen(cmd, stdout=PIPE)
    response.wait()

    if response.poll():
        return False
    return True
