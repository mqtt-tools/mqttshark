# mqttshark - MQTT formatter for tshark

mqttshark will run tshark, the terminal network packet capture tool, and
attempt to pretty print any MQTT messages received.

It can decode MQTT packets tunnelled over WebSockets, and can decode TLS
packets when pre-keys are available.

mqttshark requires at least Python 3.6, and possibly something more recent than
that. It also requires tshark to be installed.

## Usage

Run listening to port 1883 on the first non-loopback network interface:

```
mqttshark
# Run a test
mosquitto_sub -h test.mosquitto.org -t '$SYS/broker/uptime' -t sub-2 -U unsub-1 -U unsub-2 \
	-q 2 -V 5 --will-topic will-topic --will-payload payload
```

![example output](example.png)

Run on a specific network interface:
```
mqttshark -i eth0
```

Further examples:

```
mqttshark -p 1234:mqtt # Listen on port 1234, decoding as MQTT
mqttshark -p 1234:mqtts --tls-keylog <file> # Listen on port 1234, decoding as MQTT over TLS.
mqttshark -p 1234:ws # Listen on port 1234, decoding as WebSockets
mqttshark -p 1234:mqtts --tls-keylog <file> # Listen on port 1234, decoding as MQTT over WebSockets over TLS.
mqttshark -p 1883:mqtt,8883:mqtts,8080:ws,8081:wss # Listen on multiple ports
```

There are lots of ways of choosing how to display the output and suppress /
pick which packets to display, see the help:
```
mqttshark -h
```

## Display

This explains the meaning of some of the output:

![display output](details.png)


## Bugs

* Will properties are not displayed - this seems to be a missing feature in tshark
* Payloads with new lines may cause problems

## Contact

https://github.com/ralight/mqttshark
