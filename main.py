import pygame
import random
pygame.init()
clock=pygame.time.Clock()
fps=60
bottom_panel=150 #for panel
screen_width=800
screen_height=400+bottom_panel
screen=pygame.display.set_mode((screen_width,screen_height))  #screen
pygame.display.set_caption('Battle') #title
running=True
background_img=pygame.image.load('./img/Background/background.png').convert_alpha()
panel_img=pygame.image.load('./img/Icons/panel.png').convert_alpha()
sword_img=pygame.image.load('./img/Icons/sword.png').convert_alpha()
potion_img=pygame.image.load('./img/Icons/potion.png').convert_alpha()
font=pygame.font.SysFont('Times New Roman',26)
red=(255,0,0)
green=(0,255,0)

#define game var
current_fighter=1
total_fighter=3
action_cooldown=0
action_wait_time=90
attack=False
potion=False
clicked=False
game_over=0 #-1 bandits win 1=knight win



def draw_text(text,font,text_col,x,y):
    imgt=font.render(text,True,text_col)
    screen.blit(imgt,(x,y))

def draw_background():
    screen.blit(background_img,(0,0))

def draw_panel():
    screen.blit(panel_img,(0,screen_height-bottom_panel))
    draw_text(f'{knight.name} HP:{knight.hp}',font,red,100,(screen_height-bottom_panel)+10)
    count=0
    for bandits in bandit_list:
        draw_text(f'{bandits.name} HP:{bandits.hp}', font, red,550, ((screen_height - bottom_panel) + 10)+count*60)
        count+=1






class fighter():
    # constructor
    def __init__(self,x,y,name,max_hp,strength,potions):
        self.name=name
        self.max_hp=max_hp
        self.hp=max_hp #change
        self.strength=strength
        self.start_potions=potions #change
        self.potions=potions
        self.alive=True
        self.animation_list=[]
        self.frame_index=0
        self.action=0 #0=idle 1=attack 2=hurt 3=dead

        self.update_time=pygame.time.get_ticks()
        self.reset_time=pygame.time.get_ticks()
        #idle animation
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'./img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #attack animation
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'./img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)

        self.animation_list.append(temp_list)
        #hurt
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'./img/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)

        self.animation_list.append(temp_list)
        #death
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f'./img/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)

        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def update(self):
        animation_cooldown=100
        self.image=self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks()-self.update_time>animation_cooldown:
            self.update_time=pygame.time.get_ticks()
            self.frame_index+=1
        if self.frame_index>=len(self.animation_list[self.action]):
            if self.action==3:
                self.frame_index=len(self.animation_list[self.action])-1
            else:
                self.idle()





























    def idle(self):
         self.action = 0
         self.frame_index = 0
         self.update_time = pygame.time.get_ticks()









    def attack(self,target):
        rand=random.randint(-5,5)
        damage=self.strength+rand
        target.hp-=damage
        target.hurt()
        if target.hp<1:
            target.hp=0
            target.alive=False
            target.death()
        self.action=1
        self.frame_index=0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)
class HealthBar():
    def __init__(self,x,y,hp,max_hp):
        self.x=x
        self.y=y
        self.hp=hp
        self.max_hp=max_hp
    def drawHealth(self,hp):
        self.hp=hp
        ratio=self.hp/self.max_hp
        pygame.draw.rect(screen,red,(self.x,self.y,150,20))
        pygame.draw.rect(screen,green, (self.x, self.y, 150*ratio, 20))

class potion():
    def __init__(self,x,y,hp,max_hp):
        self.x=x;
        self.y=y;
        self.hp=hp;
        self.max_hp=max_hp
    def drawpotion(self):
        pygame.draw.rect(screen, red, (self.x, self.y,200,50))




knight=fighter(200,260,'Knight',30,50,3)
bandit1=fighter(550,270,'Bandit',20,6,1)
bandit2=fighter(700,270,'Bandit',20,6,1)
bandit_list=[]
bandit_list.append(bandit1)
bandit_list.append(bandit2)
knight_health_bar=HealthBar(100,screen_height-bottom_panel+40,knight.hp,knight.max_hp)
bandit1_health_bar=HealthBar(550,screen_height-bottom_panel+40,bandit1.hp,bandit1.max_hp)
bandit2_health_bar=HealthBar(550,screen_height-bottom_panel+100,bandit2.hp,bandit2.max_hp)
knight_potion=potion(300,screen_height-bottom_panel+200,knight.hp,knight.max_hp);








while running:
    clock.tick(fps)
    draw_background()
    draw_panel()
    knight_health_bar.drawHealth(knight.hp)
    bandit1_health_bar.drawHealth(bandit1.hp)
    bandit2_health_bar.drawHealth(bandit2.hp)
    knight_potion.drawpotion()
    knight.update()
    knight.draw()
    for bandit in bandit_list:
        bandit.update()
        bandit.draw()
    #player actions
    attack=False
    potion=False
    target=None
    pos=pygame.mouse.get_pos()
    bandits_count=0
    pygame.mouse.set_visible(True)
    for bandits in bandit_list:
        if bandits.rect.collidepoint(pos):
            pygame.mouse.set_visible(False)
            screen.blit(sword_img,pos)
            if clicked and bandits.alive:
                attack=True
                target=bandit_list[bandits_count]
        bandits_count+=1

    if knight.alive:
        if current_fighter==1:
            action_cooldown+=1
            if action_cooldown>=action_wait_time:
                #ready to attack
                if attack and target!=None:
                    knight.attack(target)
                    current_fighter += 1
                    action_cooldown = 0
    else:
        game_over=-1 #bandits win




    #enemy ai
    bandit_count=0
    for bandit in bandit_list:
        if current_fighter==2+bandit_count:
            if bandit.alive:
                action_cooldown+=1
                if action_cooldown>=action_wait_time:
                    bandit.attack(knight)
                    current_fighter+=1
                    action_cooldown = 0
            else:
                current_fighter += 1
        bandit_count+=1

    if current_fighter>total_fighter:
        current_fighter=1
    alive_bandits=0
    for bandits in bandit_list:
        if bandits.alive:
            alive_bandits=alive_bandits+1

    if alive_bandits == 0:
        game_over = 1  # knight win

    if game_over==-1:
        draw_text(f'YOU ARE DEAD', font, red,300,0)
    elif game_over==1:
        draw_text(f'VICTORY!!!', font, red, 300, 0)






    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            clicked=True
        else:
            clicked=False
    pygame.display.update()



pygame.quit()









