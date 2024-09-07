import pygame
from os.path import join
from random import randint, uniform

# to do
# 1. Main Menu
# 2. Pause Screen
# 3. Player HP Bar
# 4. Player Death Menu
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

        # mask
        self.mask = pygame.mask.from_surface(self.image)

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        self.rect.clamp_ip(pygame.Rect(0, 0, WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5))

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites, laser_sprites), laser_surface, self.rect.midtop)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH),randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.original_surface = surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.life_time = 2000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint(400,500)
        self.rotation_speed = randint(50, 100)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

        if pygame.time.get_ticks() - self.start_time >= self.life_time:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surface, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplostion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

def collisions():
    # collisions
    global running, kills
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, False, pygame.sprite.collide_mask)

    if collision_sprites:
        update_highscore_kills(kills)
        running = False

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplostion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()
            kills += 1
def dispay_score():
    current_time = pygame.time.get_ticks() // 1000
    text_surf = font.render(str(current_time), True, (255, 255, 255))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (255, 255, 255), text_rect.inflate(20,30).move(0, -6), 4, 5)

def display_kills():
    text_surf = font2.render(f'Kills: {kills}', True, (255,255,255))
    text_rect = text_surf.get_frect(topleft = (10,10))
    display_surface.blit(text_surf, text_rect)

def display_highscore():
    global HIGHSCORE_KILLS

    text_surf = font2.render(f'Highest Kills : {HIGHSCORE_KILLS}', True, (255, 255, 255))
    text_rect = text_surf.get_frect(midtop = (WINDOW_WIDTH/2, 10))
    display_surface.blit(text_surf, text_rect)

def update_highscore_kills(new_score):
    global HIGHSCORE_KILLS
    if new_score > HIGHSCORE_KILLS:
        HIGHSCORE_KILLS = new_score

    with open('highscore.py', 'w') as file:
        file.write(f"HIGHSCORE_KILLS = {HIGHSCORE_KILLS}")

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
kills = 0
clock = pygame.time.Clock()
highscore_content = {}
with open('highscore.py', 'r') as file:
    exec(file.read(), highscore_content)

HIGHSCORE_KILLS = highscore_content['HIGHSCORE_KILLS']

# imports
meteor_surface = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surface = pygame.image.load(join('images', 'laser.png')).convert_alpha()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)
font2 = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 20)
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
laser_sound.set_volume(0.1)

explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
explosion_sound.set_volume(0.1)

# damage_sound = pygame.mixer.Sound(join('audio', 'damage.ogg'))
# damage_sound.set_volume(0.1)

game_music = pygame.mixer.Sound(join('audio', 'game_music.wav'))
game_music.set_volume(0.1)
game_music.play(loops = -1)

# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000   #clock.tick() returns delta time in milliseconds so we divide by 1000 to get in seconds

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor((all_sprites, meteor_sprites), meteor_surface, (x, y))

    # update
    all_sprites.update(dt)

    collisions()

    # draw the game
    display_surface.fill('#3a2e3f')
    dispay_score()
    display_kills()
    display_highscore()
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()