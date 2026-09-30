import abc
import pickle
import random
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

State = Tuple[Any, ...]
Action = int
QKey = Tuple[State, Action]

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

        self.q_table: Dict[QKey, float] = defaultdict(float)

    def get_q_value(self, state: State, action: Action) -> float:
        """Get the Q-value for a given state-action pair."""
        return self.q_table.get((state, action), 0.0)

    def max_q_value(self, state: State, valid_actions: Optional[List[Action]] = None) -> float:
        """Get the maximum Q-value for a given state over all valid actions."""
        actions = valid_actions if valid_actions is not None else self.actions
        return max((self.get_q_value(state, a) for a in actions), default=0.0)

    def _resolve_actions(self, valid_actions: Optional[List[Action]]) -> List[Action]:
        """ Resolve the list of valid actions. If valid_actions is provided, use it; otherwise, use the agent's default actions. 
            Raises a ValueError if no valid actions are available.
            Returns: the list of valid actions.
        """
        actions = valid_actions if valid_actions is not None else self.actions
        if not actions:
            raise ValueError("No valid actions available.")
        return actions

    def get_best_action(self, state: State, valid_actions: Optional[List[Action]] = None) -> Action:
        """ Greedy selection of the best action based on Q-values. """
        actions = self._resolve_actions(valid_actions)
        q_values = {a: self.get_q_value(state, a) for a in actions}
        best_q = max(q_values.values())
        return random.choice([a for a, q in q_values.items() if q == best_q])

    def choose_action(self, state: State, valid_actions: Optional[List[Action]] = None) -> Action: 
        """ Choose an action based on the epsilon-greedy policy. """
        actions = self._resolve_actions(valid_actions)
        if random.random() < self.epsilon:
            return random.choice(actions)
        return self.get_best_action(state, valid_actions)

    def decay_epsilon(self) -> None: 
        """ Reduces epsilon over time to balance exploration and exploitation. """
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def _td_update(self, state: State, action: Action, target: float, step_size: Optional[float] = None) -> float:
        """ Move Q(state, action) towards the target value using the temporal difference update rule.
            Returns: the temporal difference error (TD error) for the update.
        """
        step = self.alpha if step_size is None else step_size
        error = target - self.get_q_value(state, action)
        self.q_table[(state, action)] += step * error
        return error

    @abc.abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> Any:
        """ Update the agent's knowledge based on the algorithm chosen. This method should be implemented by subclasses. """

    def save_policy(self, file_path: str) -> None:
        """ Save the agent's policy (Q-table) to a file. """
        with open(file_path, 'wb') as f:
            pickle.dump(dict(self.q_table), f)

    def load_policy(self, file_path: str) -> None:
        """ Load the agent's policy (Q-table) from a file. """
        with open(file_path, 'rb') as f:
            self.q_table = defaultdict(float, pickle.load(f))