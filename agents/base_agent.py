import abc
import pickle
import random
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

State = Tuple[Any, ...]
Action = int

class BaseAgent(abc.ABC):
    """ Base class for reinforcement learning agents. """

    def __init__(self,
        actions: List[Action],
        learning_rate: float = 0.05,
        discount_factor: float = 1.0,
        epsilon: float = 1.0,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.99995,
        ) -> None:
        self.actions = actions
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        self.q_table: Dict[Tuple[State, Action], float] = defaultdict(float)

        def get_q_value(self, state: State, action: Action) -> float:
            """Get the Q-value for a given state-action pair."""
            return self.q_table[(state, action)]

        def choose_action(self, state: State, valid_actions: Optional[List[Action]] = None) -> Action: 
            """ Choose an action based on the epsilon-greedy policy. """
            available_actions = valid_actions if valid_actions is not None else self.actions

            if not available_actions:
                raise ValueError("No valid actions available to choose from.")

            if random.random() < self.epsilon:
                return random.choice(available_actions)

            q_values = [(action, self.get_q_value(state, action)) for action in available_actions]
            max_q_value = max(q_values, key=lambda x: x[1])[1]

            best_actions =  [action for action, q_value in q_values if q_value == max_q_value]
            return random.choice(best_actions)

        def get_best_action(self, state: State, valid_actions: Optional[List[Action]] = None) -> Action:
            """ Greedy selection of the best action based on Q-values. """
            available_actions = valid_actions if valid_actions is not None else self.actions

            q_values = [(action, self.get_q_value(state, action)) for action in available_actions]
            max_q_value = max(q_values, key=lambda x: x[1])[1]
            best_actions = [action for action, q_value in q_values if q_value == max_q_value]
            return random.choice(best_actions)

        def decay_epsilon(self) -> None: 
            """ Reduces epsilon over time to balance exploration and exploitation. """
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

        @abc.abstractmethod
        def update(self, *args: Any, **kwargs: Any) -> None:
            """ Update the agent's knowledge based on the algorithm chosen. This method should be implemented by subclasses. """
            pass

        def save_policy(self, file_path: str) -> None:
            """ Save the agent's policy (Q-table) to a file. """
            with open(file_path, 'wb') as f:
                pickle.dump(self.q_table, f)

        def load_policy(self, file_path: str) -> None:
            """ Load the agent's policy (Q-table) from a file. """
            with open(file_path, 'rb') as f:
                self.q_table = pickle.load(f)