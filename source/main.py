def Main():
    import pygame
    pygame.init()
    res_x = 900
    res_y = 900
    window = pygame.display.set_mode((res_x, res_y))
    pygame.display.set_caption("main")
    ####################################################

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_ESCAPE]:
            sys.exit        


        window.fill((0,0,0))
        pygame.display.flip()

Main()