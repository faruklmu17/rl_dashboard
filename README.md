# RL Dashboard & CartPole Game 🤖🎪

Welcome to the **RL Dashboard** project! This repository contains a fun, interactive web-based implementation of the classic **CartPole** reinforcement learning problem, designed to be playable by humans (and robots!).

## 🎮 The Game: Robo-Balance!

Help our friendly robot mascot keep the pole balanced on the cart! Use your keyboard or on-screen controls to push the cart left and right.

### How to Play
- **Goal**: Keep the pole upright for as long as possible!
- **Controls**:
    - **⬅️ Left Arrow / Button**: Push Cart Left
    - **➡️ Right Arrow / Button**: Push Cart Right
    - **🤖 Robot Helper**: Let the AI take over and show you how it's done!

### Features
- **Moon Gravity Physics 🌑**: Tuned for a relaxing, easy-to-play experience.
- **Responsive Controls**: "Proportional Push" technology allows for miracle saves.
- **Kid-Friendly UI**: colorful graphics, emojis, and a friendly robot companion.

## 🛠️ Technology
- **HTML5 Canvas**: For smooth, 60fps physics rendering.
- **Vanilla JavaScript**: No heavy frameworks, just pure code.
- **CSS3**: Modern styling with gradients, shadows, and animations.

## 📦 Installation

To run the Python components (Training & Server), you'll need to set up your environment:

1. **Create and Activate a Virtual Environment** (Recommended):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Getting Started
Simply open `rl_cartpole_details.html` in any modern web browser to start playing immediately!

## 🧠 Training the AI
Want to see how the robot learns? You can train your own AI model and watch the progress live on the dashboard!

1. **Start the Dashboard Server**:
   This serves the visualization page.
   ```bash
   uvicorn server:app --reload
   ```
   *Open `http://127.0.0.1:8000` in your browser.*

2. **Run the Training Script**:
   open a new terminal, This starts the Reinforcement Learning (PPO) process.
   ```bash
   python train.py
   ```

3. **Watch it Learn**:
   Go to the dashboard (`http://127.0.0.1:8000`) to see real-time graphs of the AI's performance as it gets smarter! 📈

---
*"Balance is not something you find, it's something you create."* 🧘
