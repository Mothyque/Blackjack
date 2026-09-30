from typing import List, Optional, Tuple
from models.dealer import Dealer
from models.player import Player
from models.shoe import Shoe

ACTION_STAND = 0
ACTION_HIT = 1
ACTION_DOUBLE = 2
ACTION_SPLIT = 3

State = Tuple[int, int, bool, bool, bool]  

class BlackjackEnv:
    """ Wrapper for RL environment to interact with the blackjack game. """

    def __init__(self, num_decks: int = 6) -> None:
        self.shoe = Shoe(num_decks=num_decks)
        self.dealer = Dealer()
        self.player = Player(name="RL Agent", balance=1_000_000.0)
        self.current_hand_index = 0
        self.is_done = False

    def _get_dealer_upcard_val(self) -> int:
        """ Get the value of the dealer's upcard. """
        rank = self.dealer.upcard.get_rank()
        if rank == 'A':
            return 11
        if rank in ['J', 'Q', 'K']:
            return 10
        return int(rank)

    def _get_hand_state(self, hand_index: int) -> State:
        """ Get the state representation for a given hand index. 
            Returns: A tuple representing the state
        """
        hand = self.player.hands[hand_index]
        score = hand.score
        dealer_val = self._get_dealer_upcard_val()
        is_soft = hand.is_soft
        can_double = self.player.can_double(hand_index)
        can_split = self.player.can_split(hand_index)

        return (score, dealer_val, is_soft, can_double, can_split)

    def get_valid_actions(self, hand_index: int) -> List[int]:
        """ Get the list of valid actions for a given hand index. """
        actions = [ACTION_STAND, ACTION_HIT]

        if self.player.can_double(hand_index):
            actions.append(ACTION_DOUBLE)
        if self.player.can_split(hand_index):
            actions.append(ACTION_SPLIT)

        return actions

    def reset(self) -> Tuple[State, List[int]]:
        """ Reset the environment for a new round. 
            Returns: The initial state and valid actions for the first hand.
        """

        if self.shoe.needs_reshuffle:
            self.shoe.build_and_shuffle()

        self.player.clear_hand()
        self.dealer.clear_hand()
        self.current_hand_index = 0
        self.is_done = False

        self.player.set_current_bet(1.0)
        self.player.place_bet(self.player.current_bet)

        self.player.receive_card(self.shoe.draw_card())
        self.dealer.receive_card(self.shoe.draw_card())
        self.player.receive_card(self.shoe.draw_card())
        self.dealer.receive_card(self.shoe.draw_card())

        state = self._get_hand_state(0)
        valid_actions = self.get_valid_actions(0)  
        return state, valid_actions

    def _play_dealer_turn(self) -> None:
        """ Play the dealer's turn according to the rules. """
        while self.dealer.should_hit:
            self.dealer.receive_card(self.shoe.draw_card())

    def _resolve_round_rewards(self) -> float:
        """ Resolve the round and calculate the rewards for the player. 
            Returns: The total reward for the player after the round.
        """
        dealer_score = self.dealer.hand.score
        dealer_bj = dealer_score == 21 and len(self.dealer.hand.cards) == 2
        total_reward = 0.0

        for i, hand in enumerate(self.player.hands):
            bet_multiplier = 2.0 if len(hand.cards) == 2 and not self.player.can_double_down(i) and self.player.bets[i] > 1.0 else 1.0
            if hand.is_busted:
                total_reward -= 1.0 * bet_multiplier
                continue

            player_score = hand.score
            player_bj = player_score == 21 and len(hand.cards) == 2

            if player_bj and not dealer_bj:
                total_reward += 1.5
            elif dealer_bj and not player_bj:
                total_reward -= 1.0 * bet_multiplier
            elif dealer_score > 21 or player_score > dealer_score:
                total_reward += 1.0 * bet_multiplier
            elif player_score < dealer_score:
                total_reward -= 1.0 * bet_multiplier
            else: 
                total_reward += 0.0

        return total_reward


    def step(self, action: int) -> Tuple[State, float, bool, List[int]]:
        """ Take a step in the environment based on the action taken by the agent. 
            Returns: A tuple containing the next state, reward, done flag, and valid actions for the next hand.
        """
        if self.is_done:
            raise RuntimeError("Round is already done. Please reset the environment.")

        hand_index = self.current_hand_index
        hand = self.player.hands[hand_index]
        reward = 0.0

        if action == ACTION_HIT:
            self.player.receive_card(self.shoe.draw_card(), hand_index)
            if hand.is_busted or hand.score == 21:
                self.current_hand_index += 1

        elif action == ACTION_STAND:
            self.current_hand_index += 1

        elif action == ACTION_DOUBLE:
            self.player.double_down(hand_index)
            self.player.receive_card(self.shoe.draw_card(), hand_index)
            self.current_hand_index += 1

        elif action == ACTION_SPLIT:
            self.player.split(hand_index)

            self.player.receive_card(self.shoe.draw_card(), hand_index)
            self.player.receive_card(self.shoe.draw_card(), len(self.player.hands) - 1)

        if self.current_hand_index >= len(self.player.hands):
            self.is_done = True
            if any(not hand.is_busted for hand in self.player.hands):
                self._play_dealer_turn()

            reward = self._resolve_round_rewards()
            return None, reward, True, []

        next_state = self._get_hand_state(self.current_hand_index)
        valid_actions = self.get_valid_actions(self.current_hand_index)
        return next_state, reward, False, valid_actions