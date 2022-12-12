# Introduction

My take-home coding test for Joby Aviation.

# Summary

This is a script that pings IPs within a given range concurrently.
The script uses a predefined IP with its range, generates all
applicable IPs, and pings them concurrently using multi-threading.
The script saves the successes and failures of the pings in a
dictionary, then compares them - if an IP is pingable on one range
but not the other, that difference is printed out in the comparison.

# Configuration

To change the parameters of the script, edit the constants at the
top of `joby.py`. The parameters are listed here.

|  **Parameter**   |                                **Purpose**                                | **Type** | **Default Value** |         **Note**          |
| :--------------: | :-----------------------------------------------------------------------: | :------: | :---------------: | :-----------------------: |
|    IP_RANGE_1    |                        First range of IPs to ping                         |  String  |  192.168.1.0/24   | IP Address + Subnet Mask  |
|    IP_RANGE_2    |                        Second range of IPs to ping                        |  String  |  192.168.2.0/24   | IP Address + Subnet Mask  |
| OCTETS_TO_IGNORE |                         Last octet of IP address                          | [String] |      ["56"]       | Last 8 bits of IP address |
|   MAX_THREADS    |           Specifies max number of threads this script can spawn           |   int    |        512        |                           |
|  MAX_QUEUE_SIZE  |         Specifies max length of the queue that IPs are read into          |   int    |        100        |                           |
|   NUM_RETRIES    | Number of times a ping is retried for an IP before it's counted as a fail |   int    |         2         |                           |

# Testing

To run tests, open terminal and run `pytest -v`.

# Update to remove dependency on root priveleges

Originally to implement the ping I utilized a library titled `python-ping`.
`python-ping` requires root privileges, as do all `ping`
services. `ping` requests are sent as ICMP packets and require a
raw network socket to function. The creation of a raw network socket
requires admin rights - therefore a true ICMP `ping` cannot be done without
root privileges.

In `ping.py` I have created a `subprocess` that allows a `ping` only using
the onboard binaries. This was in an attempt to take advantage of the `setuid`
functionality of ping. In Linux, a `ping` command can be run by any user, as
the `setuid` allows `ping` to create a raw socket as root and continue as a
normal user. This works without root privileges on my Mac.

One of the downsides of using `subprocess` is that it's significantly slower
than the previous option. However, it's much faster than using `os.system` as
waiting for the response does not block the thread, allowing multithreading
to reduce execution time.

If `subprocess` doesn't work, the next option I can think of is a TCP ping;
That wouldn't require root, but it depends on whether the services you have
to test have a TCP port open.