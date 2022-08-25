import pygame

WIDTH = 900
HEIGHT = 900
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Will you ever finish this game")
FPS = 60

sub_option_group = pygame.sprite.Group()
shadow_group = pygame.sprite.Group()
house_group = pygame.sprite.Group()
house_option_group = pygame.sprite.Group()
house_option_selected = pygame.sprite.Group()
house_path_temp_group = pygame.sprite.Group()
house_path_perm_group = pygame.sprite.Group()

class main_option(pygame.sprite.Sprite):
    rect = pygame.Rect(0, 800, 900, 200)
    color = ((52, 192, 235))

    def increment_pos(self):
        self.rect.y += 10
    
    def decrement_pos(self):
        self.rect.y -= 10
    
    def check(self, mouse_pos):
        if self.rect.y <= 900 and mouse_pos[1] < 800:
            self.increment_pos()
            for sub in sub_option_group.sprites():
                sub.follow(True)
        elif self.rect.y > 800:
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
        pygame.draw.rect(WINDOW, self.color, self.rect) 

class sub_option_house(sub_option):
    rect = pygame.Rect(50, 825, 50, 50)
    color = (90, 91, 92)

    def action(self):
        self.color = (255, 0, 0)
        shadow_group.add(shadow_house())

class sub_option_2(sub_option):
    rect = pygame.Rect(150, 825, 50, 50)
    color = (90, 91, 92)

class sub_option_3(sub_option):
    rect = pygame.Rect(250, 825, 50, 50)
    color = (90, 91, 92)

class sub_option_4(sub_option):
    rect = pygame.Rect(350, 825, 50, 50)
    color = (90, 91, 92)

class house(pygame.sprite.Sprite):
    rect = pygame.Rect(0, 0, 100, 100)
    color = (255, 94, 94)
    shadow_color = (255, 179, 179)
    
    def __init__(self, x_cord, y_cord):
        super().__init__()
        self.rect = pygame.Rect.copy(house.rect)
        self.rect.y = y_cord
        self.rect.x = x_cord
        self.path_up = house_path(x_cord+25, y_cord-50, self)
        self.path_down = house_path(x_cord+25, y_cord+100, self)
        self.path_right = house_path(x_cord+100, y_cord+25, self)
        self.path_left = house_path(x_cord-50, y_cord+25, self)
        self.temp_path_lst = []
        self.temp_path_lst.append(self.path_up)
        self.temp_path_lst.append(self.path_down)   
        self.temp_path_lst.append(self.path_left)   
        self.temp_path_lst.append(self.path_right)   

    def update(self):
        pygame.draw.rect(WINDOW, self.color, self.rect)
    
class house_option(main_option):
    current_obj = None
    rect = pygame.Rect(0, 900, 900, 200)
    color = (224, 255, 48)
    flag = False
    close = False

    def mov(self):
        if not self.close and self.rect.y > 800:
            for sub in house_option_group.sprites():
                sub.decrement_pos()
            self.decrement_pos()
        
        elif self.close:
            self.increment_pos()
            for sub in house_option_group.sprites():
                sub.increment_pos()
            if self.rect.y == 900:
                self.flag = False
                self.close = False
                if house_option_selected.sprites():
                    house_option_selected.sprites()[0].clean()
                house_option.current_obj = None
    
class house_option_sub(house_option):

    def update(self):
        pygame.draw.rect(WINDOW, self.color, self.rect)

class house_option_1(house_option_sub):
    rect = pygame.Rect(50, 925, 50, 50)
    color = (90, 91, 92)

    def action(self, current_house, switch=False):
        self.color = (255, 0, 0)
        if switch:
            house_path_temp_group.empty()
        for temp_path in current_house.temp_path_lst:
            house_path_temp_group.add(temp_path)

    def clean(self):
        self.color = house_option_1.color
        house_path_temp_group.empty()
        house_option_selected.empty()


class house_option_2(house_option_sub):
    rect = pygame.Rect(150, 925, 50, 50)
    color = (90, 91, 92)

class house_option_3(house_option_sub):
    rect = pygame.Rect(250, 925, 50, 50)
    color = (90, 91, 92)

class house_option_4(house_option_sub):
    rect = pygame.Rect(350, 925, 50, 50)
    color = (90, 91, 92)

class shadow(pygame.sprite.Sprite):
    
    def mov(self, mouse_pos):
        pixel_y = mouse_pos[1] - (mouse_pos[1]%10)
        pixel_x = mouse_pos[0] - (mouse_pos[0]%10)
        self.rect.y = pixel_y
        self.rect.x = pixel_x

    def update(self, mouse_pos):
        self.mov(mouse_pos)
        pygame.draw.rect(WINDOW, self.color, self.rect)

class shadow_house(shadow):
    rect = pygame.Rect.copy(house.rect)
    color = house.shadow_color
    
    def action(self):
        sub_option_group.sprites()[0].color = sub_option_house.color
        current_shadow = shadow_group.sprites()[0]
        house_group.add(house(current_shadow.rect.x, current_shadow.rect.y))
        shadow_group.remove(self)
    
