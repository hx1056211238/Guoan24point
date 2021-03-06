#!/usr/bin/env python

# Serial port testing

import serial

test_string = "Testing 1 2 3 4"

port_list = ["/dev/serial0", "/dev/ttyS0"]

for port in port_list:

    try:
        serialPort = serial.Serial(port, 115200, timeout = 2)
        print "Opened port", port, "for testing:"
        bytes_sent = serialPort.write(test_string)
        print "Sent", bytes_sent, "bytes"
        loopback = serialPort.read(bytes_sent)
        if loopback == test_string:
            print "Received", len(loopback), "valid bytes, Serial port", port, "working \n"
        else:
            print "Received incorrect data", loopback, "over Serial port", port, "loopback\n"
        serialPort.close()
    except IOError:
        print "Failed at", port, "\n"
