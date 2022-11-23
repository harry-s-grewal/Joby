import ipaddress
from pythonping import ping
from threading import Thread, Lock
from queue import Queue

MAX_THREADS = 512
NUM_RETRIES = 2
MAX_QUEUE_SIZE = 100
OCTETS_TO_IGNORE = ["56"]
IP_RANGE_1 = '192.168.1.0/24'
IP_RANGE_2 = '192.168.2.0/24'


class result:
    def __init__(self):
        self.range_1 = self.results_dict_with_mutex()
        self.range_2 = self.results_dict_with_mutex()

    class results_dict_with_mutex:
        def __init__(self):
            self.lock = Lock()
            self.ping_success_dict = {}


def ping_ip(q, results, retries=1):
    while True:
        ip = str(q.get())
        success = False
        for i in range(retries):
            if ping(ip, timeout=2).success():
                success = True
                break

        ip_split = ip.split(".")

        if ip_split[2] == "1":
            result = results.range_1
        elif ip_split[2] == "2":
            result = results.range_2

        result.lock.acquire()
        result.ping_success_dict[ip_split[-1]] = success
        result.lock.release()
        q.task_done()


def ping_from_queue(ip_queue, results, num_retries, max_threads=255):
    for i in range(max_threads):
        t = Thread(target=ping_ip, args=(ip_queue, results, num_retries,))
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':

    iprange1 = ipaddress.ip_network(IP_RANGE_1)
    iprange2 = ipaddress.ip_network(IP_RANGE_2)

    ip_queue = Queue(maxsize=MAX_QUEUE_SIZE)
    results = result()

    ping_from_queue(ip_queue=ip_queue, results=results, num_retries=NUM_RETRIES,
                    max_threads=MAX_THREADS)

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

        continue
