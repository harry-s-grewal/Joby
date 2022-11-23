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
