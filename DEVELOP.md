# mqttshark - development sandbox


## Setup

Acquire sources.
```shell
git clone https://github.com/mqtt-tools/mqttshark
cd mqttshark
```

Install prerequisites into Python virtualenv.
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install --requirement requirements-tests.txt
```

## Tests

Run software tests.
```shell
source .venv/bin/activate
pytest
```
