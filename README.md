# Blackjack Simulator & RL Environment

This project is a complete simulation environment for the game of Blackjack, developed in Python. The ultimate goal is to create an ecosystem for training and testing Artificial Intelligence agents (Reinforcement Learning) and analyzing the efficiency of Card Counting strategies.

## 📌 Current Status (MVP)
Currently, the project runs the core game engine (Player vs. Dealer) in the console, implementing strict casino rules:
* **Shoe Management:** Support for multiple decks (e.g., 6 decks) with realistic shuffling based on deck penetration (Cut Card).
* **Hand Logic:** Precise score calculation, including dynamic Ace management (Soft/Hard hands).
* **Game Loop:** Complete flow for betting, dealing cards, player options (Hit, Stand), and forced dealer logic (Stand on all 17s).

## 🚀 Future Features (Roadmap)
* Implementation of advanced player actions (Double Down, Split).
* Development of an "Expert System" based on the Hi-Lo Card Counting system (incorporating the Illustrious 18 deviations).
* Integration of AI agents using **Q-Learning** and **QV-Learning** algorithms.
* Multi-threaded Monte Carlo simulations for generating statistical data and comparative learning curves.

## 🛠️ Technologies Used
* Python 3.x
* Object-Oriented Programming (OOP)

---
*Bachelor's Degree Project developed by Acul Mathyas.*