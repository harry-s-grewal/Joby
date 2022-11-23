from mock import patch
from queue import Queue
from main import result, ping_ip
from pythonping.executor import ResponseList


@patch("pythonping.ping")
@patch.object(ResponseList, 'success')
def test_ping_ip__happy_path(mock_ping, mock_response):
    test_queue = Queue()
    test_result = result()
    num_retries = 2
    mock_ping.return_value = mock_response
    mock_response.return_value = True

    test_queue.put("192.168.1.0")

    ping_ip(test_queue, test_result, num_retries)

    assert test_result.range_1.ping_success_dict['0']