class house_path(pygame.sprite.Sprite):
    temp_rect = pygame.Rect(0, 0, 50, 50)
    color = None
    temp_color = (23, 3, 252)
    perm_color = (67, 235, 52)

    def __init__(self, x_cord, y_cord, main_house, prev = None):
        super().__init__()
        self.rect = pygame.Rect.copy(self.temp_rect)
        self.rect.y = y_cord
        self.rect.x = x_cord
        self.color = self.temp_color
        self.prev = prev
        self.main_house = main_house
        self.extend_path = []
    
    def extend(self):
        lst = []
        left = house_path(self.rect.x-50, self.rect.y, self.main_house, self)
        right = house_path(self.rect.x+50, self.rect.y, self.main_house, self)
        up = house_path(self.rect.x, self.rect.y-50, self.main_house, self)
        down = house_path(self.rect.x, self.rect.y+50, self.main_house, self)
        lst.append(left)
        lst.append(right)
        lst.append(up)
        lst.append(down)

        for extend in lst:
            for path in house_path_perm_group:
                if pygame.sprite.collide_rect(extend, path):
                    break
            else:
                for house in house_group:
                    if pygame.sprite.collide_rect(house, extend):
                        break
                else:
                    for temp_path in house_path_temp_group:
                        if pygame.sprite.collide_rect(temp_path, extend):
                            break
                    else:
                        house_path_temp_group.add(extend)
                        self.extend_path.append(extend)
                        self.main_house.temp_path_lst.append(extend)

    def update(self):
        pygame.draw.rect(WINDOW, self.color, self.rect)
    
def actions(mouse_pos, house_box):
    if house_path_temp_group.sprites():
        for path in house_path_temp_group.sprites():
            if path.rect.collidepoint(mouse_pos):
                path.color = path.perm_color
                house_path_perm_group.add(path)
                house_path_temp_group.remove(path)
                if path.prev:
                    for old_temp_path in path.prev.extend_path:
                        house_path_temp_group.remove(old_temp_path)
                        old_temp_path.main_house.temp_path_lst.remove(old_temp_path)
                path.extend()

    if mouse_pos[1] >= 800:
        if house_box.flag:
            for sub in house_option_group.sprites():
                if sub.rect.collidepoint(mouse_pos):
                    selected_lst = house_option_selected.sprites()
                    if selected_lst:
                        if selected_lst[0] == sub:
                            selected_lst[0].clean()
                        else:
                            house_option_selected.empty()
                            house_option_selected.add(sub)
                    else:
                        house_option_selected.add(sub)
                        sub.action(house_box.current_obj)
                    return
        else:
            for sub in sub_option_group.sprites():
                if sub.rect.collidepoint(mouse_pos):
                    sub.action()
                    return 

    elif shadow_group.sprites():
        for shadow in shadow_group.sprites():
            shadow.action()
            return

    for house in house_group.sprites():
        if house.rect.collidepoint(mouse_pos):
            if house_option.current_obj == house:
                house_box.close = True
            else:
                house_box.flag = True
                if house_option_selected.sprites():
                    house_option_selected.sprites()[0].action(house, True)
            house_option.current_obj = house
            return

def draw_window(house_box, main_box, mouse_pos):
    WINDOW.fill((255,255,255))

    main_box.check(mouse_pos)

    house_path_perm_group.update()

    house_path_temp_group.update()

    for shadow in shadow_group.sprites():
        shadow.update(mouse_pos)
        
    for house in house_group.sprites():
        house.update()

    if not house_box.flag:
        pygame.draw.rect(WINDOW, main_box.color, main_box.rect)
        main_box.check(mouse_pos)
        sub_option_group.update()

    else:
        pygame.draw.rect(WINDOW, house_box.color, house_box.rect)
        house_box.mov()
        house_option_group.update()

    pygame.display.update()

def main():
    main_box = main_option()
    house_box = house_option()

    sub_1 = sub_option_house()
    sub_2 = sub_option_2()
    sub_3 = sub_option_3()
    sub_4 = sub_option_4()
    sub_option_group.add(sub_1)
    sub_option_group.add(sub_2)
    sub_option_group.add(sub_3)
    sub_option_group.add(sub_4)

    house_sub_1 = house_option_1()
    house_sub_2 = house_option_2()
    house_sub_3 = house_option_3()
    house_sub_4 = house_option_4()
    house_option_group.add(house_sub_1)
    house_option_group.add(house_sub_2)
    house_option_group.add(house_sub_3)
    house_option_group.add(house_sub_4)

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                actions(mouse_pos, house_box)
            
        draw_window(house_box, main_box, mouse_pos)
    pygame.quit()

if __name__ == "__main__":
    main()

#deal with sizes, pixel stuff.... should be easy.... boi i sure hope so
