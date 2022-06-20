import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
pygame.init()
font = pygame.font.SysFont('arial', 25)
block_size = 20
speed = 200
state_color=['white','yellow','orange','red']


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


point = namedtuple('point', 'x,y')
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

yellow = (255, 255, 205)
statesx=[]
statesy=[]
color=[]



bot_color=state_color[0]


class Stategame:
    state_count=0
    cap_count=0
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('State Game')
        self.clock = pygame.time.Clock()
        self.reset()
        # init state
        

        
                      #point(self.head.x - block_size, self.head.y),
                      #point(self.head.x - (2 * block_size), self.head.y)]
        

    def reset(self):
        self.head = point(self.w / 2, self.h / 2)
        self.bot = [self.head]
        self.direction = Direction.RIGHT
        self.score2 = 0
        self.score=0
        
        self.state_arr=[]
        self.Color=color
        self.state_select()
        self.place_state()
        self.frame_iteration=0

    def state_select(self):
        
        for i in range(50):
            if(i<30):
                color.append(state_color[random.randint(0,3)])
            color.append(state_color[random.randint(0,3)])
    def place_state(self):
        
        for i in range(50):
            x = random.randint(0, (self.w - block_size) // block_size) * block_size
            y = random.randint(0, (self.h - block_size) // block_size) * block_size
            if (x in statesx) or (y in statesy):
                i-=1
                continue 
            if x > self.w - 2*block_size or x < 0+block_size or y > self.h - 2*block_size or y < 0+block_size:
                i-=1
                continue 
            else:
                statesx.append(x)
                statesy.append(y)
                ''' statesx.append(x+20)
                statesx.append(x-20)
                
                statesy.append(y)
                statesy.append(y)
                statesx.append(x)
                statesx.append(x)
                statesy.append(y+20)
                statesy.append(y-20)
                statesx.append(x+20)
                statesy.append(y+20)'''
               
            

        for i in range(len(statesx)):
            self.state_arr.append(point(statesx[i],statesy[i]))
            #print(statesx[i],statesy[i])
            self.state_count=len(self.state_arr)

    def move(self, action):
        clock_wise=[Direction.RIGHT,Direction.DOWN,Direction.LEFT,Direction.UP]
        idx=clock_wise.index(self.direction)

        if np.array_equal(action,[1,0,0]):
            new_dir=clock_wise[idx]
        elif np.array_equal(action,[0,1,0]):
            nxt_idx=(idx+1)%4
            new_dir=clock_wise[nxt_idx]
        else:
            nxt_idx=(idx-1)%4
            new_dir=clock_wise[nxt_idx]
        self.direction=new_dir
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += block_size
        elif self.direction == Direction.LEFT:
            x -= block_size
        elif self.direction == Direction.UP:
            y -= block_size
        elif self.direction == Direction.DOWN:
            y += block_size
        '''if x>self.w:
            x=0
        elif x<0:
            x=self.w
        if y>self.h:
            y=0
        elif y<0:
            y=self.h'''
        self.head = point(x, y)

    #def play_step(self):
    def play_step(self,action):
        self.frame_iteration+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            '''if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                if event.key == pygame.K_UP:
                    self.direction = Direction.UP
                if event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN'''

        #self.move(self.direction)
        self.move(action)
        reward=0
        
        self.bot.insert(0, self.head)
        game_over = False

        '''if self.head.x > self.w - block_size or self.head.x < 0 or self.head.y > self.h - block_size or self.head.y < 0 or (self.frame_iteration>100):
            game_over = True
            reward=-10
            return reward,game_over, self.score'''
        
        if self.is_collision():
            game_over=True
            reward=-10
            return reward,game_over,self.score
        
   
        if self.head in self.state_arr:
            
            #print(self.head)
            for i in range(len(self.state_arr)):
                if(self.state_arr[i].x==self.head.x):
                    if(self.state_arr[i].y)==self.head.y:
                        if(state_color.index(self.Color[i])<=(int)(self.score/4)+1):
                            self.state_arr[i]=self.state_arr[i]._replace(x=-100)
                            self.state_arr[i]=self.state_arr[i]._replace(y=-100)
                            self.score += 1
                            self.score2+=1
                            self.cap_count+=1
                            #print((int)(self.score2/4))
                        elif not (self.is_collision):
                            reward+=2
                            
                        #print(self.Color[i])
                            
                            #print(bot_color)
                        #print(self.Color[i])
            
        
        self.bot.pop()
        if (self.cap_count==self.state_count): 
            self.state_count=0
            self.cap_count=0
            self.score2=0 
            self.state_arr=[]           
            self.state_select()
            self.place_state()
            #print("done")
        #print("abc" ,self.cap_count,self.state_count," ")
        self.update_ui()
        self.clock.tick(speed)

        return reward,game_over, self.score

    def is_collision(self,pt=None):
        if pt==None:
            pt=self.head
        if pt.x > self.w - block_size or pt.x < 0 or pt.y > self.h - block_size or pt.y < 0: #or (self.frame_iteration>1000):
            return  True
        if pt in self.state_arr:
            for i in range(len(self.state_arr)):
                if(self.state_arr[i].x==self.head.x):
                    if(self.state_arr[i].y)==self.head.y:
                        if(state_color.index(self.Color[i])>(int)(self.score/4)+1):
                            return True

    def update_ui(self):
        self.display.fill(black)
        bot_color=state_color[min((int)(self.score/4),3)]
       
        for pt in self.bot:
            pygame.draw.rect(self.display, green, pygame.Rect(pt.x, pt.y, block_size, block_size))
            pygame.draw.rect(self.display, bot_color, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
        for i in range(len(self.state_arr)):
            pygame.draw.rect(self.display, self.Color[i], pygame.Rect(self.state_arr[i].x, self.state_arr[i].y, block_size, block_size))
        text = font.render("Score= " + str(self.score2), True, white)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def isFoodLeft(self,head2):
        x2=head2.x
        y2=head2.y

        pt=point(x2-20,y2)
        if pt in self.state_arr:
            for i in range(len(self.state_arr)):
                if(self.state_arr[i].x==self.head.x):
                    if(self.state_arr[i].y)==self.head.y:
                        if(state_color.index(self.Color[i])<=(int)(self.score/4)+1):
                            return True

        return False

    def isFoodRight(self,head2):
        x2=head2.x
        y2=head2.y

        pt=point(x2+20,y2)
        if pt in self.state_arr:
            for i in range(len(self.state_arr)):
                if(self.state_arr[i].x==self.head.x):
                    if(self.state_arr[i].y)==self.head.y:
                        if(state_color.index(self.Color[i])<=(int)(self.score/4)+1):
                            return True
        return False


    def isFoodUp(self,head2):
        x2=head2.x
        y2=head2.y

        pt=point(x2,y2-20)
        if pt in self.state_arr:
            for i in range(len(self.state_arr)):
                if(self.state_arr[i].x==self.head.x):
                    if(self.state_arr[i].y)==self.head.y:
                        if(state_color.index(self.Color[i])<=(int)(self.score/4)+1):
                            return True
        return False


    def isFoodDown(self,head2):
        x2=head2.x
        y2=head2.y

        pt=point(x2,y2+20)
        if pt in self.state_arr:
            for i in range(len(self.state_arr)):
                if(self.state_arr[i].x==self.head.x):
                    if(self.state_arr[i].y)==self.head.y:
                        if(state_color.index(self.Color[i])<=(int)(self.score/4)+1):
                            return True
        return False



