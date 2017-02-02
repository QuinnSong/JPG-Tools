#coding=utf-8  
import pygame  
from sys import exit  
from pygame.locals import *  
  
BACK_WIDTH=300 #����ͼ���  
BACK_HEIGHT=230 #����ͼ�߶�  
  
pygame.init()  
screen = pygame.display.set_mode((BACK_WIDTH, BACK_HEIGHT), 0, 32)  
  
background = pygame.image.load('water_surface.jpg') #wave_bk.png') #��ȡ����ͼƬ  
clock = pygame.time.Clock()  
  
buf1 = [[0 for col in range(BACK_WIDTH)] for row in range(BACK_HEIGHT)] #�������1  
buf2 = [[0 for col in range(BACK_WIDTH)] for row in range(BACK_HEIGHT)] #�������2  
  
canvas = pygame.Surface((BACK_WIDTH, BACK_HEIGHT))  
  
def update(delta):  
    global buf1, buf2  
      
    for row in range(1, BACK_HEIGHT - 1):  
        for col in range(1, BACK_WIDTH - 1):  
            buf2[row][col] = ((buf1[row][col+1]+buf1[row][col-1]+buf1[row+1][col]+buf1[row-1][col])>>1) - buf2[row][col]    #x0'=(x1+x2+x3+x4)/2-x0  
            buf2[row][col] -= (buf2[row][col] >> 5) #����˥�� 1/32  
                  
    buf1, buf2 = buf2, buf1 # swap  
          
    canvas.lock()  
    for row in range(0, BACK_HEIGHT):  
        for col in range(0, BACK_WIDTH):  
            if row == 0 or row == BACK_HEIGHT - 1 or col == 0 or col == BACK_WIDTH - 1:  
                canvas.set_at((col, row), background.get_at((col, row)))  
            else:      
                #���Ƶ���ˮ����ĳ���ǰ����������Ĳ���֮��������������ˮ�׾����ƫ����(ģ������)  
                xoff = buf1[row][col+1]-buf1[row][col-1]  
                yoff = buf1[row+1][col]-buf1[row-1][col]  
                newCol = int(col+xoff)  
                newRow = int(row+yoff)  
                if newCol < 0:  
                    newCol = 0  
                if newCol > BACK_WIDTH-1:  
                    newCol = BACK_WIDTH-1  
                if newRow < 0:  
                    newRow = 0  
                if newRow > BACK_HEIGHT-1:  
                    newRow = BACK_HEIGHT-1  
                canvas.set_at((col, row), background.get_at((newCol, newRow)))       
      
    canvas.unlock()    
    screen.blit(canvas, (0,0))  
      
while True:  
    for event in pygame.event.get():  
        if event.type == QUIT:  
            exit()          
          
        if event.type == MOUSEBUTTONDOWN:  
            x, y = pygame.mouse.get_pos()  
            buf1[y][x] = -120 #�������λ���������  
              
    # ֡�ʿ���  
    time_passed = clock.tick(30)  
      
    update(time_passed)  
         
    pygame.display.update() 