import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import math
import time
pygame.init()
font = pygame.font.SysFont('arial.ttf',25)

# Reset 
# Reward
# Play(action) -> Direction
# Game_Iteration
# is_collision


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    NONE = 5
 
Point = namedtuple('Point','x , y')

BLOCK_SIZE=20
SPEED = 200
WHITE = (255,255,255)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)

def getDistance(pt1, pt2):
    dist = (abs(pt1.x - pt2.x) + abs(pt1.y - pt2.y))/20
    return dist

class SnakeGameAI:
    def __init__(self,w=120,h=120):
        self.w=w
        self.h=h
        #init display
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        #init game state
        self.reset()
    def reset(self):
        self.direction = Direction.NONE
        self.action = self.direction
        self.head = Point(self.w/2,self.h/2)
        self.score = 0
        self.food = None
        self.foodHp = 10
        self._place__food()
        self.frame_iteration = 0
      

    def _place__food(self):
        x = random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        self.foodHp = 10
        if(self.food == self.head):
            self._place__food()

    def _eat_food(self):
        self.foodHp -=1
        self.score += 1
        if self.foodHp <= 0:
            self._place__food()


    def play_step(self,action):
        self.frame_iteration+=1
        # 1. Collect the user input
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                quit()
            
        # 2. Move
        prevDistance = getDistance(self.head, self.food)
        self._do(action)
        newDistance = getDistance(self.head, self.food)

        # 3. Check if game Over
        reward = 0  # eat food: +10 , game over: -10 , else: 0
        game_over = False 
        if self.is_collision():
            game_over=True
            reward = -20
            return reward,game_over,self.score

        if (newDistance == 1) and (self.action == [0, 0, 0, 0, 1]):
            reward = 5
            self._eat_food()
            # time.sleep(1)
        else:
            reward = ((prevDistance - newDistance) - 1)*2 - (4 if (self.action == [0, 0, 0, 0, 1]) else 0)
        
        # 5. Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. Return game Over and Display Score
        
        return reward,game_over,self.score

    def _update_ui(self):
        self.display.fill(BLACK)
        pygame.draw.rect(self.display,BLUE1,pygame.Rect(self.head.x,self.head.y,BLOCK_SIZE,BLOCK_SIZE))
        pygame.draw.rect(self.display,BLUE2,pygame.Rect(self.head.x+4,self.head.y+4,12,12))
        pygame.draw.rect(self.display,RED,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))
        text = font.render("Score: "+str(self.score),True,WHITE)
        text2 = font.render("hp: "+str(self.foodHp),True,WHITE)
        self.display.blit(text,[0,0])
        self.display.blit(text2,[0,30])
        pygame.display.flip()

    def _do(self,action):
        self.action = action

        x = self.head.x + (action[3] - action[1]) *  BLOCK_SIZE
        y = self.head.y + (action[0] - action[2]) * BLOCK_SIZE
        self.head = Point(x, y)

    def is_collision(self,pt=None):
        if(pt is None):
            pt = self.head
        #hit boundary
        if(pt.x>self.w-BLOCK_SIZE or pt.x<0 or pt.y>self.h - BLOCK_SIZE or pt.y<0):
            return True
        return False
