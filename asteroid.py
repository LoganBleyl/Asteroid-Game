import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
import random
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        base_image = pygame.image.load("/home/loganb/Documents/Workspace/Asteroid_game/Asteroid-Game-main/Assets/Asteroids/Asteroid_1.png").convert_alpha()
        size = int(self.radius * 2)
        self.image = pygame.transform.scale(base_image, (size, size))
        self.rotation_angle = 0  # track slow spin

    def draw(self, screen):
        rotated = pygame.transform.rotate(self.image, self.rotation_angle)
        rect = rotated.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated, rect)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        random_angle = random.uniform(20, 50)
        asteroid_a = self.velocity.rotate(random_angle)
        asteroid_b = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = asteroid_a * 1.2
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = asteroid_b * 1.2
