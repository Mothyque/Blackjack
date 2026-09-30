from typing import List, Optional
from base_agent import BaseAgent, State, Action

class SarsaAgent(BaseAgent):
    """ SARSA agent implementation. """

    def update(self, state: State, action: Action, reward: float, next_state: Optional[State], next_action: Optional[Action], done: bool) -> float:
        """
        Update the Q-value for a given state-action pair using the SARSA update rule.
        Returns: the temporal difference error (TD error) for the update.
        """
        if done or next_state is None or next_action is None:
            target = reward
        else:
            target = reward + self.gamma * self.get_q_value(next_state, next_action)
        return self._td_update(state, action, target)