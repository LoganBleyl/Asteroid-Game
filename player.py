import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, SHOT_RADIUS, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from shot import Shot

class Player(CircleShape):
<<<<<<< HEAD
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cd_timer = 0
   
=======
    def __init__(self, x, y, image=None):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cd_timer = 0
        # allow caller to supply a pre-loaded/scaled image; otherwise use default
        if image is None:
            self.original_image = pygame.image.load(
                "/home/loganb/Documents/Workspace/Asteroid_game/Asteroid-Game-main/Assets/Ships/Spaceship_12.png"
            ).convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (50, 50))  # default size
        else:
            self.original_image = image
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))
>>>>>>> 1c38e60 (added ship/asteroid sprites and a new background)
    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
<<<<<<< HEAD
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
=======
        # Rotate image to match ship's rotation angle
        rotated = pygame.transform.rotate(self.original_image, -self.rotation)  # negative because pygame rotates counter-clockwise
        rect = rotated.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated, rect)
>>>>>>> 1c38e60 (added ship/asteroid sprites and a new background)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shoot_cd_timer -= dt
        if self.shoot_cd_timer < 0:
            self.shoot_cd_timer = 0

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.shoot_cd_timer > 0:
            return
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = direction * PLAYER_SHOOT_SPEED
        self.shoot_cd_timer = PLAYER_SHOOT_COOLDOWN_SECONDS