from typing import List, Optional
from base_agent import BaseAgent, State, Action

class QLearningAgent(BaseAgent):
    """ Q-learning agent implementation. """

    def update(self, state:State, action: Action, reward: float, next_state: Optional[State], done: bool, valid_next_actions: Optional[List[Action]] = None) -> float:
        """
        Update the Q-value for a given state-action pair using the Q-learning update rule.
        Returns: the temporal difference error (TD error) for the update.
        """
        if done or next_state is None:
            target = reward

        else:
            target = reward + self.gamma * self.max_q_value(next_state, valid_next_actions)
        return self._td_update(state, action, target)