from ping import ping_cmd

def test_ping_cmd():
    assert ping_cmd(hostname="192.168.0.1", timeout=1)
