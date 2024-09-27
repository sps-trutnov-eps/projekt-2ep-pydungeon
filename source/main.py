def Main():
    import pygame
    pygame.init()
    res_x = 900
    res_y = 900
    window = pygame.display.set_mode((res_x, res_y))
    pygame.display.set_caption("main")
    #####
    x_player = 320
    y_player = 320
    velocity_player = 0.5


    ####################################################

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_ESCAPE]:
            sys.exit        

        if key_press[pygame.K_w]:
            y_player -= velocity_player
        if key_press[pygame.K_s]:
            y_player += velocity_player
        if key_press[pygame.K_a]:
            x_player -= velocity_player
        if key_press[pygame.K_d]:       
            x_player += velocity_player


        window.fill((0,0,0))
        pygame.draw.rect(window ,(255,255,255), (x_player, y_player, 60, 60))
        
        pygame.display.flip()

Main()