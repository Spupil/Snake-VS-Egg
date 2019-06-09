import pygame, sys, random
from pygame.locals import *

pygame.init()
ScreenX = 500
ScreenY = 500
ScreenSize = (ScreenX, ScreenY)
Screen = pygame.display.set_mode(ScreenSize, 0, 32)
pygame.display.set_caption(" Snake Vs Egg")
Difficulty = 10

gx,gy=(0,0)


# 蛇
class snake():
    def __init__(self):
        self.Direction = K_RIGHT
        self.Body = []
        self.AddBody()
        self.AddBody()

    def AddBody(self):
        NewAddLeft, NewAddTop = (0, 0)
        if self.Body:
            NewAddLeft, NewAddTop = (self.Body[0].left, self.Body[0].top)
        NewAddBody = pygame.Rect(NewAddLeft, NewAddTop, 20, 20)
        if self.Direction == K_LEFT:
            if NewAddBody.left == 0:
                NewAddBody.left = 480
            else:
                NewAddBody.left -= 20
        elif self.Direction == K_RIGHT:
            if NewAddBody.left == 480:
                NewAddBody.left = 0
            else:
                NewAddBody.left += 20
        elif self.Direction == K_UP:
            if NewAddBody.top == 0:
                NewAddBody.top = 480
            else:
                NewAddBody.top -= 20
        elif self.Direction == K_DOWN:
            if NewAddBody.top == 480:
                NewAddBody.top = 0
            else:
                NewAddBody.top += 20
        self.Body.insert(0, NewAddBody)

    def DelBody(self):
        self.Body.pop()

    def IsDie(self):
        if self.Body[0] in self.Body[1:]:
            return True
        return False

    def Move(self):
        self.AddBody()
        self.DelBody()

    def ChangeDirection(self, Curkey):
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if Curkey in LR + UD:
            if (Curkey in LR) and (self.Direction in LR):
                return
            if (Curkey in UD) and (self.Direction in UD):
                return
            self.Direction = Curkey

# 食物
class food():
    def __init__(self):
        self.Obj = pygame.Rect(300,200, 20, 20)

    def Remove(self):
        self.Obj.x = 20

    def SendFood(self):
        if self.Obj.x == 20:
            AllPos = []
            for pos in range(20, ScreenX - 20, 20):
                AllPos.append(pos)
            self.Obj.left = random.choice(AllPos)
            self.Obj.top = random.choice(AllPos)

   


    

