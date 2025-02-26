import pygame
from core.entity import Entity
from core.settings import GameSettings

fuel_img = pygame.image.load("./assets/fuel.png")
shield_img = pygame.image.load("./assets/shield.png")
slowdown_img = pygame.image.load("./assets/slowdown.png")  # Add the image for the slowdown power-up

# ------------------------------------
# Power Up Base Class
# ------------------------------------
class PowerUp(Entity):
    """Base class for power-up items with vertical scrolling behavior."""
    def __init__(self, x, y, image, width=50, height=50):
        super().__init__(x, y, width, height)
        self.image = image

    def update(self, dt):
        """Make the power-up "fall" downwards.
        
        Args:
            dt (Float): Delta time in seconds
        """
        self.y += GameSettings.BACKGROUND_SPEED * dt

    def draw(self, surface):
        """Draw power-up image on specified surface. Image is stored in self.image.
        
        Args:
            surface (pygame.Surface): Game display surface
        """
        surface.blit(self.image, (self.x, self.y))

    def apply(self, balloon):
        """Abstract method to apply power-up effect to balloon.
        
        Args:
            balloon (Balloon): Balloon to apply effect to
        """
        raise NotImplementedError("Subclasses must implement apply method.")

# ------------------------------------
# Power Up Subclasses
# ------------------------------------
class ShieldPowerUp(PowerUp):
    """Power-up that grants temporary invincibility to the balloon."""
    def __init__(self, x, y):
        super().__init__(x, y, shield_img)

    def apply(self, balloon):
        """Activate shield protection on balloon.
        
        Args:
            balloon (Balloon): Balloon to apply effect to
        """
        balloon.shield_active = True
        balloon.shield_timer = GameSettings.SHIELD_DURATION
        print("Shield activated for {} ms!".format(GameSettings.SHIELD_DURATION))

class FuelPowerUp(PowerUp):
    """Power-up that refills balloon's fuel supply."""
    def __init__(self, x, y):
        super().__init__(x, y, fuel_img)

    def apply(self, balloon):
        """Increase balloon's fuel level.
        
        Args:
            balloon (Balloon): Balloon to apply effect to
        """
        balloon.fuel += GameSettings.FUEL_POWER_UP # Increase fuel
        if balloon.fuel > GameSettings.FUEL_MAX_FILL:
            balloon.fuel = GameSettings.FUEL_MAX_FILL
        print("Fuel increased!")

class SlowdownPowerUp(PowerUp):
    """Power-up that slows down obstacles."""
    def __init__(self, x, y):
        super().__init__(x, y, slowdown_img)

    def apply(self, balloon):
        """Slow down obstacles.
        
        Args:
            balloon (Balloon): Balloon to apply effect to
        """
        balloon.slowdown_active = True
        balloon.slowdown_timer = GameSettings.SLOWDOWN_DURATION
        GameSettings.OBSTACLE_SPEED = GameSettings.SLOWDOWN_OBSTACLE_SPEED
        print("Obstacles slowed down for {} ms!".format(GameSettings.SLOWDOWN_DURATION))