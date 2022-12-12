import ipaddress
from ping import ping_cmd
from threading import Thread, Lock
from queue import Queue

IP_RANGE_1 = '192.168.1.0/24'
IP_RANGE_2 = '192.168.2.0/24'
OCTETS_TO_IGNORE = ["56"]
MAX_THREADS = 512
MAX_QUEUE_SIZE = 100
NUM_RETRIES = 2


class result:
    """Store the results of the pings, and have a separate
        lock for each dictionary
    """

    def __init__(self):
        self.range_1 = self.results_dict_with_mutex()
        self.range_2 = self.results_dict_with_mutex()

    class results_dict_with_mutex:
        def __init__(self):
            self.lock = Lock()
            self.ping_success_dict = {}


def ping_ip(q, results, retries):
    """Pings the ip received from the queue and
        stores the result in a thread-safe way
    """
    ip = str(q.get())
    success = False
    for i in range(retries):
        if ping_cmd(ip, timeout=2):
            success = True
            break

    ip_split = ip.split(".")

    if ip_split[2] == "1":  # Use network ID to separate range
        result = results.range_1
    elif ip_split[2] == "2":
        result = results.range_2

    result.lock.acquire()
    result.ping_success_dict[ip_split[-1]] = success
    result.lock.release()
    q.task_done()


def multithread_loop(q, results, retries=1):
    while True:
        ping_ip(q, results, retries)


def ping_from_queue(ip_queue, results, num_retries, max_threads=255):
    for i in range(max_threads):
        t = Thread(target=multithread_loop, args=(
            ip_queue, results, num_retries,))
        t.setDaemon(True)
        t.start()


def main():
    iprange1 = ipaddress.ip_network(IP_RANGE_1)
    iprange2 = ipaddress.ip_network(IP_RANGE_2)

    ip_queue = Queue(maxsize=MAX_QUEUE_SIZE)
    results = result()

    ping_from_queue(ip_queue=ip_queue, results=results,
                    num_retries=NUM_RETRIES, max_threads=MAX_THREADS)

    for ip in iprange1:
        if str(ip).split(".")[-1] in OCTETS_TO_IGNORE:
            continue
        ip_queue.put(ip)

    for ip in iprange2:
        if str(ip).split(".")[-1] in OCTETS_TO_IGNORE:
            continue
        ip_queue.put(ip)

    ip_queue.join()

    for key in results.range_1.ping_success_dict.keys():
        if key not in results.range_2.ping_success_dict:
            continue
        value_range_1 = results.range_1.ping_success_dict[key]
        value_range_2 = results.range_2.ping_success_dict[key]
        if value_range_1 != value_range_2:
            print("Discrepancy with ip suffix " + key)
            print("Is IP 192.168.1." + key +
                  " pingable: " + str(value_range_1) + " \n")
            print("Is IP 192.168.1." + key +
                  " pingable: " + str(value_range_2) + " \n")


if __name__ == '__main__':
    main()
