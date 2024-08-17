import pygame
import os
from Main_code.Frontend import Draw_pieces, draw_board, draw_big_pieces, Winner
def Quit_game(pos_v):
    """Quits the game"""
    quit()

def go_left(pos_v):
    """The next position if the player wants to go left"""
    x,y,z,a=pos_v
    if x ==0:
            pos_v=(x+720,y,z,a)
    else:
            pos_v=(x-90,y,z,a)
    return pos_v


def go_right(pos_v):
    """The next position if the player wants to go right"""
    x,y,z,a=pos_v
    if x ==720:
            pos_v=(x-720,y,z,a)
    else:
            pos_v=(x+90,y,z,a)
    return pos_v

def go_down(pos_v):
    """The next position if the player wants to go down"""
    x,y,z,a=pos_v
    if y ==720:
            pos_v=(x,y-720,z,a)
    else:
            pos_v=(x,y+90,z,a)
    return pos_v


def go_up(pos_v):
    """The next position if the player wants to go up"""
    x,y,z,a=pos_v
    if y ==0:
            pos_v=(x,y+720,z,a)
    else:
            pos_v=(x,y-90,z,a)
    return pos_v

    
def place(pos_v,box):
    """The next position if the player wants to play the move"""
    if box== None:
        xx,yy=360,360
    else:
        y,x= box[0]
        yy=x*90
        xx=y*90
    pos_v=(xx,yy,90,90)
    return pos_v
