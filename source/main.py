import pygame
import sys
import math


class Projectile:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.vel = 10  # rychlost kulky
        self.radius = 5 # velikost kulky

    def movement(self):
        self.x += math.cos(self.angle) * self.vel
        self.y += math.sin(self.angle) * self.vel

    def draw(self, window):
        pygame.draw.circle(window, (255, 0, 0), (int(self.x), int(self.y)), self.radius)

    def despawn(self, res_x, res_y): # despawn kulky m
        return self.x < 0 or self.x > res_x or self.y < 0 or self.y > res_y

#####################################

def Main():
    pygame.init()
    res_x = 1100
    res_y = 800
    window = pygame.display.set_mode((res_x, res_y))
    pygame.display.set_caption("main")
    clock = pygame.time.Clock()


    x_player = 320
    y_player = 320
    velocity_player = 5

    projektily = []


    cooldown = 200  # cooldown zbraně
    last_shot_time = 0 

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Získání aktuálního času
        current_time = pygame.time.get_ticks()

        # Střelba projektilů při kliknutí myší
        if pygame.mouse.get_pressed()[0] and current_time - last_shot_time >= cooldown:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Vypočítání úhlu střelby
            rel_x, rel_y = mouse_x - (x_player + 30), mouse_y - (y_player + 30)
            angle = math.atan2(rel_y, rel_x)
            projektily.append(Projectile(x_player + 30, y_player + 30, angle))
            last_shot_time = current_time  # čas posledního výstřelu

        # Pohyb hráče
        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_ESCAPE]:
            sys.exit()

        if key_press[pygame.K_w]:
            y_player -= velocity_player
        if key_press[pygame.K_s]:
            y_player += velocity_player
        if key_press[pygame.K_a]:
            x_player -= velocity_player
        if key_press[pygame.K_d]:
            x_player += velocity_player

        window.fill((0, 0, 0))


        for projektil in projektily[:]:
            projektil.movement()
            projektil.draw(window)


            if projektil.despawn(res_x, res_y):
                projektily.remove(projektil)


        pygame.draw.rect(window, (255, 255, 255), (x_player, y_player, 60, 60))
        pygame.display.flip()

Main()
