from collections import defaultdict
from typing import Any, Dict, List, Tuple
from base_agent import Action, BaseAgent, State, QKey

class MonteCarloAgent(BaseAgent):
    """ A Monte Carlo agent for playing blackjack. """

    def __init__(
            self, 
            actions: List[Action],
            learning_rate: float = 0.02,
            use_sample_average: bool = True,
            **kwargs: Any,
    ) -> None: 
        super().__init__(actions, learning_rate=learning_rate, **kwargs)

        self.use_sample_average = use_sample_average
        self.returns_count: Dict[QKey, int] = defaultdict(int)
        self.episode_buffer: List[Tuple[State, Action, float]] = []


    def record_step(self, state: State, action: Action, reward: float) -> None:
        """ Record a step in the episode buffer. """
        self.episode_buffer.append((state, action, reward))

    def update(self) -> None:
        """ Update the Q-values based on the episode buffer. """
        first_visit: Dict[QKey, int] = {}
        for t, (state, action, _) in enumerate(self.episode_buffer):
            first_visit.setdefault((state, action), t)

        G = 0.0
        for t in reversed(range(len(self.episode_buffer))):
            state, action, reward = self.episode_buffer[t]
            G = reward + self.gamma * G
            pair = (state, action)
            if first_visit[pair] != t:
                continue

            step = None
            if self.use_sample_average:
                self.returns_count[pair] += 1
                step = 1.0 / self.returns_count[pair]
            self._td_update(state, action, G, step)

        self.episode_buffer.clear()    

