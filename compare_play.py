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
    # Setup environments (using rgb_array but we'll draw manually)
    env_h = gym.make("CartPole-v1", render_mode="rgb_array")
    env_ai = gym.make("CartPole-v1", render_mode="rgb_array")

    try:
        model = PPO.load("ppo_cartpole")
    except:
        print("Model ppo_cartpole not found. Please train it first.")
        return

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Human (Left) vs AI (Right)")
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
        pole_img = pygame.transform.scale(pole_img, (POLE_WIDTH, POLE_LENGTH))
    except Exception as e:
        print(f"Error loading assets: {e}")
        return

    obs_h, _ = env_h.reset()
    obs_ai, _ = env_ai.reset()
    
    score_h = 0
    score_ai = 0
    font = pygame.font.SysFont("Arial", 20, bold=True)

    action_h = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: action_h = 0
                if event.key == pygame.K_RIGHT: action_h = 1

        # Step AI
        action_ai, _ = model.predict(obs_ai, deterministic=True)
        
        obs_h, r_h, t_h, tr_h, _ = env_h.step(action_h)
        obs_ai, r_ai, t_ai, tr_ai, _ = env_ai.step(action_ai)
        
        score_h += r_h
        score_ai += r_ai

        if t_h or tr_h: 
            obs_h, _ = env_h.reset()
            score_h = 0
        if t_ai or tr_ai: 
            obs_ai, _ = env_ai.reset()
            score_ai = 0

        # Draw Background
        screen.blit(background, (0, 0))
        
        # Draw Divider
        pygame.draw.line(screen, (0, 189, 255), (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)

        # Draw Environments
        def draw_env(obs, score, offset_x, label):
            cart_x = obs[0]
            pole_angle = obs[2]
            
            # Map coordinates for half screen
            screen_x = offset_x + int((cart_x / 4.8 + 0.5) * (WIDTH//2))
            screen_y = HEIGHT - 120
            
            # Cart
            cart_rect = cart_img.get_rect(center=(screen_x, screen_y))
            screen.blit(cart_img, cart_rect)
            
            # Pole
            angle_deg = -math.degrees(pole_angle)
            rotated_pole = pygame.transform.rotate(pole_img, angle_deg)
            pivot_y = screen_y - 10
            
            pole_rect = rotated_pole.get_rect()
            v_offset = pygame.math.Vector2(0, -POLE_LENGTH / 2).rotate(-angle_deg)
            pole_rect.center = (screen_x, pivot_y) + v_offset
            screen.blit(rotated_pole, pole_rect)
            
            # UI
            label_surf = font.render(label, True, (0, 189, 255))
            screen.blit(label_surf, (offset_x + 20, 20))
            score_surf = font.render(f"SCORE: {int(score)}", True, (255, 255, 255))
            screen.blit(score_surf, (offset_x + 20, 50))

        draw_env(obs_h, score_h, 0, "HUMAN (Arrows)")
        draw_env(obs_ai, score_ai, WIDTH//2, "AI AGENT")

        # Glass Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 189, 255, 20), (0,0, WIDTH, HEIGHT))
        screen.blit(overlay, (0,0))

        pygame.display.flip()
        clock.tick(60)

    env_h.close()
    env_ai.close()
    pygame.quit()

if __name__ == "__main__":
    main()
