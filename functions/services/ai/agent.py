"""
Agent for playing Shogi using a Deep Q-Network (DQN). Handles model initialization,
action selection, memory management, and training using experience replay.
"""

import os

import numpy as np
from shogi import Move
import torch

from services.ai.deep_q_network import DQN
from services.ai.environment import ShogiEnv


class ShogiAgent:
    """
    Agent for playing Shogi using a Deep Q-Network (DQN). Handles model initialization,
    action selection, memory management, and training using experience replay.
    """

    def __init__(self, path: str | None = None):
        """
        Initializes the ShogiAgent with parameters, networks, loss function, and optimizer.
        """
        self.target_network = DQN()
        if path:
            self.get_model(path)
    @staticmethod
    def get_move_index(move):
        """
        Converts a move to an index.
        """
        index = 81 * ShogiAgent.get_from_square(move) + move.to_square
        return index

    @staticmethod
    def get_from_square(move):
        """
        Converts a move to an index.
        """
        # pieces = ["", "p", "l", "n", "s", "g", "b", "r"]
        if(move.from_square == None):
            # from_square max = 81
            return 81 + move.drop_piece_type - 1
            # now from_square max = 88
        return move.from_square

    def mask_and_valid_moves(self, env: ShogiEnv) -> (np.array, dict):
        """
        Get the mask and valid moves for the current player.
        """
        mask = np.zeros((88, 81))
        valid_moves_dict = {}

        legal_moves = env.get_legal_moves()

        for move in legal_moves:
            mask[self.get_from_square(move), move.to_square] = 1
            valid_moves_dict[self.get_move_index(move)] = move

        return mask, valid_moves_dict

    def select_action(self, env: ShogiEnv) -> (Move, int):
        """
        Selects an action using an epsilon-greedy policy.
        """
        valid_moves, valid_move_dict = self.mask_and_valid_moves(env)

        current_state = env.get_observation()
        valid_moves_tensor = torch.from_numpy(valid_moves).float().unsqueeze(0)
        current_state_tensor = torch.from_numpy(current_state).float().unsqueeze(0)
        valid_moves_tensor = valid_moves_tensor.view(current_state_tensor.size(0), -1)
        policy_values = self.target_network(current_state_tensor, valid_moves_tensor)
        chosen_move_index = int(policy_values.max(1)[1].view(1, 1))
        chosen_move = valid_move_dict[chosen_move_index]

        return chosen_move, chosen_move_index

    def get_model(self, path: str):
        """
        Get the model parameters from the specified path.
        """
        if os.path.isfile(path):
            model_dict = torch.load(path)
            self.target_network.load_state_dict(model_dict)
