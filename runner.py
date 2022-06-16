import pygame
from sys import exit
from random import randint,choice

# classes
class Player(pygame.sprite.Sprite):
    # PLAYER'S MAIN FEATURES
    def __init__(self):
        super().__init__()

        # WALK FEATURES
        walk_frame1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()        
        walk_frame2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [walk_frame1,walk_frame2]
        self.player_index = 0

        # JUMP FEATURES
        self.jump_frame = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.05)

        # PLAYER SPRITE
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
    
    # PLAYER KEY INPUT / JUMP
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >=300 :
            self.gravity = -20
            self.jump_sound.play()

    # PLAYER GRAVITY
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    # PLAYER ANIMATION
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.jump_frame
        else:
            self.player_index += 0.15

            if self.player_index >= len(self.player_walk):
                self.player_index = 0

            self.image = self.player_walk[int(self.player_index)]

    # PLAYER UPDATE FUNCTION
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    # OBSTACLE SPRITES
    def __init__(self, enemy_type):
        super().__init__()

        if enemy_type == 'snail':
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1,snail_frame2]
            y_pos = 300
        else:
            fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame1,fly_frame2]
            y_pos = 150
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
    
    # OBSTACLES ANIMATION
    def animation_state(self):
        self.animation_index += 0.2
        if self.animation_index >= len(self.frames):
            self.animation_index=0
        self.image = self.frames[int(self.animation_index)]
    
    # CLEAR LIST (obstacles outside the screen)
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    
    # OBSTACLES UPDATE
    def update(self):
        self.animation_state()
        self.rect.x -= game_speed

# functions

def colision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = text_font.render(f'{current_time}',True,'black')
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

pygame.init()

# BASIC GAME FEATURES
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
text_font = pygame.font.Font('font/PixelType.ttf',50)
game_active = False
start_time = 0
score = 0
game_speed = 6

# Background Features
sky = pygame.image.load('graphics/Sky.png').convert_alpha()
ground = pygame.image.load('graphics/ground.png').convert_alpha()
bg_Music = pygame.mixer.Sound('audio/music.wav')
bg_Music.set_volume(0.05)
bg_Music.play(loops= -1)

# TITLE SCREEN FEATURES
stand_suf = pygame.transform.scale2x(pygame.image.load('graphics/player/player_stand.png')).convert_alpha()
stand_rect = stand_suf.get_rect(center = (400,200))
game_name = text_font.render('PIXEL RUNNER',True,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))
game_message = text_font.render('Press SPACE to Run',True,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,320))
restart_message = text_font.render('Press SPACE to Run again!',True,(111,196,169))
restart_message_rect = restart_message.get_rect(center = (400,350))

# PLAYER DEF
player = pygame.sprite.GroupSingle()
player.add(Player())

# OBSTACLE DEF
obstacle_group = pygame.sprite.Group()
obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer,1200)

# GAME LOOP
while True:
    for event in pygame.event.get():
        # QUIT Game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        # start game
        if game_active == False:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)

        # OBSTACLE GENERATOR EVENT
        if game_active == True:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','fly','snail','snail','snail'])))

    if game_active == True: # Playing Game
        screen.blit(sky,(0,0))
        screen.blit(ground,(0,300))
        score = display_score()

        # add player to the screen
        player.draw(screen)
        player.update()

        # add obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # stop the game when collide
        game_active = colision_sprite()

    # TITLE SCREEN
    else:
        screen.fill((94,129,162))
        screen.blit(stand_suf,stand_rect)
        screen.blit(game_name,game_name_rect)
        
        score_message = text_font.render(f'Your score: {score}',True,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,300))

        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)
            screen.blit(restart_message,restart_message_rect)

    pygame.display.update() # set to display screen
    clock.tick(60) # set frame rate