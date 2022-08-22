import pygame

WIDTH = 900
HEIGHT = 900


WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Will you ever finish this game")

WINDOW.fill((255, 255, 255))

FPS = 60

print(pygame.mouse.get_visible())

def draw_window(building_rect, house_option):
    WINDOW.fill((255, 255, 255))
    pygame.draw.rect(WINDOW,(52, 192, 235), building_rect)
    pygame.draw.rect(WINDOW, (90, 91, 92), house_option)
    pygame.display.update()

def option_box(mouse_pos, building_rect, building_rect_sub):
    if building_rect.y <= 900 and mouse_pos[1] < 800:
        building_rect.y += 10
        for sub_box in building_rect_sub:
            sub_box.y += 10
    elif building_rect.y > 800:
        for sub_box in building_rect_sub:
            sub_box.y -= 10
        building_rect.y -= 10

def main():
    building_rect = pygame.Rect(0, 800, 900, 200)
    house_option = pygame.Rect(building_rect.x+50, building_rect.y+25, 50, 50)
    building_rect_sub = [house_option]

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            mouse_position = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if house_option.collidepoint(mouse_position):
                    pass


        
        option_box(mouse_position, building_rect, building_rect_sub)
        draw_window(building_rect, house_option)

    pygame.quit()


if __name__ == '__main__':
    main()