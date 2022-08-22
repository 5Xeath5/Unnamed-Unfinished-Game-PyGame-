import pygame

WIDTH = 900
HEIGHT = 900
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Will you ever finish this game")
FPS = 60

sub_option_group = pygame.sprite.Group()
shadow_group = pygame.sprite.Group()
house_group = pygame.sprite.Group()

class main_option(pygame.sprite.Sprite):
    main_rect = pygame.Rect(0, 800, 900, 200)
    color = ((52, 192, 235))

    def increment_pos(self):
        self.main_rect.y += 10
    
    def decrement_pos(self):
        self.main_rect.y -= 10
    
    def check(self, mouse_pos):
        if self.main_rect.y <= 900 and mouse_pos[1] < 800:
            self.increment_pos()
            for sub in sub_option_group.sprites():
                sub.follow(True)
        elif self.main_rect.y > 800:
            self.decrement_pos()
            for sub in sub_option_group.sprites():
                sub.follow(False)

class sub_option(main_option):
    def follow(self, flag):
        if flag:
            self.increment_pos()
        else:
            self.decrement_pos()

    def update(self):
        pygame.draw.rect(WINDOW, self.color, self.main_rect) 

class sub_option_house(sub_option):
    main_rect = pygame.Rect(50, 825, 50, 50)
    color = (90, 91, 92)

    def action(self):
        self.color = (255, 0, 0)
        shadow_group.add(shadow_house())

    
class sub_option_2(sub_option):
    main_rect = pygame.Rect(150, 825, 50, 50)
    color = (90, 91, 92)


class sub_option_3(sub_option):
    main_rect = pygame.Rect(250, 825, 50, 50)
    color = (90, 91, 92)


class sub_option_4(sub_option):
    main_rect = pygame.Rect(350, 825, 50, 50)
    color = (90, 91, 92)

class house(pygame.sprite.Sprite):
    main_rect = pygame.Rect(0, 0, 100, 100)
    color = (255, 94, 94)
    shadow_color = (255, 179, 179)
    
    def __init__(self, x_cord, y_cord):
        super().__init__()
        self.main_rect = pygame.Rect.copy(house.main_rect)
        self.main_rect.y = y_cord
        self.main_rect.x = x_cord

    def update(self):
        pygame.draw.rect(WINDOW, self.color, self.main_rect)

class shadow(pygame.sprite.Sprite):
    
    def mov(self, mouse_pos):
        pixel_y = mouse_pos[1] - (mouse_pos[1]%10)
        pixel_x = mouse_pos[0] - (mouse_pos[0]%10)
        self.main_rect.y = pixel_y
        self.main_rect.x = pixel_x

    def update(self, mouse_pos):
        self.mov(mouse_pos)
        pygame.draw.rect(WINDOW, self.color, self.main_rect)

class shadow_house(shadow):
    main_rect = pygame.Rect.copy(house.main_rect)
    color = house.shadow_color
    
    def action(self):
        sub_option_group.sprites()[0].color = sub_option_house.color
        current_shadow = shadow_group.sprites()[0]
        house_group.add(house(current_shadow.main_rect.x, current_shadow.main_rect.y))
        shadow_group.remove(self)
        print


def actions(mouse_pos):
    if mouse_pos[1] >= 800:
        for sub in sub_option_group.sprites():
            if sub.main_rect.collidepoint(mouse_pos):
                sub.action()
                return 
    elif shadow_group.sprites():
        for shadow in shadow_group.sprites():
            shadow.action()
            return

def draw_window(main_box, mouse_pos):
    WINDOW.fill((255,255,255))

    main_box.check(mouse_pos)

    if shadow_group.sprites():
        for shadow in shadow_group.sprites():
            shadow.update(mouse_pos)
        
    if house_group.sprites():
        for house in house_group.sprites():
            house.update()

    pygame.draw.rect(WINDOW, main_box.color, main_box.main_rect)
    sub_option_group.update()
    pygame.display.update()

def main():
    main_box = main_option()

    sub_1 = sub_option_house()
    sub_2 = sub_option_2()
    sub_3 = sub_option_3()
    sub_4 = sub_option_4()
    sub_option_group.add(sub_1)
    sub_option_group.add(sub_2)
    sub_option_group.add(sub_3)
    sub_option_group.add(sub_4)

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                actions(mouse_pos)
            
        draw_window(main_box, mouse_pos)
    pygame.quit()

if __name__ == "__main__":
    main()