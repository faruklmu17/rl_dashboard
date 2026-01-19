import json
import time
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback

METRICS_FILE = "metrics.json"

class MetricsCallback(BaseCallback):
    def __init__(self, write_every_steps=1000, verbose=0):
        super().__init__(verbose)
        self.write_every_steps = write_every_steps
        self.last_write = 0
        self.episode_rewards = []
        self.current_ep_reward = 0.0
        self.episodes = 0

    def _on_step(self) -> bool:
        reward = float(self.locals["rewards"][0])
        done = bool(self.locals["dones"][0])

        self.current_ep_reward += reward
        if done:
            self.episode_rewards.append(self.current_ep_reward)
            self.episodes += 1
            self.current_ep_reward = 0.0

        if (self.num_timesteps - self.last_write) >= self.write_every_steps:
            self.last_write = self.num_timesteps
            last_10 = self.episode_rewards[-10:]
            avg_10 = sum(last_10) / len(last_10) if last_10 else 0.0

            data = {
                "timesteps": int(self.num_timesteps),
                "episodes": int(self.episodes),
                "avg_reward_last_10": float(avg_10),
                "reward_history": self.episode_rewards[-200:],
                "updated_at": time.time(),
            }
            with open(METRICS_FILE, "w") as f:
                json.dump(data, f)

        return True

def main():
    env = gym.make("CartPole-v1")
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=200_000, callback=MetricsCallback(write_every_steps=1000))
    model.save("cartpole_ppo")

if __name__ == "__main__":
    main()
