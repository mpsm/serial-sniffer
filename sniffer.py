#!/usr/bin/env python
import sys
import serial
import select
import os
import binascii

def usage():
    sys.stderr.write("Usage: " + sys.argv[0] + " <app_pts> <serial>\n")

def serial_open(name):
    print "Opening " + name
    return serial.Serial(name)

if __name__ == "__main__":
    try:
        outname = sys.argv[1]
        inname = sys.argv[2]
    except:
        usage()
        sys.exit(1)

    serout = serial_open(outname)
    serin = serial_open(inname)
    fds = [serout.fileno(), serin.fileno()]
    print "File descriptors " + " ".join([str(fd) for fd in fds])
    serial_map = {serout.fileno(): [serout, "OUT", serin], serin.fileno(): [serin, "IN", serout]}

    while True:
       readable,_,_ = select.select(fds, [], [])
       for r in readable:
            s = ""
            ser = serial_map[r][0]
            while ser.inWaiting() > 0:
                c = ser.read(ser.inWaiting())
                if c is None or c == '': break
                s += c

            print serial_map[r][1] + " : " + binascii.hexlify(s)
            serial_map[r][2].write(s)
        
