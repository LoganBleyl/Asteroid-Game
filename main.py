
import constants
import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASSETS_DIR
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()

    # initialize display before converting images
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # load and scale the background now that display is ready (project-relative path)
    background = pygame.image.load(str(ASSETS_DIR / "Backgrounds" / "Blue_Nebula_05-1024x1024.png")).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # helper for loading other assets (if needed)
    def load_all():
        return {
            "ship": pygame.image.load(str(ASSETS_DIR / "Ships" / "Spaceship_12.png")).convert_alpha(),
            "asteroid": pygame.image.load(str(ASSETS_DIR / "Asteroids" / "Asteroid_01.png")).convert_alpha(),
            "background": background,
        }

    # track total elapsed time so we can ignore collisions briefly
    elapsed_time = 0.0
    print(f"Starting Asteroids game with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    clock = pygame.time.Clock()
    Shot.containers = (updatable, drawable, shots)
    AsteroidField.containers = (updatable,)
    Asteroid.containers = (updatable, drawable, asteroids)
    Player.containers = (updatable, drawable)
    asteroid_field = AsteroidField()
    # once the player exists, let the field know so it can avoid spawning nearby
    
    player_image = pygame.image.load(str(ASSETS_DIR / "Ships" / "Spaceship_12.png")).convert_alpha()
    player_image = pygame.transform.scale(player_image, (constants.PLAYER_RADIUS * 2, constants.PLAYER_RADIUS * 2))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, player_image)
    # inform asteroid field about the player so it can keep a safe distance
    asteroid_field.player = player
    dt = 0
    
   
    # game loop variables
    elapsed_time = 0.0
    grace_period = 1.0  # seconds during which player cannot die

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        updatable.update(dt)
        # only check collisions after the grace period has passed
        if elapsed_time > grace_period:
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    log_event("player_hit")
                    print("Game over!")
                    sys.exit()
        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
        screen.blit(background, (0, 0))
        for obj in drawable:
            obj.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        elapsed_time += dt

       

if __name__ == "__main__":
    main()
