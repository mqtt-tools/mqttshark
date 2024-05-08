import shlex
import sys
import threading

import runs

import pytest
from strip_ansi import strip_ansi


def test_cli_version(capfd):
    """
    Verify `mqttshark --version` succeeds.
    """
    run_mqttshark("--version")
    out, err = capfd.readouterr()
    assert out.strip() == "mqttshark version 0.0.1"


def test_cli_capture(capfd, mosquitto):
    """
    Verify capturing a single MQTT PUBLISH succeeds.
    """
    interface_name = "lo"
    if sys.platform == "darwin":
        interface_name = "lo0"

    ev = threading.Event()
    def mqttshark():
        run_mqttshark(f"-i {interface_name}")
    t = threading.Thread(target=mqttshark)
    t.start()
    ev.wait(0.5)

    command = """mosquitto_pub -t 'testdrive' -m '{"temperature": 42.42}'"""
    runs.run(command)
    ev.wait(0.5)

    runs.run("sudo pkill tshark")
    ev.wait(0.25)

    out, err = capfd.readouterr()

    assert out is not None, "Captured output was expected, but it is empty"
    out = strip_ansi(out)
    assert 'CONNECT     clientid=""  keepalive=60  cleansession=True  protover=4' in out
    assert 'CONNACK     rc=0 (accepted)' in out
    assert 'PUBLISH(0)  retain=0  topic="testdrive"  payload="{"temperature": 42.42}"' in out
    assert 'DISCONNECT' in out


@pytest.mark.skipif(sys.version_info >= (3, 12), reason="Does not work on Python 3.12")
def test_cli_load_module(capsys):
    """
    Basic test function, loading `mqttshark` as Python module.
    This is too verbose!

    :param capsys:
    :return:
    """
    import imp

    command = "mqttshark --version"
    sys.argv[1:] = shlex.split(command)
    with pytest.raises(SystemExit):
        imp.load_source(name="mqttshark", pathname="mqttshark")
    out, err = capsys.readouterr()
    assert out.strip() == "mqttshark version 0.0.1"


def run_mqttshark(arguments):
    """
    Utility function to invoke `mqttshark`.

    :param arguments:
    :return:
    """
    command = f"sudo python mqttshark {arguments}"
    response = runs.run(command)
    return response
