import pygame
from src.game import Game
from os import path

mygame = Game()
mygame.dir = path.dirname(__file__)

while True:
	mygame.main()
	#mygame.handle_input()