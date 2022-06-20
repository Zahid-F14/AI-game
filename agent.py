from cmath import isfinite, isnan
from turtle import speed
import torch
import numpy as np
import random
from interface import Stategame,Direction,point
from collections import deque
from model import Qtrainer,Linear_QNet
from plot_helper import plot
import interface


state_color=['white','yellow','orange','red']
max_memory=100_000
batch=100
lr=.001

class Agent:
    def __init__(self):
        self.n_games=0
        self.epsilon=0 #randomness
        self.gamma=.5 #discount
        self.memory=deque(maxlen=max_memory)
        #model,trainer
        self.model=Linear_QNet(11,64,32,16,3)
        self.trainer=Qtrainer(self.model,lr=lr,gamma=self.gamma)
        


    def get_state(self,game):
        head=game.bot[0]
        point_l=point(head.x-20,head.y)
        point_r=point(head.x+20,head.y)
        point_u=point(head.x,head.y-20)
        point_d=point(head.x,head.y+20)

        dir_l=game.direction==Direction.LEFT
        dir_r=game.direction==Direction.RIGHT
        dir_u=game.direction==Direction.UP
        dir_d=game.direction==Direction.DOWN

        for i in range(len(game.state_arr)):
                if(game.state_arr[i].x!=-100):
                    if(state_color.index(game.Color[i])<=(int)(game.score/4)+1):
                        Target=i
                        break


        state=[
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_d and game.is_collision(point_d)) or
            (dir_u and game.is_collision(point_u)) ,

            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_d)) or
            (dir_l and game.is_collision(point_u)) ,

            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)) ,

            dir_l,
            dir_r,
            dir_u,
            dir_d,
            game.isFoodLeft(head),
            game.isFoodRight(head),
            game.isFoodDown(head),
            game.isFoodUp(head)


        ]
        #return np.array(state,dtype=float)
        #''',
        return np.array(state,dtype=float)

    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))

    def train_long_memory(self):
        if(len(self.memory)>batch):
            mini_sample=random.sample(self.memory,batch)
        else:
            mini_sample=self.memory
        
        for state,action,reward,next_state,done in mini_sample:
            self.trainer.train_step(state,action,reward,next_state,done)



    def train_short_memory(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)

    def get_action(self,state):
        self.epsilon=300-self.n_games
        final_move=[0,0,0]
        if random.randint(0,20)<self.epsilon:
            move=random.randint(0,2)
            final_move[move]=1
        else:
            interface.speed=30
            
            state0=torch.tensor(state,dtype=torch.float)
            prediction=self.model(state0)
            #print(prediction)
            move=torch.argmax(prediction).item()
            #print(move)
            final_move[move]=1
            #print(final_move)
            
        return final_move
def train():
    plot_score=[]
    plot_mean_score=[]
    total_score=0
    record=0
    agent=Agent()
    game=Stategame()
    while True:
        state_old=agent.get_state(game)
        #print(state_old)
        
        while True:
            if(np.isnan(state_old.astype(float).any())):
                state_old=agent.get_state(game)
            else:
                break
        final_move=agent.get_action(state_old)
        reward,done,score=game.play_step(final_move)

        state_new=agent.get_state(game)
        while True:
            if(np.isnan(state_new.astype(float).any())):
                state_new=agent.get_state(game)
            else:
                break
        if not (np.isnan(state_old.astype(float)).any() or np.isnan(state_new.astype(float)).any()):
            agent.train_short_memory(state_old,final_move,reward,state_new,done)
        #print(state_old,final_move,reward,state_new,done)


            agent.remember(state_old,final_move,reward,state_new,done)

        if done:

            game.reset()
            agent.n_games+=1
            agent.train_long_memory()
            
            if score>record:
                record=score
                agent.model.save()
            print('Game ',agent.n_games,'Score ',score,'Record ',record,'   ')
            plot_score.append(score)
            total_score+=score
            mean_score=total_score/agent.n_games
            plot_mean_score.append(mean_score)
            if agent.n_games==1000:
                break
            #plot(plot_score,plot_mean_score)

    

if __name__=='__main__':
    train()