# 难度选择及游戏
def GameMain():
    global Difficulty
    FPSClock = pygame.time.Clock()
    Score = 100
    Life = 0

    Snake = snake()
    Food = food()

    BackgroungImg = pygame.image.load('1.jpg').convert()
    DifficultyChoiceImg = pygame.image.load('2.jpg').convert()

    ChoiceHintFont = pygame.font.SysFont('arial', 30)
    ChoiceFont = pygame.font.SysFont('arial', 180)
    # DifficultyChoice
    while True:
        IsChoice = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    IsChoice = True
                    break
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    Difficulty = Difficulty + 1
                elif event.key == K_DOWN:
                    if Difficulty > 1:
                        Difficulty = Difficulty - 1
        if IsChoice:
            break

        Screen.blit(DifficultyChoiceImg, (0, 0))
        ChoiceHintSurface = ChoiceHintFont.render('Snake can choose a difficulty', True, (0, 0, 0))
        Screen.blit(ChoiceHintSurface, (30, 110))
        ChoiceSurface = ChoiceFont.render(str(Difficulty), True, (0, 0, 0))
        Screen.blit(ChoiceSurface, (136, 150))
        EntranceHintSurface = ChoiceHintFont.render('Press Space to enter the game', True, (0, 0, 0))
        Screen.blit(EntranceHintSurface, (70, 350))
        pygame.display.update()

    ScoreFont = pygame.font.SysFont('arial', 30)
    LifeFont = pygame.font.SysFont('arial', 30)
    
    # main game loop
    while True:
        global gx,gy
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                Snake.ChangeDirection(event.key)
                if event.key==K_a:      #蛋的移动
                   gx-=20
                elif event.key==K_d:
                    gx+=20
                elif event.key==K_w:
                    gy-=20
                elif event.key==K_s:
                    gy+=20
            if event.type==KEYUP:
                if event.key==K_a:
                    gx=0
                if event.key==K_d:
                    gx=0
                if event.key==K_w:
                    gy=0
                if event.key==K_s:
                    gy=0
                   
            Food.Obj.left+=gx
            Food.Obj.top+=gy
            
            if Food.Obj.left>ScreenX-20:
                   Food.Obj.left=ScreenX-20
            if Food.Obj.left<0:
                   Food.Obj.left=0
            if Food.Obj.top>ScreenY-20:
                   Food.Obj.top=ScreenY-20
            if Food.Obj.top<0:
                   Food.Obj.top=0
                   
        Screen.blit(BackgroungImg, (0, 0))
        pygame.draw.rect(Screen, (0, 0, 0), Food.Obj, 0)
        Snake.Move()

    
        for rect in Snake.Body:
            pygame.draw.rect(Screen, (148,251,240), rect, 0)
        for rect in Snake.Body[1]:
            pygame.draw.rect(Screen,(255,76,108),(Snake.Body[1].left,Snake.Body[1].top,20,20),0)

        if Snake.IsDie():
            return Score
        if Food.Obj == Snake.Body[1]:
            return Life
     
        
        if Food.Obj == Snake.Body[0]:
            Score += Difficulty
            Life +=1
            Food.Remove()
            Snake.AddBody()

        Food.SendFood()

        ScoreSurface = ScoreFont.render(str(Score), True, (0, 0, 0))
        Screen.blit(ScoreSurface, (0, 0))
        LifeSurface = LifeFont.render(str(Life), True, (0, 0, 0))
        Screen.blit(LifeSurface, (480, 0))

       
        pygame.display.update()
        FPSClock.tick(Difficulty)

# 游戏结果
def GameResult(Score):
    GameResultBackgroundImg = pygame.image.load('3.jpeg').convert()
    ScoreHintFont = pygame.font.SysFont('arial', 35)
    ScoreFont = pygame.font.SysFont('arial', 180)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return True

        Screen.blit(GameResultBackgroundImg, (0, 0))
        ChoiceHintSurface = ScoreHintFont.render('Come up And Your Score is:', True, (0, 0, 0))
        Screen.blit(ChoiceHintSurface, (40, 110))
        ChoiceSurface = ScoreFont.render(str(Score), True, (0, 0, 0))
        Screen.blit(ChoiceSurface, (100, 150))
        EntranceHintSurface = ScoreHintFont.render('Space to restart', True, (0, 0, 0))
        Screen.blit(EntranceHintSurface, (50, 350))
        pygame.display.update()
        
def GameResultt(Life):
    GameResulttBackgroundImg = pygame.image.load('4.jpg').convert()
    LifeHintFont = pygame.font.SysFont('arial', 35)
    LifeFont = pygame.font.SysFont('arial', 180)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return True

        Screen.blit(GameResulttBackgroundImg, (0, 0))
        ChoiceHintSurface = LifeHintFont.render('Egg Win and Life Used', True, (0, 0, 0))
        Screen.blit(ChoiceHintSurface, (75, 50))
        ChoiceSurface = LifeFont.render(str(Life), True, (0, 0, 0))
        Screen.blit(ChoiceSurface, (190, 150))
        EntranceHintSurface = LifeHintFont.render('Space to restart', True, (0, 0, 0))
        Screen.blit(EntranceHintSurface, (120, 350))
        pygame.display.update()


if __name__ == '__main__':
      fin=True
      while f1:  #重启循环结构
        mid = GameMain()
        if mid>99:
           fin = GameResult(mid)
        elif mid<99:
           fin = GameResultt(mid)
        
    



