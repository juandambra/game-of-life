
import pyglet
import jack
import binascii


#NOTEON = 0x9
#NOTEOFF = 0x8
class MidiDispatcher(pyglet.event.EventDispatcher):
    def __init__(self):
        self.client = jack.Client('MIDI-Monitor')
        self.port = self.client.midi_inports.register('input')

        @self.client.set_process_callback
        def process(frames):
            for offset, data in self.port.incoming_midi_events():
                #print('{0}: 0x{1}'.format(self.client.last_frame_time + offset,
                #                  binascii.hexlify(data).decode()))

                message = binascii.hexlify(data).decode()
                if message != 'f8':
                    #print(message)
                    status, pitch, vel = bytes(data)
                    if status == 144:
                        print(pitch)
                        self.dispatch_event('on_pitch', pitch)

MidiDispatcher.register_event_type('on_pitch')