import pygame


class Ground(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill("green")
        self.rect = self.image.get_rect(center=position)

        self.scroll_speed = 1
        self.counted = False

    def scroll(self, scroll, scroll_speed):
        if scroll != 0:
            if scroll_speed > scroll:
                self.rect.y += scroll_speed
            else:
                self.rect.y += scroll

    def destroy(self):
        if self.rect.y > 900:
            self.kill()
            return 1
        return 0

    def update(self, scroll_distance, scroll_speed):
        self.scroll(scroll_distance, scroll_speed)
        self.destroy()
