import gymnasium as gym
import pygame
import numpy as np
import math
from stable_baselines3 import PPO

# Constants
WIDTH = 800
HEIGHT = 500
CART_WIDTH = 100
CART_HEIGHT = 60
POLE_WIDTH = 15
POLE_LENGTH = 150

def main():
    # Setup environment
    env = gym.make("CartPole-v1", render_mode="rgb_array")
    try:
        model = PPO.load("ppo_cartpole")
    except:
        print("Model ppo_cartpole not found. Please train it first.")
        return

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CartPole: Enhanced Graphics")
    clock = pygame.time.Clock()

    # Load Assets
    try:
        background = pygame.image.load("background.png").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        
        cart_img = pygame.image.load("cart.png").convert_alpha()
        cart_img.set_colorkey((255, 255, 255))
        cart_img = pygame.transform.scale(cart_img, (CART_WIDTH, CART_HEIGHT))
        
        pole_img = pygame.image.load("pole.png").convert_alpha()
        pole_img.set_colorkey((255, 255, 255))
        # Scale pole height, width stays relatively small
        pole_img = pygame.transform.scale(pole_img, (POLE_WIDTH, POLE_LENGTH))
    except Exception as e:
        print(f"Error loading assets: {e}")
        return

    obs, _ = env.reset()
    score = 0
    font = pygame.font.SysFont("Arial", 24, bold=True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # AI Predicts
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, _ = env.step(action)
        score += reward

        if terminated or truncated:
            obs, _ = env.reset()
            score = 0

        # Rendering
        # 1. State extraction
        # x, x_dot, theta, theta_dot = obs
        cart_x_state = obs[0]
        pole_angle = obs[2]

        # 2. Map coordinates (Gym x: -2.4 to 2.4)
        cart_screen_x = int((cart_x_state / 4.8 + 0.5) * WIDTH)
        cart_screen_y = HEIGHT - 100

        # Draw Background
        screen.blit(background, (0, 0))

        # Draw Cart
        cart_rect = cart_img.get_rect(center=(cart_screen_x, cart_screen_y))
        screen.blit(cart_img, cart_rect)

        # Draw Pole
        # Note: Gymnasium theta=0 is vertical (up), theta increases clockwise.
        # Pygame rotation: 0 is right, increases counter-clockwise.
        # Conversion: pole_img is vertical up. We rotate by -theta (in degrees).
        angle_deg = -math.degrees(pole_angle)
        
        rotated_pole = pygame.transform.rotate(pole_img, angle_deg)
        # We want the bottom of the pole to stay at the cart's center
        # Pivot point is bottom center of the pole
        # This is a bit tricky in Pygame, easiest way is to use the center of rotation
        
        # Calculate pivot position
        pivot_x = cart_screen_x
        pivot_y = cart_screen_y - 10
        
        pole_rect = rotated_pole.get_rect()
        
        # Offset calculation to rotate around bottom center
        # The center of the rotated rect shifts. We need the bottom center of the pole sprite
        # to stay at (pivot_x, pivot_y).
        # Before rotation, bottom center is (POLE_WIDTH/2, POLE_LENGTH)
        # After rotation, we need to find where that point went.
        
        # Simplified approach: 
        offset = pygame.math.Vector2(0, -POLE_LENGTH / 2).rotate(-angle_deg)
        pole_rect.center = (pivot_x, pivot_y) + offset
        
        screen.blit(rotated_pole, pole_rect)

        # Draw Score and UI
        score_surf = font.render(f"SCORE: {int(score)}", True, (255, 255, 255))
        screen.blit(score_surf, (20, 20))
        
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 189, 255, 30), (0,0, WIDTH, HEIGHT)) # Subtle blue tint
        screen.blit(overlay, (0,0))

        pygame.display.flip()
        clock.tick(60)

    env.close()
    pygame.quit()

if __name__ == "__main__":
    main()
