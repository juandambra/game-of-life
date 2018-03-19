#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 11:16:27 2016

@author: juan
"""

import random
import pyglet

class GameOfLife:
    def __init__(self, height,width, cell_size, probability):
        self.grid_width = int(width/cell_size)
        self.grid_height = int(height/cell_size)
        self.cell_size = cell_size
        self.probability = probability
        self.cells = []
        self.generate_cells()
        
    def generate_cells(self):
        def randomBlock(probability):
            if probability > 1 or probability < 0:
                probability = 0.5
            if random.random() < probability:
                return 1
            else:
                return 0
        
        self.cells = [[randomBlock(self.probability) for row in range(0, self.grid_width)] for column in range(0,self.grid_height)]
    
    def drawPoint(self, x, y):
        self.cells[int(x/self.cell_size)][int(y/self.cell_size)] = 1
        #self.cells[int(x/self.cell_size)][int(y/self.cell_size)+1] = 1
        #self.cells[int(x/self.cell_size)+1][int(y/self.cell_size)] = 1
        #self.cells[int(x/self.cell_size+1)][int(y/self.cell_size)+1] = 1
        #self.cells[int(self.cell_size*100*x/self.grid_width)][int(self.cell_size*100*y/self.grid_height)] = 1
    
    def drawCircle(self, x, y):
        self.cells[int(x/self.cell_size)+2][int(y/self.cell_size)] = 1
        self.cells[int(x/self.cell_size)+1][int(y/self.cell_size)+1] = 1
        self.cells[int(x/self.cell_size)][int(y/self.cell_size)+2] = 1
        self.cells[int(x/self.cell_size)-1][int(y/self.cell_size)+1] = 1
        self.cells[int(x/self.cell_size)-2][int(y/self.cell_size)] = 1
        self.cells[int(x/self.cell_size)-1][int(y/self.cell_size)-1] = 1
        self.cells[int(x/self.cell_size)][int(y/self.cell_size)-2] = 1
        self.cells[int(x/self.cell_size)+1][int(y/self.cell_size)-1] = 1
        
        
    def run_rules(self):
        def getSubmodule(x,y, matrix):
            submodule = []
            for i in range(0,3):
                submodule.append([])
                for j in range(0,3):
                    xpos = x+i-1
                    ypos = y+j-1
                    if (xpos < 0) or (xpos  > len(matrix)-1) or (ypos < 0) or (ypos > len(matrix)-1):
                        val = 0
                    else:
                        val = matrix[xpos][ypos]
                    submodule[i].append(val)
            return submodule
        
        def analyzeSubmodule(submodule):
            def center(submodule):
                return submodule[1][1]
            
            def neighbours(submodule):
                total = 0
                for i in range(0,3):
                    total += submodule[i].count(1)
                return total - submodule [1][1]
                            
            def alter(submodule):
                submodule[1][1] = not submodule[1][1]
                
            neighboursAmount = neighbours(submodule)
            if center(submodule):           #if center is 1
                if neighboursAmount > 3 or neighboursAmount < 2:
                    alter(submodule)
            else:
                if neighbours(submodule) == 3:
                    alter(submodule)
            return center(submodule)
            
            
        def checkNeighbours(x,y,matrix):
            count = 0
            length = len(matrix)
            for i in range(-1,2):
                for j in range(-1,2):
                    if x+i > 0 and x+i < length and y+1 >= 0 and y+j < length:
                        count += matrix[i+x][j+y]
            count -= matrix[x][y]
            if matrix[x][y]:           #if center is 1
                if count > 3 or count < 2:
                    return 0
            else:
                if count == 3:
                    return 1
            return matrix[x][y]
            
        nextGrid = []
        for x in range(0, self.grid_width):
            nextGrid.append([])
            for y in range(0, self.grid_height):
                nextGrid[x].append(checkNeighbours(x,y,self.cells))
                #submodule = getSubmodule(x,y,self.cells)
                #nextGrid[x].append(analyzeSubmodule(submodule))
        self.cells = nextGrid
        
                
    def draw(self):
        for x in range(0,self.grid_width):
            for y in range(0,self.grid_height):
                if self.cells[x][y]:
                    coordinates = (x * self.cell_size, y* self.cell_size,
                                   x * self.cell_size, y* self.cell_size + self.cell_size,
                                   x * self.cell_size + self.cell_size, y* self.cell_size,
                                   x * self.cell_size + self.cell_size, y* self.cell_size + self.cell_size)
                    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,[0,1,2,1,2,3],("v2f", coordinates))