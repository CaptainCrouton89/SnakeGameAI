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
    def __init__(self,w=200,h=200):
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
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE,self.head.y),
                      ]
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
        if(self.food in self.snake):
            self._place__food()

    def _eat_food(self):
        self.foodHp -=1
        print("eating food!!!")
        self.score += 1
        if self.foodHp < 0:
            self.score += 10
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
        self.snake.insert(0,self.head)
        self.snake.pop()

        print(self.action)

        # 3. Check if game Over
        reward = 0  # eat food: +10 , game over: -10 , else: 0
        game_over = False 
        if self.is_collision():
            game_over=True
            reward = -10
            return reward,game_over,self.score
        
        print(prevDistance - newDistance)

        if (newDistance == 1) and (self.action == Direction.NONE):
            reward = 10
            self._eat_food()
        elif (self.action == Direction.NONE):
            reward = -1
        else:
            reward = (prevDistance - newDistance) - 1
        
        # 5. Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. Return game Over and Display Score
        
        return reward,game_over,self.score

    def _update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(self.display,BLUE1,pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(self.display,BLUE2,pygame.Rect(pt.x+4,pt.y+4,12,12))
        pygame.draw.rect(self.display,RED,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))
        text = font.render("Score: "+str(self.score),True,WHITE)
        text2 = font.render("hp: "+str(self.foodHp),True,WHITE)
        self.display.blit(text,[0,0])
        self.display.blit(text2,[0,30])
        pygame.display.flip()

    def _do(self,action):
        # Action
        # [1,0,0] -> Straight
        # [0,1,0] -> Right Turn 
        # [0,0,1] -> Left Turn

        clock_wise = [Direction.RIGHT,Direction.DOWN,Direction.LEFT,Direction.UP,Direction.NONE]
        idx = clock_wise.index(self.direction)
        new_dir = self.direction
        if np.array_equal(action,[1,0,0,0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action,[0,1,0,0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right Turn
        elif np.array_equal(action,[0,0,1,0]):
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # Left Turn
        else:
            new_dir = Direction.NONE

        self.action = new_dir

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if(self.direction == Direction.RIGHT):
            x+=BLOCK_SIZE
        elif(self.direction == Direction.LEFT):
            x-=BLOCK_SIZE
        elif(self.direction == Direction.DOWN):
            y+=BLOCK_SIZE
        elif(self.direction == Direction.UP):
            y-=BLOCK_SIZE
        self.head = Point(x,y)

    def is_collision(self,pt=None):
        if (self.action == Direction.NONE): return False
        if(pt is None):
            pt = self.head
        #hit boundary
        if(pt.x>self.w-BLOCK_SIZE or pt.x<0 or pt.y>self.h - BLOCK_SIZE or pt.y<0):
            return True
        if(pt in self.snake[1:]):
            return True
        return False
