#!/usr/bin/env python
import sys
import serial
import select
import os
import binascii
import time

class CrossedStream(object):
    def __init__(self, ser, other):
        self.ser = ser
        self.other = other

    def __str__(self):
        return self.ser.name + " <-> " + self.other.name

    def name(self):
        return self.ser.name

    def process(self):
        s = ""
        while self.ser.inWaiting() > 0:
            c = self.ser.read(self.ser.inWaiting())
            if c is None or c == '': break
            s += c

        self.other.write(s)
        return s

def usage():
    sys.stderr.write("Usage: " + sys.argv[0] + " <app_pts> <serial>\n")

def serial_open(name):
    print "Opening " + name
    return serial.Serial(name)

def data_print(cr, data):
    print "[" + time.asctime() + " | " + cr.name() + "]\t" + binascii.hexlify(data)

def sniff(open_func = serial_open, print_func = data_print):
    serout = open_func(outname)
    serin = open_func(inname)
    crout = CrossedStream(serout, serin)
    crin = CrossedStream(serin, serout)
    fds = [serout.fileno(), serin.fileno()]

    serial_map = {serout.fileno(): crout, serin.fileno(): crin}

    while True:
       readable,_,_ = select.select(fds, [], [])
       for r in readable:
           cr = serial_map[r]
           print_func(cr, cr.process())

if __name__ == "__main__":
    try:
        outname = sys.argv[1]
        inname = sys.argv[2]
    except:
        usage()
        sys.exit(1)

    sniff()
        
