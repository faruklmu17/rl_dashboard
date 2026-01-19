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
    mascot_img = None
    try:
        mascot_img = pygame.image.load("mascot.png").convert_alpha()
        mascot_img = pygame.transform.scale(mascot_img, (100, 100)) # Scale mascot
    except Exception as e:
        print(f"Error loading mascot: {e}")
        # Proceed without mascot if missing

    # Procedural assets (no images needed for cart/pole anymore)

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

        # Draw Background (Match HTML Canvas Color)
        screen.fill((240, 249, 255)) # #f0f9ff
        
        # Draw Mascot (Top Right)
        if mascot_img:
            mascot_rect = mascot_img.get_rect(topright=(WIDTH - 20, 20))
            screen.blit(mascot_img, mascot_rect)

        # Draw Ground Line
        pygame.draw.line(screen, (203, 213, 225), (50, HEIGHT - 80), (WIDTH - 50, HEIGHT - 80), 4) # #cbd5e1

        # Draw Cart (Yellow Rounded Rect)
        # HTML: roundRect(screenX - 40, H - 100, 80, 40, 10)
        cart_rect = pygame.Rect(0, 0, 80, 40)
        cart_rect.centerx = cart_screen_x
        cart_rect.bottom = HEIGHT - 80 - 20 + 40 # HTML draws at H-100. Ground is H-80? No HTML ground is H-80. Cart is at H-100 (floating?).
        # HTML: ground at H-80. Cart at H-100. Cart is 80x40. 
        # So Cart bottom is at H-60. Wait.
        # HTML: ctx.roundRect(screenX - 40, H - 100, 80, 40, 10);
        # Top-left is H-100. Height 40. Bottom is H-60.
        # Ground line is H-80. So cart overlaps ground?
        # Let's trust values.
        
        cart_y = HEIGHT - 100
        cart_draw_rect = pygame.Rect(cart_screen_x - 40, cart_y, 80, 40)
        
        pygame.draw.rect(screen, (255, 206, 0), cart_draw_rect, border_radius=10) # #ffce00
        pygame.draw.rect(screen, (51, 51, 51), cart_draw_rect, 2, border_radius=10) # Stroke #333

        # Draw Wheels
        # HTML: arc(screenX - 25, H - 65, 10...)
        pygame.draw.circle(screen, (51, 51, 51), (cart_screen_x - 25, HEIGHT - 65), 10)
        pygame.draw.circle(screen, (51, 51, 51), (cart_screen_x + 25, HEIGHT - 65), 10)

        # Draw Pole (Red Rounded Rect)
        # HTML: pivot is screenX, H-100.
        # It translates to (screenX, H-100) then rotates.
        # Rect is (-5, -120, 10, 120).
        # So pivot is at the BOTTOM CENTER of the pole rect.
        
        # New Procedural Pole Surface
        pole_surf = pygame.Surface((20, 140), pygame.SRCALPHA) # Bigger to fit ball
        # Draw pole relative to its own center/pivot.
        # We'll draw it upright then rotate.
        # Rect local coords: (5, 10, 10, 120) -> perfectly centered horizontally (20 width).
        # Bottom of rect at 130.
        
        # Actually easier: Draw pole primarily vertical, then rotate.
        # Pole dims: 10 wide, 120 high.
        # Color: #ff6b6b (255, 107, 107)
        
        # Create a surface for the pole for rotation
        pole_w, pole_h = 10, 120
        # Surface needs space for the ball on top too.
        surf_w, surf_h = 40, 160
        pole_surf = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
        
        # Pivot point on surface: (surf_w/2, surf_h - 20) (arbitrary padding)
        pivot_local = (surf_w//2, surf_h - 10)
        
        # Draw Rect
        # Top-left of rect relative to pivot: (-5, -120)
        rect_top_left = (pivot_local[0] - 5, pivot_local[1] - 120)
        pygame.draw.rect(pole_surf, (255, 107, 107), (*rect_top_left, 10, 120), border_radius=5)
        
        # Draw Ball
        # HTML: arc(0, -125, 8...)
        # Center relative to pivot: (0, -125)
        ball_center = (pivot_local[0], pivot_local[1] - 125)
        ball_color = (255, 243, 64) # #fff340 (alive) - Assumed alive for visual
        pygame.draw.circle(pole_surf, ball_color, ball_center, 8)

        # Rotation
        angle_deg = -math.degrees(pole_angle)
        rotated_pole = pygame.transform.rotate(pole_surf, angle_deg)
        
        # Blit at pivot
        # The pivot in valid screen coords is (cart_screen_x, HEIGHT - 100)
        # We need to align the pivot_local of the rotated surf with this screen point.
        
        screen_pivot = (cart_screen_x, HEIGHT - 100)
        rect = rotated_pole.get_rect()
        
        # Standard way to rotate around a pivot in Pygame:
        # offset = pivot_local - center_of_image
        # rotated_offset = offset.rotate(angle)
        # rect.center = pivot + rotated_offset
        # But we constructed the surface, we know the vector from center to pivot.
        
        # Simpler:
        # 1. Start with rect centered at screen_pivot
        rect.center = screen_pivot
        # 2. Shift it. The pivot is NOT the center of the surface.
        # The pivot on the unrotated surface is (surf_w/2, surf_h-10). The center is (surf_w/2, surf_h/2).
        # Vector from Center -> Pivot = (0, (surf_h-10) - surf_h/2) = (0, surf_h/2 - 10)
        # We need to apply the rotation to this vector.
        
        vec = pygame.math.Vector2(0, (surf_h/2 - 10)) # Vector from Center to Pivot (downwards)
        vec_rot = vec.rotate(-angle_deg) # Rotate vector (remember y is down)
        
        # The rect center should be such that: rect.center + vec_rot = screen_pivot
        # So: rect.center = screen_pivot - vec_rot
        
        rect.center = (screen_pivot[0] - vec_rot.x, screen_pivot[1] - vec_rot.y)
        
        screen.blit(rotated_pole, rect)

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
