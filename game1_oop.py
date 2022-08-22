import pygame
from copy import copy

WIDTH = 900
HEIGHT = 900
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Will you ever finish this game")
FPS = 60


rect_dic_house = {}

class main_option_box():
    main_rect = pygame.Rect(0, 800, 900, 200)
    color = ((52, 192, 235))
    sub_options = []
    
    def increment_pos(self):
        self.main_rect.y += 10
    
    def decrement_pos(self):
        self.main_rect.y -= 10
    
    def check(self, mouse_pos):
        if self.main_rect.y <= 900 and mouse_pos[1] < 800:
            self.increment_pos()
            for sub in self.sub_options:
                sub.increment_pos()
        elif self.main_rect.y > 800:
            self.decrement_pos()
            for sub in self.sub_options:
                sub.decrement_pos()

class sub_house_box(main_option_box):
    current_obj = None
    main_rect = pygame.Rect(0, 900, 900, 200)
    flag = False
    color = (224, 255, 48)
    close = False
    sub_options = []
    
    def check(self):
        if not sub_house_box.close and self.main_rect.y > 800:
            self.decrement_pos()
            for sub in sub_house_box.sub_options:
                sub.decrement_pos()

        elif sub_house_box.close:
            self.increment_pos()
            for sub in sub_house_box.sub_options:
                sub.increment_pos()
            if self.main_rect.y == 900:
                sub_house_box.close = False
                sub_house_box.flag = False
                sub_house_box.current_obj = None

class sub_option_box(main_option_box):
    main_rect = pygame.Rect(50, 825, 50, 50)
    color = (90, 91, 92)

    def __init__(self):
        self.add_into_main()

    def add_into_main(self):
        self.sub_options.append(self)

    def increment_pos(self):
        self.main_rect.y += 10
    
    def decreament_pos(self):
        self.main_rect.y -= 10

class sub_option_house(sub_option_box):
    color = (90, 91, 92)

    def action(self):
        self.color = (255, 0, 0)
        shadow.length = sub_house.length
        shadow.height = sub_house.height
        shadow.current_button = self
        shadow.flag = True
        shadow.current_action = shadow.shadow_house
        shadow.main_rect = copy(pygame.Rect(0, 0, sub_house.length, sub_house.height))

    def reset(self):
        self.color = sub_option_house.color

class sub_house_box_option_path(sub_house_box):
    main_rect = pygame.Rect(50, 925, 50, 50)
    color = (90, 91, 92)

    def __init__(self):
        self.add_into_main()

    def add_into_main(self):
        self.sub_options.append(self)

    def increment_pos(self):
        self.main_rect.y += 10
    
    def decrement_pos(self):
        self.main_rect.y -= 10
    
    def action(self):
        self.color = (255, 0, 0)

class shadow():
    main_rect = None
    current_button = None
    flag = False
    current_action = None
    end = False

    def shadow_house(mouse_position):
        
        shadow.main_rect.x = mouse_position[0]
        shadow.main_rect.y = mouse_position[1]
        pygame.draw.rect(WINDOW, sub_house.shadow_color, shadow.main_rect)

        if shadow.end:
            sub_house.create(mouse_position)
            shadow.current_button.reset()
            shadow.current_button = None
            shadow.flag = False
            shadow.current_action = None
            shadow.end = False


class sub_house():
    length = 100
    height = 100
    main_rect = pygame.Rect(0, 0, length, height)
    color = (255, 94, 94)
    shadow_color = (255, 179, 179)

    def __init__(self, mouse_position):
        self.main_rect.x = mouse_position[0]
        self.main_rect.y = mouse_position[1]
        rect_dic_house[self] = copy(self.main_rect)
    
    def update(self):
        pygame.draw.rect(WINDOW, self.color, rect_dic_house[self])

    def delete(self):
        del rect_dic_house[self]
        del self

    @classmethod
    def create(cls, mouse_position):
        return cls(mouse_position)


def actions(mouse_pos, option_box):
    if shadow.flag:
        shadow.end = True
    
    elif mouse_pos[1] >= 800:
        if sub_house_box.flag:
            for sub in sub_house_box.sub_options:
                if sub.main_rect.collidepoint(mouse_pos):
                    sub.action()
        else:
            for sub in option_box.sub_options:
                if sub.main_rect.collidepoint(mouse_pos):
                    sub.action()
    
    else:
        for rect in rect_dic_house:
            if rect_dic_house[rect].collidepoint(mouse_pos):
                if sub_house_box.flag and rect == sub_house_box.current_obj:
                    sub_house_box.close = True
                else:
                    sub_house_box.flag = True
                
                sub_house_box.current_obj = rect
                     
def draw_window(sub_house_box, option_box, mouse_position):
    WINDOW.fill((255, 255, 255))

    for rect in rect_dic_house:
        rect.update()

    if not sub_house_box.flag:
        option_box.check(mouse_position)
        pygame.draw.rect(WINDOW, option_box.color, option_box.main_rect)
        for sub in option_box.sub_options:
            pygame.draw.rect(WINDOW, sub.color, sub.main_rect) 

    else:
        sub_house_box.check()
        pygame.draw.rect(WINDOW, sub_house_box.color, sub_house_box.main_rect)
        for sub in sub_house_box.sub_options:
            pygame.draw.rect(WINDOW, sub.color, sub.main_rect)
    if shadow.flag:
        shadow.current_action(mouse_position)

    pygame.display.update()

def main():
    option_box = main_option_box()
    sub_box_1 = sub_option_house()
    sub_house_box_1 = sub_house_box()
    sub_house_box_option_path_1  = sub_house_box_option_path()

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            mouse_position = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                actions(mouse_position, option_box)

        draw_window(sub_house_box_1, option_box, mouse_position)
    
    pygame.quit()

if __name__ == "__main__":
    main()