#!/usr/bin/env python
#
# test_midiin_callback.py
#
"""Shows how to receive MIDI input by setting a callback function."""

import logging
import sys
import time

import pyglet
import rtmidi       #using python.rtmidi

log = logging.getLogger('test_midiin_callback')
logging.basicConfig(level=logging.DEBUG)


class MidiInputHandler(pyglet.event.EventDispatcher):
    def __init__(self, port=0):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        if message[0] == 144:
            self.dispatch_event('on_pitch', message[1])
            print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))

MidiInputHandler.register_event_type('on_pitch')

class MidiDispatcher(pyglet.event.EventDispatcher):
    def __init__(self):
        port = sys.argv[1] if len(sys.argv) > 1 else None
        try:
            self.midiin = rtmidi.MidiIn(name="game")
            available_ports = self.midiin.get_ports()
            if available_ports:
                self.midiin.open_port(0)
            else:
                self.midiin.open_virtual_port("My virtual output")
        except (EOFError, KeyboardInterrupt):
            sys.exit()
        self.midiInputHandler = MidiInputHandler(port)
        self.midiin.set_callback(self.midiInputHandler)

    def close(self):
        self.midiin.close_port()
        del self.midiin

