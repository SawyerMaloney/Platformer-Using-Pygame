import pygame

pygame.init()


class Input:
    def __init__(self, size, position):

        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(center=position)

        self.font = pygame.font.SysFont("verdana", 25)
        self.text = ""

        self.enter_name = self.font.render("Enter Name", True, "white")
        self.enter_name_rect = self.enter_name.get_rect(
            center=(size[0] / 2, size[1] / 2)
        )
        self.should_show = True

        self.fill_color = 'gray'

    def draw(self, screen):
        self.surf.fill(self.fill_color)

        self.text_render = self.font.render(f"{self.text}", True, "white")
        self.text_render_rect = self.text_render.get_rect(topleft=(0, 0))

        if self.should_show:
            self.surf.blit(self.enter_name, self.enter_name_rect)

        self.surf.blit(self.text_render, self.text_render_rect)
        screen.blit(self.surf, self.rect)

    def clicked(self, pos):
        if self.rect.collidepoint(pos):
            pygame.key.start_text_input()
            print('clicked')
            self.should_show = False
            self.fill_color = 'black'

    def type(self, textinput):
        self.text += textinput

    def backspace(self):
        self.text = self.text[:-1]

    def enter(self):
        pygame.key.stop_text_input()
        self.should_show = True
        rv = self.text
        self.text = ""
        self.surf.fill("gray")
        return rv