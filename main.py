#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 10:12:59 2016

@author: juan
"""

import pyglet

import midi_dispatcher
from game_of_life import GameOfLife

import random

cell_size = 8
framerate = 30

class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(600,600)
        self.gameOfLife = GameOfLife(self.get_size()[0],self.get_size()[1],cell_size, 0.4)
        pyglet.clock.schedule_interval(self.update, 1.0/float(framerate))
        self.midiDispatcher = midi_dispatcher.MidiDispatcher()
        @self.midiDispatcher.midiInputHandler.event
        def on_pitch(pitch):
            #self.gameOfLife.drawCircle(random.uniform(-1, 1)*250 + 300, random.uniform(-1, 1)*250 +300)
            self.gameOfLife.run_rules()     #actualizo el juego con el teclado
            
    def on_draw(self):
        self.clear()
        self.gameOfLife.draw()
        
   
    
    def on_mouse_press(self,x, y, button, modifiers):
        self.gameOfLife.drawCircle(x,y)
    
    def update(self,dt):
        self.gameOfLife.run_rules()
        pass
        
if __name__ == "__main__":
    window = Window()
    pyglet.app.run()
      
      
        
