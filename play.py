import gymnasium as gym
from stable_baselines3 import PPO

def main():
    env = gym.make("CartPole-v1", render_mode="human")
    model = PPO.load("ppo_cartpole")

    obs, _ = env.reset()
    for _ in range(5000):
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, _ = env.step(action)
        if terminated or truncated:
            obs, _ = env.reset()

    env.close()

if __name__ == "__main__":
    main()