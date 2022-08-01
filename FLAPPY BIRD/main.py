from operator import truediv
import random #for generating random numbers and generating the pipe layout for the game
import sys
from turtle import window_width #system will exit which means that the game will close
import pygame
from pygame.locals import *
 #global variable
FPS=32
Screenwidth=289
Screenlength=511
screen=pygame.display.set_mode((Screenwidth,Screenlength)) #
Game_sprites={}
Game_sounds={}
elevation=Screenlength*0.8
pipeimage ='images/pipe.png'
background_image ='images/background.jpg'
birdplayer ='images/bird.png'
sealevel_image = 'images/base.jfif'


def flappygame():
         score = 0
         horizontal = int(Screenwidth/5)
         vertical = int(Screenlength/2)
         ground = 0
         basex=0
         mytempheight = 100
         # Generating two pipes for blitting on window
         first_pipe = createPipe()
         second_pipe = createPipe()
         upper_pipe=[
             {'x':Screenwidth+200,'y':first_pipe[0]['y']},
             {'x':Screenwidth+200+(Screenwidth/2),'y':second_pipe[0]['y']}]
         lower_pipe=[
             {'x':Screenwidth+200,'y':first_pipe[1]['y']},
             {'x':Screenwidth+200+(Screenwidth/2),'y':second_pipe[1]['y']}]
         pipevelx=-4 #birdvelocity
         playervelY=-9
         playermaxvelY=10
         playerminvelY=-8
         playeraccy= 1

         playerFlapAccY=-8 #velocity while flapping 
         birdflapped=False # ture only when the bird starts flying
         while True:
             for event in pygame.event.get():
                 if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                  pygame.quit()
                  sys.exit()
                 if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                     if vertical>0:
                         playervelY=playerFlapAccY
                         birdflapped=True

             game_over=is_collide(horizontal,vertical,upper_pipe,lower_pipe)
             if game_over:
                 return True
             
             #we will be checking for score
             player_mid=horizontal + Game_sprites['bird'].get_width()/2
             for pipe in upper_pipe:
                 pipe_mid=pipe['x']+Game_sprites['pipe'][0].get_width()/2       
                 if pipe_mid<=player_mid<pipe_mid+4:
                      score=score+1
                      print(f"your score is {score}") 
             if playervelY<playermaxvelY and not birdflapped:
                  playervelY+=playeraccy
             if birdflapped:
                 birdflapped=False
             playerHeight = Game_sprites['bird'].get_height()
             vertical = vertical +  min(playervelY, elevation - vertical - playerHeight)
             #movimng pipes to the left
             for up,lp in zip(upper_pipe,lower_pipe):
                 up['x']+=pipevelx
                 lp['x']+=pipevelx
             #if pipe is out of the screen,remove it
             if upper_pipe[0]['x']< -Game_sprites['pipe'][0].get_width():
                 upper_pipe.pop(0)
                 lower_pipe.pop(0)
             #if the pipe is about to be removed add a new pipe beforehand
             if 0<upper_pipe[0]['x']<5:
                 newpipe=createPipe()
                 upper_pipe.append(newpipe[0])
                 lower_pipe.append(newpipe[1])
             # we will start blitting our screens now
             screen.blit(Game_sprites['background'],(0,0))
             screen.blit(Game_sprites['sea_level'],(basex,elevation))
             screen.blit(Game_sprites['bird'],(horizontal,vertical))
             for up,lp in zip(upper_pipe,lower_pipe):
                 screen.blit(Game_sprites['pipe'][0],(up['x'],up['y']))
                 screen.blit(Game_sprites['pipe'][1],(lp['x'],lp['y']))
             numbers = [int(x) for x in list(str(score))]
             width = 0
             for num in numbers:
                 width += Game_sprites['scores'][num].get_width()
                 Xoffset = (Screenwidth - width)/2
             for num in numbers:
                  screen.blit(Game_sprites['scores'][num], (Xoffset,Screenlength*0.12))
                  Xoffset += Game_sprites['scores'][num].get_width()
              # Refreshing the game window and displaying the score.
             pygame.display.update() 
             # Set the framepersecond
             FPS_clock.tick(FPS)

 #will help us in returning the upper pipe and lower pipe locations

def createPipe():
         pipeHeight=Game_sprites['pipe'][0].get_height() #gets height of the pipe
         offset=Screenlength/3  #it is the upper third part of the screen
         y2=offset+random.randrange(0,int(Screenlength-Game_sprites['sea_level'].get_height()-1.2*offset)) # helps in having random pipe lenghts
         pipex=Screenwidth+10
         y1=pipeHeight-y2+offset
         pipe = [
             {'x':pipex,'y':-y1},#upper pipe
             {'x':pipex,'y':y2}]#lower pipe
         return pipe


def is_collide(h,v,up,lp):
     return False


if __name__=="__main__":
     pygame.init() #helps in initializing the modules of pygame
     FPS_clock=pygame.time.Clock() #helps in controlling the fps of the game
     pygame.display.set_caption("Flappy Bird by Laksh Sekhri")
     Game_sprites["scores"]=( pygame.image.load('images/0.png').convert_alpha(),  #will load all images in required pixels using convert_alpha
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),        
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha())
     Game_sprites['bird']=pygame.image.load(birdplayer).convert_alpha()
     Game_sprites['background']=pygame.image.load(background_image).convert_alpha()
     Game_sprites['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()
     Game_sprites['pipe']=(
     pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(),180), #rotates the pipe by 180 so we can get upper pipe
     pygame.image.load(pipeimage).convert_alpha()
     ) #lower pipe
    
     while True:
        horizontal = int(Screenwidth/5)
        vertical = int((Screenlength - Game_sprites['bird'].get_height())/2)
        basex=0
        while True:
            #if the user wants to leave the game
            for event in pygame.event.get():
                if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                  pygame.quit()
                  sys.exit()
                elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                     flappygame()
                else:
                    screen.blit(Game_sprites['background'],(0,0))
                    screen.blit(Game_sprites['bird'],(horizontal,vertical))
                    screen.blit(Game_sprites['sea_level'],(basex,elevation))
                    #Refreshes the screen and displays the the screens
                    pygame.display.update()
                    #helps in controlling fps
                    FPS_clock.tick(FPS)

