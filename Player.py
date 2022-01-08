import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()

        self.image = pygame.Surface((30, 60))
        self.image.fill("green")
        self.rect = self.image.get_rect(center=(screen.width / 2, screen.height - 100))

        self.gravity = 0
        self.movement_speed = 7
        self.jump_gravity = -20

    def apply_gravity(self, onFloor, position):
        self.rect.y += self.gravity
        if not onFloor:
            self.gravity += 1
        elif self.gravity > 0:
            self.rect.bottom = position

    def input(self, onGround):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if onGround:
                self.gravity = self.jump_gravity
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.movement_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.movement_speed

    def scroll(self, scroll, scroll_speed):
        if scroll != 0:
            if scroll_speed > scroll:
                self.rect.y += scroll_speed
            else:
                self.rect.y += scroll

    def check_offscreen(self):
        if self.rect.centerx < 0:
            self.rect.centerx = 400
        elif self.rect.centerx > 400:
            self.rect.centerx = 0

    def update(self, onGround, scroll, scroll_speed):
        self.input(onGround)
        self.scroll(scroll, scroll_speed)
        self.check_offscreen()