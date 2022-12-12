from unittest.mock import patch
from queue import Queue
from main import result, ping_ip


@patch("main.ping_cmd")
def test_ping_ip__happy_path(mock_ping):
    test_queue = Queue()
    test_result = result()
    num_retries = 2
    mock_ping.return_value = True

    test_queue.put("192.168.1.0")

    ping_ip(test_queue, test_result, num_retries)

    assert test_result.range_1.ping_success_dict['0']
